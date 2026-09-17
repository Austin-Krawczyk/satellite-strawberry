# Satellite-confirmed rainfall index for California strawberries

A feasibility analysis of one question, for one event:

> **Does a rainfall trigger confirmed by satellite imagery separate flooded strawberry fields
> from unflooded ones better than a rainfall trigger alone?**

Prepared for USDA RMA's Davis Regional Office and Agralytica, who are exploring a rainfall index
product for strawberries. The test case is the **Pajaro River levee breach of 10–11 March 2023**
in Monterey and Santa Cruz counties, California, across **1,320 strawberry fields** totalling
14,683 acres.

**The deliverable is an analysis, not software.** The code here exists to produce the figures and
the numbers in the exhibit, and to let someone else check them.

---

## Start here

| If you want | Read |
|---|---|
| The conclusion, in three paragraphs | [`SUMMARY.md`](strawberry-index-insurance/SUMMARY.md) |
| The full argument, with every table and caveat | [`EXHIBIT.md`](strawberry-index-insurance/EXHIBIT.md) |
| What was specified, and every scope change | [`CLAUDE.md`](strawberry-index-insurance/CLAUDE.md), [`SPEC_CHANGELOG.md`](strawberry-index-insurance/SPEC_CHANGELOG.md) |
| The code, in the order it ran | [`notebooks/`](strawberry-index-insurance/notebooks) |
| The per-field numbers | [`data/derived/units.csv`](strawberry-index-insurance/data/derived) |

---

## What it found

**The design did not work on this event**, for three independent reasons — none of them a
threshold that could be retuned.

**1. Neither sensor could see the fields at peak inundation.** There was no usable optical view
of the valleys for 11–14 March: no Sentinel-2 overpass at all on 11, 13 or 14 March, and the
12 March overpass was 0% clear over both valleys. The cloud is not bad luck — the storm that
caused the flood is the system that hid it. Sentinel-1 sees through cloud, but its coverage is
track-dependent: only five passes between 1 February and 31 March covered ≥95% of the fields, and
the breach fell inside a 12-day gap (7 → 19 March). Only Sentinel-1A was flying in 2023;
Sentinel-1B had been retired in August 2022, halving revisit. Sentinel-1C, launched December 2024,
has since restored it.

**2. The imagery gate missed the fields it most needed to catch.** Of the 18 fields the optical
reference places in standing water on 15 March, the radar gate fired on 3 and the NDVI gate on 3
— 6 by either, a 33% detection rate. Fifteen fields at 95–100% inundation carried a radar flooded
fraction of exactly zero. The mechanism is plastic mulch: it is radar-dark, so flooding *raises*
backscatter on these beds instead of lowering it, and the specified mask fires on a drop. The
radar gate fired on every field where backscatter fell and none of the 15 where it rose.
Widening the flooded set to cover 58% of the county's reported acreage drops detection to **17%**,
so 33% is the gate's best case.

**3. No rainfall threshold separated flooded from dry fields, in any of four products.** At 50 mm
all four pay every field in the study area. The coarsest product — closest in grid size to the one
RMA's Rainfall Index uses — returns only **five distinct values across all 1,320 fields** and gives
flooded and dry fields the identical median total of 79.2 mm. Fourteen CIMIS ground stations
recorded between 33.8 mm and 137.3 mm over the same six days, and that spread is spatially
coherent, so the variation the coarse grid erases is real measured rainfall.

The reason for the third failure is physical: **the water came from a levee failure upstream, not
from rain falling on the field.**

### The finding most likely to transfer

What the imagery detected was standing water. Once the water drained the canopy looked unchanged
— the signal decays to 1 field in 18 within two weeks, and the event never appears in the crop's
seasonal growth curve. So the gate confirmed **inundation**, which the weather trigger already
implies, rather than **damage**, which it never saw. A gate that only re-detects the hazard adds
verification cost without adding information about loss.

Whether that extends to other perils is stated in the exhibit as **a proposition worth testing,
not a result established here** — it rests on one peril, one crop, one event.

### The constructive recommendation

This event is the wrong test case for a rainfall index and the **right** test case for a **river
stage trigger**. Gauge stage is observed hourly, has a long record, and is causally upstream of
the damage.

### Two results worth reusing

- **Mulched strawberry beds are radar-dark.** Before any flooding, 50.4% of strawberry fields read
  as majority open water in VH against 21.2% of neighbouring lettuce fields (a factor of 2.4);
  median water-like fractions are 0.503 against 0.115 (a factor of 4.4). Useful to anyone
  attempting SAR monitoring of mulched specialty crops, insurance or not.
- **There is almost no insured loss history here.** Across crop years 2015–2024, the entire federal
  cause-of-loss record for strawberries in these two counties is **two claims**, both from this
  event, totalling $497,559 — against the 1,919 acres and $160 million the county reported lost.
  That is what a protection gap looks like; it also means there is no local insured experience to
  rate a product against.

