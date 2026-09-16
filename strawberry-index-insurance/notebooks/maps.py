"""Map helpers shared by the notebooks: Sentinel-2 basemap, scale bar, north arrow.

Axes are assumed to be in common.GRID_CRS (metres).
"""
from pathlib import Path

import ee
import matplotlib.patheffects as pe
import numpy as np
import rasterio
import requests

from common import CLEAR_CS_CDF, GRID_CRS, S2, S2_CLOUD

HALO = [pe.withStroke(linewidth=2.5, foreground="black")]


def _halo(color):
    """Contrasting outline: white around dark text, black around light text."""
    return [pe.withStroke(linewidth=2.5, foreground="white" if color in ("black", "k") else "black")]


def s2_basemap(path, bbox_lonlat, scale_m, start, end, max_scene_cloud=10):
    """Cloud-masked Sentinel-2 true-colour median, saved as an RGB GeoTIFF in GRID_CRS.

    Scenes with CLOUDY_PIXEL_PERCENTAGE >= max_scene_cloud are dropped first; without that
    pre-filter a multi-month median exceeds Earth Engine's interactive memory limit.
    Downloads only if `path` does not exist. Returns (H x W x 3 uint8 array, extent)
    with extent as (left, right, bottom, top) for imshow.
    """
    path = Path(path)
    if not path.exists():
        region = ee.Geometry.BBox(*bbox_lonlat)
        clear = (ee.ImageCollection(S2).filterBounds(region).filterDate(start, end)
                 .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", max_scene_cloud))
                 .linkCollection(ee.ImageCollection(S2_CLOUD), ["cs_cdf"])
                 .map(lambda im: im.updateMask(im.select("cs_cdf").gt(CLEAR_CS_CDF))))
        rgb = (clear.select(["B4", "B3", "B2"]).median().multiply(0.0001)
               .visualize(min=0, max=0.3))
        url = rgb.getDownloadURL({"region": region, "crs": GRID_CRS,
                                  "scale": scale_m, "format": "GEO_TIFF"})
        resp = requests.get(url, timeout=900)
        if resp.status_code != 200:
            raise RuntimeError(f"Earth Engine download failed ({resp.status_code}): {resp.text[:500]}")
        path.write_bytes(resp.content)
    with rasterio.open(path) as src:
        rgb = np.moveaxis(src.read([1, 2, 3]), 0, -1)
        b = src.bounds
    return rgb, (b.left, b.right, b.bottom, b.top)


def add_scale_bar(ax, length_km, loc=(0.05, 0.05), color="white"):
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    x, y = x0 + loc[0] * (x1 - x0), y0 + loc[1] * (y1 - y0)
    ax.plot([x, x + length_km * 1000], [y, y], color=color, lw=4,
            solid_capstyle="butt", path_effects=_halo(color))
    ax.text(x + length_km * 500, y + 0.015 * (y1 - y0), f"{length_km:g} km", color=color,
            ha="center", va="bottom", fontsize=9, fontweight="bold", path_effects=_halo(color))


def add_north_arrow(ax, loc=(0.94, 0.86), color="white"):
    # In EPSG:3310 grid north is within ~2° of true north across the study area.
    ax.annotate("N", xy=(loc[0], loc[1] + 0.08), xytext=(loc[0], loc[1]),
                xycoords="axes fraction", ha="center", va="top", color=color,
                fontsize=12, fontweight="bold", path_effects=_halo(color),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2))


def ee_tif(img, path, bbox_lonlat, scale_m, crs=GRID_CRS):
    """Download an Earth Engine image as a GeoTIFF over bbox_lonlat, in `crs` at `scale_m`.

    For RGB pass an image already run through .visualize(). Cached: skips if `path` exists.
    Returns (array [H, W] or [H, W, bands], extent) with extent as (left, right, bottom, top).
    """
    import numpy as np
    import rasterio
    import requests

    path = Path(path)
    if not path.exists():
        url = img.getDownloadURL({"region": ee.Geometry.BBox(*bbox_lonlat), "crs": crs,
                                  "scale": scale_m, "format": "GEO_TIFF"})
        resp = requests.get(url, timeout=900)
        if resp.status_code != 200:
            raise RuntimeError(f"Earth Engine download failed ({resp.status_code}): {resp.text[:500]}")
        path.write_bytes(resp.content)
    with rasterio.open(path) as src:
        arr = src.read()
        b = src.bounds
    arr = np.moveaxis(arr, 0, -1) if arr.shape[0] > 1 else arr[0]
    return arr, (b.left, b.right, b.bottom, b.top)
