"""Download the DWR / Land IQ Statewide Crop Mapping file geodatabases (2022, 2023) into
data/raw/dwr_crop_mapping/, untouched, and record provenance in SOURCE.md.

Never overwrites: files already present are skipped, and SOURCE.md is only created, never edited.
Run from the notebooks/ folder:  python download_dwr_crop_mapping.py
"""
import hashlib
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests

from common import RAW

DEST = RAW / "dwr_crop_mapping"
PAGE = "https://data.cnra.ca.gov/dataset/statewide-crop-mapping/resource/{rid}"
API = "https://data.cnra.ca.gov/api/3/action/resource_show?id={rid}"
ALLOWED_HOSTS = ("data.cnra.ca.gov", "water.ca.gov")
RESOURCES = {  # file geodatabase resources on the CNRA "Statewide Crop Mapping" dataset page
    "2022": "e41f74d2-7ff9-4871-bc95-1e9673fc53cb",
    "2023": "4e17ca38-268e-4bf5-bbc5-09636d44ed60",
}

DEST.mkdir(parents=True, exist_ok=True)
rows = []
for year, rid in RESOURCES.items():
    meta = requests.get(API.format(rid=rid), timeout=60).json()["result"]
    url = meta["url"]
    host = urlparse(url).hostname or ""
    if urlparse(url).scheme != "https" or not any(host == h or host.endswith("." + h) for h in ALLOWED_HOSTS):
        sys.exit(f"{year}: download URL on unexpected host, stopping: {url}")
    if year not in (meta.get("name") or "") + url:
        sys.exit(f"{year}: resource name/URL does not mention {year}, stopping: {meta.get('name')!r} {url}")
    out = DEST / urlparse(url).path.rsplit("/", 1)[-1]
    print(f"{year}: {meta.get('name')!r} format={meta.get('format')} last_modified={meta.get('last_modified')}")
    print(f"      {url}")
    if out.exists():
        print(f"      {out.name} already present; not downloaded again")
        sha = hashlib.sha256(out.read_bytes()).hexdigest()
    else:
        h = hashlib.sha256()
        with requests.get(url, stream=True, timeout=900) as r:
            r.raise_for_status()
            tmp = out.with_suffix(out.suffix + ".part")
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(chunk_size=1 << 20):
                    f.write(chunk)
                    h.update(chunk)
            tmp.rename(out)
        sha = h.hexdigest()
        print(f"      saved {out.name}")
    rows.append((year, meta, url, out, sha))

src = DEST / "SOURCE.md"
if src.exists():
    print(f"{src.name} exists; not modified")
else:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        "# DWR / Land IQ Statewide Crop Mapping — provenance",
        "",
        "Publisher: California Department of Water Resources; produced by Land IQ LLC.",
        "Dataset page: https://data.cnra.ca.gov/dataset/statewide-crop-mapping",
        "Files are stored exactly as downloaded and must not be modified (CLAUDE.md §11).",
        "",
        "| Year | Resource | Resource page | Download URL | File | Bytes | SHA-256 | CNRA last modified | Downloaded (UTC) |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for year, meta, url, out, sha in rows:
        lines.append(f"| {year} | {meta.get('name')} | {PAGE.format(rid=meta['id'])} | {url} | {out.name} | "
                     f"{out.stat().st_size} | {sha} | {meta.get('last_modified')} | {today} |")
    src.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {src.name}")
