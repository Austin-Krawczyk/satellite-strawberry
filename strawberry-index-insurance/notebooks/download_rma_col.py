"""Download RMA Summary of Business Cause of Loss files (CLAUDE.md §5, Step 5 context).

Provenance-recording downloader, same pattern as download_dwr_crop_mapping.py and
download_cimis.py: the zips land in data/raw/rma/ unmodified, with a SOURCE.md recording each
URL, retrieval date, SHA-256 and size. Nothing is filtered here; filtering happens in the
notebook so the raw files stay as published.

Source (verified 2026-09-17):
  https://www.rma.usda.gov/tools-reports/summary-of-business/cause-loss
  files  https://pubfs-rma.fpac.usda.gov/pub/Web_Data_Files/Summary_of_Business/
         cause_of_loss/colsom_<year>.zip
  layout .../cause_of_loss/COL_Summary_of_Business_with_Month_All_Years.pdf

Each zip holds one pipe-delimited text file with 30 unnamed fields. The layout is recorded in
COLUMNS below and in SOURCE.md so the notebook never guesses a column position.

Run:  python notebooks/download_rma_col.py
"""
from __future__ import annotations

import hashlib
import urllib.request
from datetime import date
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "data" / "raw" / "rma"
BASE = ("https://pubfs-rma.fpac.usda.gov/pub/Web_Data_Files/Summary_of_Business/"
        "cause_of_loss")
LAYOUT_URL = f"{BASE}/COL_Summary_of_Business_with_Month_All_Years.pdf"
YEARS = range(2015, 2025)          # crop years 2015-2024 (CLAUDE.md §5)

# Record layout, from the PDF above. Position is 1-based in the file; this list is 0-based.
COLUMNS = [
    "commodity_year", "state_code", "state_abbrev", "county_code", "county_name",
    "commodity_code", "commodity_name", "insurance_plan_code", "insurance_plan_abbrev",
    "coverage_category", "stage_code", "cause_code", "cause_description",
    "month_of_loss", "month_name", "year_of_loss", "policies_earning_premium",
    "policies_indemnified", "net_planted_quantity", "net_endorsed_acres", "liability",
    "total_premium", "producer_paid_premium", "subsidy", "state_private_subsidy",
    "additional_subsidy", "efa_premium_discount", "net_determined_quantity",
    "indemnity_amount", "loss_ratio",
]

UA = {"User-Agent": "Mozilla/5.0 (research download; USDA RMA public data files)"}


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
        return r.read()


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    records = []
    for year in YEARS:
        url = f"{BASE}/colsom_{year}.zip"
        path = RAW / f"colsom_{year}.zip"
        if path.exists():
            blob = path.read_bytes()
            print(f"  {path.name} already present ({len(blob):,} bytes), not re-downloaded")
        else:
            print(f"downloading {url} ...")
            blob = fetch(url)
            if blob[:2] != b"PK":
                raise SystemExit(f"{url} did not return a zip ({len(blob)} bytes)")
            path.write_bytes(blob)
            print(f"  wrote {path.name} ({len(blob):,} bytes)")
        records.append({"file": path.name, "url": url, "bytes": len(blob),
                        "sha256": hashlib.sha256(blob).hexdigest()})

    layout = RAW / "COL_record_layout.pdf"
    if not layout.exists():
        layout.write_bytes(fetch(LAYOUT_URL))
        print(f"  wrote {layout.name}")
    records.append({"file": layout.name, "url": LAYOUT_URL,
                    "bytes": layout.stat().st_size,
                    "sha256": hashlib.sha256(layout.read_bytes()).hexdigest()})

    lines = [
        "# RMA Summary of Business, Cause of Loss — provenance",
        "",
        "Publisher: USDA Risk Management Agency. Public data files, no registration required.",
        f"Retrieved: {date.today().isoformat()}",
        "Landing page: https://www.rma.usda.gov/tools-reports/summary-of-business/cause-loss",
        "",
        "Pipe (|) delimited flat files, one per crop year, 30 unnamed fields. Column names are",
        "taken from the record layout PDF below and are reproduced in `download_rma_col.py`;",
        "the notebook imports them rather than guessing a position. Indemnity Amount is field 29,",
        "Cause of Loss Description field 13, Month of Loss fields 14-15, Net Determined Quantity",
        "field 28 (acres lost after the insured's share).",
        "",
        "Zips are gitignored; this file is the record of what was downloaded.",
        "",
        "| File | URL | SHA-256 | Bytes |",
        "|---|---|---|---|",
    ]
    for r in records:
        lines.append(f"| `{r['file']}` | {r['url']} | `{r['sha256']}` | {r['bytes']:,} |")
    (RAW / "SOURCE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {RAW / 'SOURCE.md'}")


if __name__ == "__main__":
    main()
