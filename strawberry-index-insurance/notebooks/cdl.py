"""CDL helpers: download a one-class 0/1 mask on CDL's native 30 m grid as a local GeoTIFF."""
from pathlib import Path

import ee
import numpy as np
import rasterio
import requests
from rasterio.merge import merge

from common import CDL


def cdl_image(year):
    col = ee.ImageCollection(CDL).filterDate(f"{year}-01-01", f"{year + 1}-01-01")
    n = col.size().getInfo()
    assert n == 1, f"expected 1 CDL image for {year}, found {n}"
    return col.first().select("cropland")


def cdl_tif(path, year, bbox_lonlat, class_value=None, n_tiles=6):
    """uint8 GeoTIFF of CDL `cropland` on CDL's native 30 m grid (EPSG:5070).

    With `class_value`, writes a 0/1 mask for that class instead of the class codes.
    The bbox is split into `n_tiles` west-east strips to stay under Earth Engine's
    50 MB per-request download limit, and the strips are merged. Cached: skips if `path` exists.
    """
    path = Path(path)
    if path.exists():
        return path
    img = cdl_image(year)
    proj = img.projection().getInfo()
    crs = proj.get("crs") or proj["wkt"]
    mask = img.toByte() if class_value is None else img.eq(class_value).toByte()

    w, s, e, n = bbox_lonlat
    edges = np.linspace(w, e, n_tiles + 1)
    parts = []
    for i in range(n_tiles):
        url = mask.getDownloadURL({
            "region": ee.Geometry.BBox(edges[i], s, edges[i + 1], n),
            "crs": crs, "crs_transform": proj["transform"], "format": "GEO_TIFF",
        })
        resp = requests.get(url, timeout=900)
        if resp.status_code != 200:
            raise RuntimeError(f"Earth Engine download failed ({resp.status_code}): {resp.text[:500]}")
        part = path.with_name(f"{path.stem}_part{i}.tif")
        part.write_bytes(resp.content)
        parts.append(part)

    srcs = [rasterio.open(p) for p in parts]
    try:
        mosaic, transform = merge(srcs, method="max")
        profile = srcs[0].profile | {"height": mosaic.shape[1], "width": mosaic.shape[2],
                                     "transform": transform, "compress": "deflate"}
        with rasterio.open(path, "w", **profile) as dst:
            dst.write(mosaic)
    finally:
        for s_ in srcs:
            s_.close()
        for p in parts:
            p.unlink()
    return path
