# Project spec: Satellite-confirmed rain-damage index for California strawberries

Read this file at the start of every session. It is the source of truth for scope.
If a task would take the work outside this spec, stop and ask.

## 1. The question

For California strawberries, does a **rainfall trigger confirmed by satellite imagery**
separate fields that actually lost crop from fields that did not, better than a
rainfall trigger alone?

This is a feasibility analysis for a federal crop insurance index product. The
customer is two named parties who asked for it: USDA RMA's Davis Regional Office
(exploring a rain index for strawberries) and Agralytica (RMA policy-development
contractor). The deliverable is figures and a short written exhibit, not software.

Design principle, fixed: **rainfall carries the insurable event; imagery is a
confirmation gate that blocks payouts to fields with no visible damage.** Imagery is
never the loss meter. Rot, mold, and internal fruit damage are invisible from orbit.

## 2. Scope

**Study area:** Monterey County (FIPS 06053) and Santa Cruz County (FIPS 06087).

**Primary event:** Pajaro River levee breach, night of March 10–11, 2023. Strawberry
fields near Pajaro and Watsonville flooded; fields in the Salinas Valley a few miles
away did not. Same county, same storm, same coarse rainfall grid, different outcomes.
This is a natural experiment for basis risk.

**Secondary events (only if primary completes):** January 4–16, 2023 atmospheric
rivers (Salinas River flooding); February 2017 storms.

**Out of scope, do not build:** a UI, a general pipeline for other crops or counties,
a rating model, anything requiring paid imagery, anything requiring RMA data that
has not been shared.

## 3. Deliverables

1. `notebooks/` — reproducible notebooks, one per stage (see §6), runnable top to
   bottom in Google Earth Engine via the Python API.
2. `figures/` — the six figures in §7.
3. `data/derived/` — the per-unit table (§6, step 6) as CSV.
4. `EXHIBIT.md` — ten pages max, structured like an FCIC feasibility exhibit (§8).

## 4. Kill criteria (report these honestly, do not paper over them)

- If rainfall alone already discriminates flooded from unflooded units well, the
  image gate adds complexity without value. Say so.
- If Sentinel-1/2 cannot resolve strawberry beds at usable accuracy, the design
  should pivot to farmer photo verification. Say so.
- If ground truth cannot be established for any units, the analysis is theoretical
  and the exhibit must say so in its first paragraph.

## 5. Data sources

Use these exact Earth Engine dataset IDs. Do not substitute or invent IDs. If one is
unavailable, stop and report it.

| Purpose | Dataset | Notes |
|---|---|---|
| Strawberry fields | `USDA/NASS/CDL` | Band `cropland`, class **221 = Strawberries**. Use 2022 and 2023. 30 m. |
| Flood detection | `COPERNICUS/S1_GRD` | IW mode, VV polarization, 10 m. Keep one orbit direction. |
| Vegetation change | `COPERNICUS/S2_SR_HARMONIZED` | Bands B4, B8, scale 0.0001. Cloud mask with `GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED` (`cs_cdf` > 0.6). |
| Permanent water mask | `JRC/GSW1_4/GlobalSurfaceWater` | Exclude `occurrence` > 50. |
| Rain, coarse (PRF-like) | `NOAA/CPC/Precipitation` | Band `precipitation`, mm/day, 0.5°. The product PRF's Rainfall Index most resembles. |
| Rain, 4 km | `OREGONSTATE/PRISM/ANd` | Band `ppt`, mm/day. RMA reportedly evaluated PRISM and found it weak; test that claim. Replaces deprecated `AN81d`, which ends 2020-12-30 (see SPEC_CHANGELOG). |
| Rain, 1 km | `NASA/ORNL/DAYMET_V4` | Band `prcp`, mm/day. |
| Rain, satellite | `NASA/GPM_L3/IMERG_V07` | Band `precipitation`, mm/hr, half-hourly. Sum × 0.5. |
| Counties | `TIGER/2018/Counties` | Filter `GEOID` in `['06053','06087']`. |

**Non-GEE data (download manually, store in `data/raw/`, never modify):**

- **RMA Summary of Business, Cause of Loss files** (rma.usda.gov → Tools & Reports →
  Summary of Business → Cause of Loss). Filter: state CA, counties Monterey and Santa
  Cruz, commodity Strawberries, crop years 2015–2024. Fields of interest: cause of
  loss description (Excess Moisture/Precipitation/Rain; Flood), month of loss,
  indemnity amount. This is public, county-level loss ground truth.
- **CIMIS station data** (cimis.water.ca.gov): daily precipitation for stations in
  the study area for the event windows. Station-level check on the gridded products.
- **Flood extent reference** for March 2023: any published inundation map (FEMA,
  USGS, Cal OES, Monterey County, or a Copernicus EMS activation if one exists).
  Record source and date. If none is found, record that.
- **Grower or Strawberry Commission reports** of which blocks flooded, if obtained.
  Store as `data/raw/ground_truth_notes.md` with source and date for each entry.

## 6. Method, in order. Do not skip steps or run ahead.

Each step ends with a **CHECKPOINT**: produce the artifact, then stop and show it.
The human verifies before the next step starts.

**Step 1 — Analysis units.**
Rasterize CDL strawberries for 2022 and 2023 in the two counties. Aggregate to
250 m cells; keep cells with ≥ 60% strawberry pixels in both years. Exclude cells
touching permanent water. Export cell centroids and polygons.
CHECKPOINT: map of units over a satellite basemap. Human confirms units are
strawberry fields, not greenhouses, nurseries, or misclassified lettuce.