---

## Please read the numbers with these caveats

These are not fine print. Quoting the figures without them will misrepresent the work.

- **This measures flood detection, not loss prediction.** No field-level loss records exist for
  this event. Fields are classified flooded or not flooded against an optical water mask built
  here — never lost or not lost. Every "hit" and "miss" is a detection or a failure to detect.
- **The reference is a water mask derived in this analysis**, not a surveyed inundation extent.
  Its first clear view is four days after the peak, so it under-counts flooded area — which biases
  *against* the method, not for it.
- **Do not quote "18 of 18" from the 15 March NDVI window.** Those units were *defined* by the
  15 March water mask, and NDWI shares a band with NDVI, so that column largely restates the
  reference definition. The exhibit explains this where the number appears.
- **Neither crop map is ground truth.** DWR defines the units and publishes no strawberry-specific
  accuracy; its acreage and the Commission's district projection disagree by a third.
- **One event, two counties, one crop.** Eighteen reference units carry the central measurement,
  and all of them are in Monterey County.

---

## Layout

```
strawberry-index-insurance/
  SUMMARY.md            one page, three paragraphs
  EXHIBIT.md            the full exhibit, FCIC-style, ~8,500 words
  CLAUDE.md             the project specification and source of truth for scope
  SPEC_CHANGELOG.md     every scope change, dated, with its reasoning
  requirements.txt      pinned versions (Python 3.11)
  notebooks/            one per stage, runnable top to bottom
  figures/              the six numbered figures plus supplementary ones
  data/raw/             downloaded inputs, never modified; SOURCE.md records provenance
  data/derived/         everything the notebooks produce
  docs/                 aggregate loss figures used only as sanity checks
```

Notebooks run in name order: `01` units → `01c` optical flood reference → `02` Sentinel-1 →
`02b`/`02c` mulch and confound tests → `03`/`03b` NDVI → `04`/`04b` rainfall and the station
check → `05` RMA loss history → `06` trigger logic and the four-cell tables.

---

## Reproducing it

```bash
pip install -r strawberry-index-insurance/requirements.txt
earthengine authenticate          # once, per user
```

Earth Engine does the heavy lifting; set your own project id in `notebooks/common.py`. Three
inputs are downloaded rather than pulled from Earth Engine, each by its own script with
provenance and SHA-256 recorded:

- `notebooks/download_dwr_crop_mapping.py` — DWR / Land IQ crop map (defines the fields)
- `notebooks/download_rma_col.py` — RMA Summary of Business, Cause of Loss
- `notebooks/download_cimis.py` — CIMIS station precipitation

**The CIMIS script needs a personal app key**, which is not in this repository and must not be.
Put it in a gitignored `.env` as `CIMIS_APP_KEY=...`; the script sends it as an HTTP header and
never in a URL.

**A reproducibility note that will otherwise waste your afternoon:** the legacy CIMIS Web API
(`/api/data`, key as an `appKey` query parameter) was retired on 31 July 2026. Requests carrying
that parameter are now rejected by the site firewall whatever the key's value, with no informative
error. The current endpoint is `/StationWeb/GetDataByStationNumber` behind Azure API Management.

Large raw archives (the crop-map geodatabases, the RMA zips, exported rasters) are **not
redistributed here** — the download scripts fetch them from the publishers, and `SOURCE.md` in
each `data/raw/` subdirectory records exactly what was retrieved, when, and with what checksum.

---

## Data sources

All inputs are public. Earth Engine: Sentinel-1 GRD, Sentinel-2 SR Harmonized with Cloud Score+,
JRC Global Surface Water, NOAA CPC, PRISM, Daymet V4, GPM IMERG V07, USGS 3DEP, WWF HydroSHEDS,
TIGER counties, USDA NASS CDL. Outside Earth Engine: California DWR / Land IQ Statewide Crop
Mapping, USGS streamflow gauges, USDA RMA Summary of Business, and CIMIS station data. Each is
listed in `EXHIBIT.md` §2 with provider, resolution, years, latency and known weaknesses, and each
publisher's own terms apply to their data.

The only non-public figures are the aggregate county loss numbers in
`docs/ground_truth_aggregate.md`, supplied by the author and used solely as order-of-magnitude
checks.

---

## Status

Complete. Every deliverable and figure specified in `CLAUDE.md` exists. Known gaps are stated in
the exhibit rather than hidden: there is no field-level loss data, the analysis covers a single
event, and the design-level generalisation is offered as a testable proposition.

Analysis by Austin Krawczyk, UC Davis, September 2026.

*No licence is currently declared, so default copyright applies and the terms for reuse are
undecided. If you want this to be genuinely reusable, add one.*
