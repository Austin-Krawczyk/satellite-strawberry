"""Download CIMIS station precipitation for Step 4b (CLAUDE.md §6).

Provenance-recording downloader, same pattern as download_dwr_crop_mapping.py: raw JSON goes to
data/raw/cimis/ unmodified, with a SOURCE.md recording the endpoint, parameters, retrieval date
and SHA-256 of each file.

The app key is read from the environment variable CIMIS_APP_KEY, or from data/raw/cimis/APP_KEY
(gitignored). It is never printed, never written into any output, and never committed.

API — the NEW CIMIS web API (verified by probe on 2026-09-16). The legacy API at
`/api/data` was operational only through 2026-07-31 and now returns a firewall rejection page
for any request carrying an `appKey` query parameter. The replacement sits behind Azure API
Management and takes the key as a HEADER, never in the query string:

  data     https://et.water.ca.gov/StationWeb/GetDataByStationNumber
           stationNbrs, startDate (yyyy-mm-dd), endDate, isHourly, unitOfMeasure, dataItems
  station  https://et.water.ca.gov/StationWeb/GetAllStations
  header   Ocp-Apim-Subscription-Key: <app key>

Limit: 1,750 records per request (stations x days).

Run:  python notebooks/download_cimis.py
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "data" / "raw" / "cimis"
DATA_URL = "https://et.water.ca.gov/StationWeb/GetDataByStationNumber"
STATION_URL = "https://et.water.ca.gov/StationWeb/GetAllStations"
MAX_RECORDS = 1750   # API limit: stations x days

# Study-area counties, plus neighbours: CIMIS is sparse and the nearest station to a given
# field may sit across a county line. Selection is by distance to the units, not by county.
COUNTIES = {"Monterey", "Santa Cruz", "San Benito", "Santa Clara"}

WINDOWS = [
    ("event_march", "2023-03-09", "2023-03-14"),   # the event window, Step 4
    ("context_january", "2023-01-04", "2023-01-16"),  # the January event, second data point
]
# Full calendar years at one station, for the units sanity check that caught the CPC error.
SANITY_YEARS = [2022, 2023]


KEY_NAMES = {"cimis_app_key", "cimis_appkey", "cimis_key"}
ROOT = Path(__file__).resolve().parent.parent


def _from_dotenv(path: Path) -> str:
    """Minimal KEY=value reader; no dependency on python-dotenv."""
    if not path.exists():
        return ""
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, _, value = line.partition("=")
        if name.strip().lower() in KEY_NAMES:
            return value.strip().strip('"').strip("'")
    return ""


def app_key() -> str:
    """Environment (any casing), then .env at the repo root, then the gitignored key file."""
    for name, value in os.environ.items():
        if name.lower() in KEY_NAMES and value.strip():
            return value.strip()
    for path in (ROOT / ".env", RAW / "APP_KEY"):
        found = _from_dotenv(path) if path.suffix == ".env" or path.name == ".env" else (
            path.read_text(encoding="utf-8").strip() if path.exists() else "")
        if found:
            return found
    sys.exit(
        "No CIMIS app key found. Checked, in order: the environment (CIMIS_APP_KEY, any\n"
        f"casing), {ROOT / '.env'}, and {RAW / 'APP_KEY'}.\n"
        "A variable set in your own terminal tab does not reach this process. All three of\n"
        "those locations are gitignored. The key is never printed or committed."
    )


def get(url: str, params: dict, key: str) -> bytes:
    """The key goes in the Azure APIM header. It never appears in the URL."""
    q = urllib.parse.urlencode(params)
    req = urllib.request.Request(
        f"{url}?{q}" if params else url,
        headers={"Accept": "application/json", "Ocp-Apim-Subscription-Key": key})
    with urllib.request.urlopen(req, timeout=180) as r:
        body = r.read()
    if body.lstrip()[:1] not in (b"{", b"["):
        raise SystemExit(f"Non-JSON response from {url} ({len(body)} bytes). "
                         "The request was rejected; the key is not included in URLs.")
    return body


def decimal_from_hms(s: str) -> float | None:
    """HmsLatitude looks like "36º20'10N / 36.3360"; take the decimal after the slash."""
    m = re.search(r"/\s*(-?\d+\.\d+)", s or "")
    return float(m.group(1)) if m else None


def write(name: str, blob: bytes, note: str, params: dict, records: list[dict]) -> None:
    path = RAW / name
    path.write_bytes(blob)
    records.append({
        "file": name,
        "note": note,
        "sha256": hashlib.sha256(blob).hexdigest(),
        "bytes": len(blob),
        "params": params,
    })
    print(f"  wrote {name} ({len(blob):,} bytes)")


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    key = app_key()
    records: list[dict] = []

    print("station metadata ...")
    blob = get(STATION_URL, {}, key)
    write("stations.json", blob, "full CIMIS station list", {}, records)
    stations = json.loads(blob)["Stations"]

    near = [s for s in stations if (s.get("County") or "").strip() in COUNTIES]
    for s in near:
        s["lat"] = decimal_from_hms(s.get("HmsLatitude", ""))
        s["lon"] = decimal_from_hms(s.get("HmsLongitude", ""))
    near = [s for s in near if s["lat"] is not None and s["lon"] is not None]
    targets = ",".join(str(s["StationNbr"]) for s in near)
    print(f"  {len(near)} stations in {sorted(COUNTIES)}: {targets}")
    if not near:
        sys.exit("No stations matched the county filter; check the station list.")

    for label, start, end in WINDOWS:
        print(f"daily precipitation, {label} ({start} to {end}) ...")
        params = {"stationNbrs": targets, "startDate": start, "endDate": end,
                  "isHourly": "false", "unitOfMeasure": "M", "dataItems": "day-precip"}
        write(f"daily_{label}.json", get(DATA_URL, params, key),
              f"day-precip, metric, stations {targets}, {start} to {end}", params, records)

    # Sanity-check station: the active station closest to Watsonville/Pajaro by longitude order
    # is chosen in the notebook; here we pull whichever active station is first in the list, and
    # record which, so the annual totals can be compared with PRISM and Daymet at that point.
    active = [s for s in near if s.get("IsActive") in (True, "True", "true")]
    sanity = (active or near)[0]
    for year in SANITY_YEARS:
        print(f"daily precipitation, station {sanity['StationNbr']} calendar {year} ...")
        params = {"stationNbrs": str(sanity["StationNbr"]),
                  "startDate": f"{year}-01-01", "endDate": f"{year}-12-31",
                  "isHourly": "false", "unitOfMeasure": "M", "dataItems": "day-precip"}
        write(f"daily_sanity_{sanity['StationNbr']}_{year}.json", get(DATA_URL, params, key),
              f"day-precip, metric, station {sanity['StationNbr']} ({sanity['Name']}), {year}",
              params, records)

    lines = [
        "# CIMIS station data — provenance",
        "",
        "Publisher: California Department of Water Resources, California Irrigation Management",
        "Information System (CIMIS). Retrieved with the CIMIS Web API.",
        "",
        f"Retrieved: {date.today().isoformat()}",
        f"Data endpoint: {DATA_URL}",
        f"Station endpoint: {STATION_URL}",
        "Units requested: metric (`unitOfMeasure=M`), so `DayPrecip` is in millimetres.",
        "Data item: `day-precip`.",
        "",
        "Authentication: the app key is sent as the `Ocp-Apim-Subscription-Key` HTTP header",
        "(Azure API Management). It never appears in a URL. It is supplied at run time from the",
        "environment or a gitignored file, **is not recorded here and must not be committed.**",
        "",
        "The legacy API at `/api/data` was retired after 2026-07-31; requests carrying an",
        "`appKey` query parameter are rejected by the site firewall. See SPEC_CHANGELOG.",
        "",
        f"Counties filtered: {', '.join(sorted(COUNTIES))}. Station selection for the comparison",
        "is by distance to the analysis units, done in `notebooks/04b_cimis_check.ipynb`.",
        "",
        "## Files",
        "",
        "| File | Contents | SHA-256 | Bytes |",
        "|---|---|---|---|",
    ]
    for r in records:
        lines.append(f"| `{r['file']}` | {r['note']} | `{r['sha256']}` | {r['bytes']:,} |")
    lines += ["", "## Request parameters", "", "```json",
              json.dumps([{"file": r["file"], "params": r["params"]} for r in records], indent=2),
              "```", ""]
    (RAW / "SOURCE.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {RAW / 'SOURCE.md'}")


if __name__ == "__main__":
    main()