**Step 2 — Sentinel-1 flood mask.**
Pre window: Feb 1–Mar 8, 2023. Post window: Mar 11–20, 2023. Same orbit direction.
Apply 3×3 focal mean (speckle). Per pixel: flooded if
(post_VV_dB − pre_VV_dB) < −3 **and** post_VV_dB < −15. Mask permanent water.
Per unit: fraction of pixels flooded.
CHECKPOINT: pre image, post image, flood mask, side by side, with the town of
Pajaro labeled. Human confirms the known breach area shows as flooded and the
Salinas Valley does not.

**Step 3 — Sentinel-2 vegetation change.**
Pre composite: median NDVI, Feb 1–Mar 8, 2023, cloud-masked.
Post composite: median NDVI, Mar 20–Apr 30, 2023, cloud-masked.
Per unit: ΔNDVI = post − pre. Also record number of clear observations per unit in
each window, because the post window may be cloud-starved.
CHECKPOINT: ΔNDVI map and a histogram. Note how many units have < 2 clear post
observations.

**Step 4 — Rainfall per unit, four products.**
Event window: Mar 9–14, 2023. For each product, per unit: event total (mm) at the
unit centroid, and the mean of the grid cell containing it. Also compute the
Jan 4–16, 2023 total.
Add CIMIS station totals for comparison.
CHECKPOINT: table of per-unit event totals across products, and one figure
showing all four products over the study area. Note the range across products
for the same unit; that range is the basis risk of the rainfall data itself.

**Step 5 — Ground truth.**
Per unit, assign `truth` ∈ {flooded, not_flooded, unknown} from the flood extent
reference and any grower notes. Record the source for each assignment. Do not infer
truth from the imagery being tested; that is circular.
County level: from RMA Cause of Loss, tabulate strawberry indemnities by cause and
month, 2015–2024, both counties.
CHECKPOINT: count of units in each truth class. If most are `unknown`, stop and
report before continuing.

**Step 6 — Trigger logic and the four-cell table.**
Rain trigger: event total > T, for T in {50, 75, 100} mm, per product.
Image trigger: (S1 flooded fraction > 0.3) **or** (ΔNDVI < −0.15 with ≥ 2 clear
post observations).
Dual trigger: rain **and** image.
For each product × threshold, and for rain-only vs dual, tabulate against truth:
hit (pays, loss), miss (no pay, loss), false alarm (pays, no loss),
correct reject (no pay, no loss). Report counts and rates.
Output: `data/derived/units.csv` with every per-unit value used.
CHECKPOINT: the four-cell tables. This is the core result.

**Step 7 — Write EXHIBIT.md.** See §8.

## 7. Figures

1. Study area: analysis units over basemap, county lines, Pajaro River, Pajaro town.
2. Sentinel-1 pre, post, flood mask (three panels).
3. ΔNDVI map with clear-observation count inset.
4. Rainfall event totals, four products, same color scale (four panels).
5. Four-cell results: rain-only vs dual, best threshold per product (one table figure).
6. RMA Cause of Loss: strawberry indemnities by cause, 2015–2024, both counties (bar).

Every figure: title, data source, date window, scale bar, north arrow where spatial.
Save as PNG at 200 dpi and as the notebook cell that produced it.

## 8. EXHIBIT.md structure

Mirror how RMA justified FIP-SI and HIP-WI. Sections, in order:

1. Question and design principle (from §1), in five sentences.
2. Data sources: each with provider, resolution, years available, latency, and
   known weaknesses. This is what expert reviewers read first.
3. Event and study area.
4. Method (from §6), one paragraph per step.
5. Results: the four-cell tables; rain-only vs dual; rainfall-product disagreement.
6. Basis risk: false-alarm rate (pays without loss) and miss rate (loss without
   pay) for each design, stated plainly.
7. Limitations: cloud cover, mulch and bare-soil confounds, 250 m units vs bed
   width, invisibility of internal damage, single event, ground-truth coverage.
8. What it would take to be rateable: more events, more counties, field-level
   ground truth, possibly commercial 3 m imagery.
9. Verdict against the kill criteria in §4.

No adjectives about how promising this is. Numbers and their sources.

## 9. Repo layout

```
CLAUDE.md               this file
SPEC_CHANGELOG.md       any change to scope, dated, one line each
data/raw/               downloaded inputs, never modified
data/derived/           outputs of notebooks
notebooks/
  01_units.ipynb
  02_s1_flood.ipynb
  03_s2_ndvi.ipynb
  04_rain.ipynb
  05_truth.ipynb
  06_triggers.ipynb
figures/
EXHIBIT.md
```

## 10. Environment

Python 3.11. Packages: `earthengine-api`, `geemap`, `geopandas`, `rasterio`,
`pandas`, `matplotlib`. Earth Engine authentication is done by the human once
(`earthengine authenticate`); never attempt to authenticate or store credentials.
Export large rasters to Google Drive via `ee.batch`, then download to `data/derived/`.
Cache intermediate results; a notebook should not re-run a 20-minute export on
every execution.

## 11. Rules for the agent

- Do not invent dataset IDs, band names, class codes, or URLs. If unsure, say so.
- Do not fabricate ground truth, loss figures, or rainfall values. Empty cells are
  acceptable; invented ones are not.
- Never modify anything in `data/raw/`.
- Ask before any export longer than ~10 minutes or any operation that overwrites
  a derived file.
- Every notebook cell that produces a figure or table must also print the number of
  units, the date window, and the dataset ID used.
- When a result looks surprisingly good, flag it. Surprisingly good results in this
  domain usually mean a mask or a date window is wrong.
- Stop at every CHECKPOINT. Do not continue to the next step until told to.

## 12. Time box

Four weeks. Steps 1–2 in week one; 3–4 in week two; 5–6 in week three; 7 in week
four. At the start of week three, cut anything not needed for the four-cell table.
Secondary events only if the primary is complete and verified.
