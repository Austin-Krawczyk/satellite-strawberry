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
fields near Pajaro and Watsonville flooded. **Revised 2026-09-16:** the Step 1c optical
reference shows the Salinas River corridor flooded as well, so Salinas Valley fields are
not a dry control. The natural experiment is therefore **fields inside a flood corridor
versus fields outside both the Pajaro and Salinas corridors**, in the same counties, under
the same storm and the same coarse rainfall grid.

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
4. `EXHIBIT.md` — structured like an FCIC feasibility exhibit (§8). **Length, revised
   2026-09-16:** approximately 6,300 words with nine tables, five of them mandatory (the
   four-cell tables, the 18-unit reference table, the optical acquisition table, the radar
   coverage table and the dataset table; the other four carry the NDVI timing comparison,
   the rainfall event totals, the mulch comparison and the basis-risk rates), rendering to
   about ten pages at 10pt with 0.75-inch margins. Word count
   and table count are the measures, not a rendered page count. The original ten-page cap was
   set before the analysis produced its table load; none of the mandated content in §8 is to be
   cut to meet a page number.
5. `SUMMARY.md` — one page, three paragraphs, no tables: what was tested, what was found, what
   it means for an index product, with no caveat beyond the absence of field-level loss data.
   Read first; the exhibit is checked afterward. Added 2026-09-16.

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
| Analysis units | `projects/cropczyk/assets/strawberry_fields_dwr_wy2023` | Uploaded from the DWR WY2023 crop map (see Non-GEE data). All T20 fields in the two counties; `is_unit` marks sequence A fields (§6 step 1). |
| Strawberry fields, comparison | `USDA/NASS/CDL` | Band `cropland`, class **221 = Strawberries**. Use 2022 and 2023. 30 m. Comparison only since 2026-09-15 (see SPEC_CHANGELOG). |
| Flood detection | `COPERNICUS/S1_GRD` | IW mode, **VV and VH** polarization, 10 m. Keep one orbit direction, and pair pre with post on the same relative orbit (§6 step 2). |
| Vegetation change | `COPERNICUS/S2_SR_HARMONIZED` | Bands B4, B8, scale 0.0001. Cloud mask with `GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED` (`cs_cdf` > 0.6). |
| Permanent water mask | `JRC/GSW1_4/GlobalSurfaceWater` | Exclude `occurrence` > 50. |
| Rain, coarse (PRF-like) | `NOAA/CPC/Precipitation` | Band `precipitation`, **0.1 mm/day — multiply by 0.1 for mm** (corrected 2026-09-16; the catalog states "Daily total precipitation estimate in 0.1 mm"). 0.5°. The product PRF's Rainfall Index most resembles. |
| Rain, 4 km | `OREGONSTATE/PRISM/ANd` | Band `ppt`, mm/day. RMA reportedly evaluated PRISM and found it weak; test that claim. Replaces deprecated `AN81d`, which ends 2020-12-30 (see SPEC_CHANGELOG). |
| Rain, 1 km | `NASA/ORNL/DAYMET_V4` | Band `prcp`, mm/day. |
| Rain, satellite | `NASA/GPM_L3/IMERG_V07` | Band `precipitation`, mm/hr, half-hourly. Sum × 0.5. |
| Elevation (Step 2c) | `USGS/3DEP/10m_collection` | 10 m elevation, band `elevation`; an ImageCollection, so mosaic it. Replaces deprecated `USGS/3DEP/10m` (see SPEC_CHANGELOG). For the confound test on field position. |
| River lines (Step 2c) | `WWF/HydroSHEDS/v1/FreeFlowingRivers` | Distance from fields to the Pajaro and Salinas channels. Coarse network; note the limitation. |
| Counties | `TIGER/2018/Counties` | Filter `GEOID` in `['06053','06087']`. |

**Non-GEE data (download manually, store in `data/raw/`, never modify):**

- **DWR / Land IQ Statewide Crop Mapping** (data.cnra.ca.gov/dataset/statewide-crop-mapping),
  WY2022 and WY2023 final file geodatabases in `data/raw/dwr_crop_mapping/` (provenance
  in `SOURCE.md`; zips gitignored). Field-boundary polygons. Strawberries are subclass
  **T20** in `CROPTYP1`–`CROPTYP4` and `MAIN_CROP`. Peak-NDVI dates are in `ADOY1`–`ADOY4`
  (WY2023: −92 = 1 Oct 2022 … −1 = 31 Dec 2022, 1 = 1 Jan 2023 … 273 = 30 Sep 2023).
  There is no planting date. Defines the analysis units. **Not ground truth:** no
  strawberry-specific accuracy is published, and WY2023 main-crop T20 acreage in the
  two counties is 132% of the Commission's district projection.
- **USGS streamflow gauges** (waterservices.usgs.gov): Pajaro River at Chittenden (site
  11159000) and a Salinas River gauge, event-window gage height and discharge, stored in
  `data/raw/usgs/` with site numbers and retrieval date. Used in Step 2 to report peak stage
  and discharge alongside the rainfall totals.
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
Units are DWR WY2023 field polygons with strawberries (T20) as the only crop of the
water year (**sequence A**), in the two counties (DWR `COUNTY`, the county of the
field centroid). Exclude fields touching permanent water. T20 fields where
strawberries were followed by another crop (**sequence B**) or planted after one
(**sequence C**) stay in the unit table, flagged as non-units, with their crop
sequence and T20 peak-greenness date as attributes; do not filter them away. Upload
all T20 fields with these attributes as the Earth Engine asset in §5. Report CDL
2023 cells (250 m, ≥ 60% class 221; 127 units) and the both-years cells (15) as the
comparison. When the flood extent reference arrives, report unit counts inside and
outside the footprint for the DWR units, with the CDL cells as comparison.
CHECKPOINT: map of units over a satellite basemap. Human confirms units are
strawberry fields, not greenhouses, nurseries, or misclassified lettuce.

**Step 1c — Optical flood reference (run before Step 2).**
No independent flood extent polygon is available for this event. Every ready-made SAR
flood product (NASA/ASF, Copernicus GFM, ARIA, OPERA) is derived from Sentinel-1, so
using one to validate the Sentinel-1 analysis would be circular. Naming trap: the NASA
Disasters service named `california_atmospheric_river_2023` covers only the January
2023 event (image dates 1/1 through 1/23), not the March breach.
Build the reference from optical bands only. **Do not use any Sentinel-1 data in this
step.** With `COPERNICUS/S2_SR_HARMONIZED` and Cloud Score+ masking (`cs_cdf` > 0.6):

1. **Acquisition table**, a standalone result for the exhibit: every Sentinel-2 acquisition
   over the study area from March 11 to March 25, 2023, with the clear-pixel fraction for
   the study area, for the Pajaro and northern Salinas valleys, and for the lower Pajaro
   Valley. It shows that no optical observation exists for March 11–14, when water was at
   its peak, and that the valleys were 0% clear on March 12 and 17. This is the
   sensor-availability argument for SAR, stated in our own data rather than asserted.
2. **Water mask per date** for March 15, 20 and 25, 2023: NDWI = (B3 − B8)/(B3 + B8) and
   MNDWI = (B3 − B11)/(B3 + B11), compared against a pre-event baseline composite
   (February 1 – March 8, 2023), excluding permanent water
   (`JRC/GSW1_4/GlobalSurfaceWater` occurrence > 50).
3. **The reference is the union of those three dates**, exported to `data/derived/` as a
   polygon layer, each polygon tagged with the date it was first seen as water. Report it
   as three nested extents — seen on March 15, added by March 20, added by March 25 — and
   never as a single number. March 15 is the closest thing to peak extent; the March 25
   additions are more likely long-standing water or irrigation than flood. For each added
   extent also report how much of it was cloud-covered on the earlier dates, because both
   recession and cloud gaps create additions.
4. **Threshold sensitivity**, reported at this checkpoint: mapped area with the NDWI and
   MNDWI minima at 0 and at 0.1, the MNDWI rise over baseline at 0.15, 0.2 and 0.25, and
   the minimum polygon size at 0.1, 0.2 and 0.5 ha. We need to know how much of the
   reference is a threshold choice before using it to judge the radar.
5. **Figure:** pre-event composite, the post-event composites, and the union mask coloured
   by the date first seen, over the Pajaro Valley and Salinas Valley.

This is the independent ground truth reference for Step 2.
CHECKPOINT: the figure, the acquisition table and the threshold sensitivity. Stop before
Step 2.

**Step 2 — Sentinel-1 flood mask.**
Pre window: Feb 1–Mar 8, 2023. Post window: Mar 11–20, 2023. IW mode, **VV and VH**, one
orbit direction, pairing pre with post on the same relative orbit. Apply 3×3 focal mean
(speckle). Per pixel, per polarization: flooded if (post_dB − pre_dB) < −3 **and**
post_dB < −15. Report the mask three ways: **VV only, VH only, and the two combined** — VH
often separates flooded vegetation from open water better than VV. Mask permanent water.
Per unit: fraction of pixels flooded.
**Baseline wetness, checked before differencing:** report how much of the study area, and how
many units, already show water-like backscatter in the Feb 1 – Mar 8 baseline. That window sits
in a wet winter that included the January flooding; if the baseline is already wet, the change
detection understates the March event, and the exhibit must say so.
**Radar availability, a standalone result:** for the event window list every Sentinel-1
acquisition over the units — date, relative orbit, orbit direction and the share of units its
footprint covers — and report the longest gap between usable acquisitions over the unit area.
State from the data which platforms were operating (Sentinel-1B failed in December 2021 and was
retired in August 2022, which cut revisit from 6 days to 12; Sentinel-1C launched in December 2024
and restores two-satellite revisit), so the exhibit can say that a product designed today faces a
different coverage regime than this event did.
**River stage:** report peak gage height and discharge for the Pajaro River at Chittenden
(USGS 11159000) and a Salinas River gauge over the event window, alongside the rainfall totals.
The breach was a hydraulic failure: water reached those fields because a structure gave way
upstream, not because a given amount of rain fell on the field.
**Comparison:** against the Step 1c optical reference in both directions, against both the
March 15 extent and the full union, plus flooded unit acreage against the 1,919-acre March
strawberry figure in `docs/ground_truth_aggregate.md`. Treat neither as truth; report both.
Use the optical reference at index minimum 0.0 as the default and carry the 0.1 variant as a
**sensitivity band on every agreement figure**, not as a separate table.
**Framing:** this measures **flood detection**, not loss. There is no field-level loss data.
**Analysis region:** Sentinel-1 statistics over both counties exceed Earth Engine's interactive
limits, so area statistics are computed over the Pajaro-to-northern-Salinas valley box. State that
region's area wherever acreages are reported, so they are never read as two-county totals. Per-unit
fractions still cover every unit.
CHECKPOINT: pre image, post image, flood mask, side by side, with the town of
Pajaro labeled. Human confirms the known breach area shows as flooded and the
Salinas Valley does not.

**Step 2b — Mulch confound investigation (run before Step 3).**
Step 2 found the median unit 50.3% water-like in VH before any flooding, consistent with
plastic mulch producing specular reflection indistinguishable from standing water at these
thresholds. That plausibly explains both the weak agreement with the optical reference and
the fact that only 11 units exceeded the flooded-fraction threshold while the county recorded
1,919 flooded strawberry acres.
- Report the **distribution** of baseline water-like fraction across units, VV and VH
  separately, not just the median, and the same for a comparison set of non-strawberry DWR
  fields in the same region (lettuce T30, cole crops T4), to show whether the effect is
  specific to mulched strawberry beds or general to the area.
- **Test whether the change signal survives:** for units inside the March 15 optical extent
  versus units outside it, compare the pre-to-post backscatter change rather than the absolute
  post value, restricted to units with a clear optical view on March 15. If mulch raises the
  baseline but flooding still lowers backscatter further, the mask definition is wrong rather
  than the method.
- If the change signal does not separate the two groups, report that plainly as a negative
  result against the §4 kill criterion on resolving strawberry beds. **Do not tune thresholds
  until something appears.**
- Report how many units fall inside the March 15 optical extent, as the denominator for the
  Step 2 count of units above the flooded-fraction threshold.
CHECKPOINT: the distributions, the change-signal comparison and the verdict. Stop before
Step 3.

**Step 2c — Is the brightening a confound? (run before Step 3).**
Aimed at the confound, not at rescuing the design.
- **Position rather than flooding?** Across all units, test whether pre-event VV backscatter is
  explained by distance to the river, elevation and field size, and whether the flooded and dry
  groups differ on those variables independently of flooding. Repeat the change comparison on dry
  units matched to the flooded group on elevation and distance. If pre-event brightness is
  explained by position rather than by flooding, say so plainly.
- **Does the brightening persist?** Compare the March 19 post value with the March 31 acquisition
  on the same track. Sediment deposition or damaged mulch should persist for weeks; transient
  standing water should not. This is a cheap test of the mechanism that 18 units cannot resolve
  on their own.
CHECKPOINT: correlations, the matched comparison, the persistence test, and a verdict on whether
the brightening survives the confound. Stop before Step 3.

**Step 3 — Sentinel-2 vegetation change.**
Pre composite: median NDVI, Feb 1–Mar 8, 2023, cloud-masked.
Post composite: median NDVI, Mar 20–Apr 30, 2023, cloud-masked.
Per unit: ΔNDVI = post − pre. Also record number of clear observations per unit in
each window, because the post window may be cloud-starved.
Planned validation, done here and not before: use February 2023 NDVI per field to
check the assumption that sequence A fields had a planted crop in March 2023; a
planted field should look different from bare ground.
CHECKPOINT: ΔNDVI map and a histogram. Note how many units have < 2 clear post
observations.

**Step 3b — The reference units, one by one (run before Step 4).**
With 18 units in the reference set, the exhibit shows them rather than summarising them.
- Report each of the 18 units the Step 1c reference places in standing water: inundation fraction
  on March 15, radar flooded fraction, VV pre and post, ΔNDVI, clear observation counts, elevation,
  acreage, and which gates fired. Reviewers need to see that the misses are not a handful of edge
  cases.
- **Ask why NDVI missed them.** The post window opens on March 20, nine days after the flood, so a
  fast-growing crop had time to recover before the first observation, and the pre window sits in a
  wet winter when the crop is small and mostly plastic, leaving little canopy to lose. Report ΔNDVI
  for those units using the tightest available post windows as well as the spec default, and state
  whether the miss is a timing artefact or a real absence of signal. **Do not change the spec
  default**; report both.
CHECKPOINT: the per-unit table and the timing comparison. Stop before Step 4.

**Step 4 — Rainfall per unit, four products.**
Event window: Mar 9–14, 2023. For each product, per unit: event total (mm) at the
unit centroid, and the mean of the grid cell containing it. Also compute the
Jan 4–16, 2023 total.
Add CIMIS station totals for comparison.
**Purpose, narrowed 2026-09-16:** the gauge evidence shows this was a hydraulic failure rather than
a rainfall-threshold event, so Step 4 tests whether any rainfall product would have triggered on
these fields at all. That bears on whether a rainfall gate alone is viable even though the imagery
gate is not.
CHECKPOINT: table of per-unit event totals across products, and one figure
showing all four products over the study area. Note the range across products
for the same unit; that range is the basis risk of the rainfall data itself.

**Step 5 — Ground truth. SKIPPED (decision of 2026-09-16).**
There is no field-level loss data, so `truth` cannot be assigned as lost or not lost. The Step 1c
optical reference supplies flooded / not flooded instead, and Step 6 uses it directly. The RMA
Cause of Loss tabulation stays in scope for the exhibit's context section if time allows.
Original text, retained for the record:
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
Output: `data/derived/units.csv` with every per-unit value used, including the
flagged sequence B and C fields.
The four-cell table measures **flood detection performance, not loss prediction**: `truth` is
flooded or not flooded from the Step 1c reference, and no field-level loss data exists. Do not
describe hits and misses as losses paid or missed.
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
5. Results, framed as flood detection performance and not loss prediction: the four-cell
   tables; rain-only vs dual; rainfall-product disagreement; and a **sensor-availability
   section** combining the Step 1c optical acquisition table (clear-pixel fraction over the
   valleys by date, showing no optical observation for March 11–14 when water was at its peak)
   with the Step 2 radar availability table (per-acquisition share of units covered, and the
   longest gap over the unit area). Report this as a finding in its own right, not merely as a
   limitation of this analysis: optical had no clear view at the peak and radar coverage was
   track-dependent and sparse, which together are the operational constraint on any
   imagery-confirmed trigger. State which satellites were flying at the time and how today's
   constellation differs.
   Include the rainfall result in the results section: **CPC takes only 5 distinct values across
   all 1,320 fields** and gives the reference and dry units the same median total (79.2 mm), so at
   the 0.5° grid PRF's Rainfall Index uses, a flooded field and its dry neighbour are the same
   pixel. Put the best case beside it: Daymet at 100 mm fires on 83% of reference units and 43% of
   dry ones, still paying 556 fields that never flooded. State that the four products disagree by a
   median 28.5 mm for the same field (90th percentile 57 mm), comparable to the spacing between the
   50, 75 and 100 mm thresholds themselves, so **the choice of rainfall product moves the outcome
   as much as the choice of trigger level — a rating problem independent of basis risk.**
6. Basis risk: false-alarm rate (pays where no flood was detected in the reference) and miss
   rate (flood in the reference with no payment) for each design, stated plainly as detection
   error against the Step 1c reference, not as loss outcomes.
7. Limitations: cloud cover, mulch and bare-soil confounds, 10–30 m pixels vs bed
   width, invisibility of internal damage, single event, ground-truth coverage, and
   crop-map uncertainty. For the last, state plainly that neither crop map is
   ground truth and that the uncertainty propagates into every result: DWR (which
   defines the units) publishes no strawberry-specific accuracy, and its WY2023
   main-crop T20 acreage is 132% of the Commission's district projection for a
   smaller area; DWR `ACRES` is whole-polygon area while the Commission figure is
   planted acreage, which plausibly explains part of the gap; CDL 2023 places only
   32.6% of its strawberry area inside DWR T20 fields. Do not resolve this by
   assuming either source is correct. Also state that sequence A fields having a
   crop in the ground in March 2023 is agronomic reasoning, not something the data
   states, and report the Step 3 February NDVI check on it. State that the unit definition
   rests on DWR's classification plus a visual check by the project owner across a sample,
   not on grower-confirmed field records; if results hinge on a small number of units, those
   units are revisited individually. State the limits of the
   Step 1c optical reference: the first clear Sentinel-2 pass is several days after the
   March 10–11 peak, so water has partly receded and the reference under-counts flooded
   area, which biases against this method rather than for it; cloud cover during the peak
   is why no optical observation exists at maximum inundation; and the reference is a
   water mask derived here, not a surveyed extent, so it carries its own error.
   State that there is no field-level loss data: units can be classified flooded or not, never
   lost or not; the 1,919-acre county figure is an aggregate from a voluntary survey with no
   map. State that flood from a levee breach and damage from direct rainfall are different
   perils that a real product would treat differently, and that this event tests the former.
   State that in the optical reference the index minimum moves mapped area by about a third
   while the change threshold moves it about 5%, so the reference carries a substantial
   analyst-choice component, reported as a sensitivity band on every agreement figure.
   State that the original natural-experiment premise (Salinas Valley as a dry control) was
   revised on 2026-09-16 when the Step 1c optical reference showed the Salinas River corridor
   flooded, and that the comparison is now flood-corridor fields against fields outside both
   corridors. State that the Sentinel-1 mask comes from the March 19 pass, 8 days after the
   peak, because no earlier pass covered the units.
   **Product-documentation risk, as a worked example:** the CPC band is stored in 0.1 mm/day, not
   mm/day. Read unscaled it gave 792 mm for the six-day event and 5,053 mm for calendar 2021 at
   Pajaro, against 592 mm from PRISM for the same point and year. Undetected, that single error
   would have produced a confident and wrong conclusion — that the coarse PRF-like product triggers
   everywhere at any threshold — which is a plausible-sounding statement about grid resolution that
   was really a units mistake. Anyone building an index on gridded inputs should cross-check
   products against each other and against physical plausibility before trusting any of them.
   **The CIMIS station check was not done:** the API requires a personal key that this project did
   not have, so the gridded products were never cross-checked against ground stations. Their
   absolute accuracy over these fields is unverified, although the disagreement between them is
   measured.
8. What it would take to be rateable: more events, more counties, field-level
   ground truth, possibly commercial 3 m imagery.
9. Verdict against the kill criteria in §4. State this plainly, near the front of the section,
   and do not soften it or bury it under the sensitivity tables.
   **Lead finding, design level: on this event the imagery gate confirmed inundation, not damage.**
   What the imagery detected was standing water; once the water drained the canopy looked unchanged
   (Step 3b: the signal decays to 3 of 18 units by March 20 and 1 of 18 by March 25). Inundation is
   already implied by the weather trigger, so a gate that only re-detects it adds verification cost
   without adding information about loss. That holds regardless of timing, threshold or sensor, and
   it generalises beyond strawberries to any peril where the visible signal is the hazard itself
   rather than its effect on the crop.
   **Second finding, measurement level: the imagery gate as specified fails on the fields it most
   needs to catch.**
   Of the 18 units the Step 1c reference places in standing water on March 15, the radar gate fires
   on 3 and the NDVI gate on 3, with 6 caught by either. Fifteen units at 95–100% inundation carry
   a radar flooded fraction of exactly 0.000 and NDVI changes of −0.02 to −0.11 against a −0.15
   trigger. The March event is also invisible in the units' seasonal NDVI trajectory. **Include the
   Step 3b per-unit table in full, not as an excerpt**, and keep the sentence that the radar gate
   fired on all 3 units where VV fell and on none of the 15 where it rose: that one sentence
   explains the entire radar failure.
   **The 18-of-18 figure from the March 15 window must never appear without its circularity
   caveat:** those units were defined by the March 15 water mask, NDWI shares band B8 with NDVI, so
   both fall when water covers a field, and that column largely restates the reference definition.
   **The specified design — a rainfall trigger confirmed by a radar flood mask — therefore did not
   work on California strawberries for this event.** Two mechanisms explain part of the failure and
   are secondary to the measurement above. First, no usable imagery existed at peak inundation from
   either sensor: no optical acquisition at all for March 11–14, and no radar pass covering the
   units between March 7 and March 19. Second, plastic mulch makes mulched beds radar-dark, so
   flooding raises rather than lowers backscatter and the specified mask cannot fire at any
   threshold. **The mulch mechanism explains the radar failure but not the NDVI failure.** Both are
   physical constraints, not parameter choices. A brightening-based rule may be possible but rests
   on 18 units and a confound that was not eliminated (Step 2c).
   **The verdict carries three independent failures, each a physical or structural constraint
   rather than a parameter choice:** (i) no usable imagery existed at peak inundation from either
   sensor; (ii) the imagery gates confirmed inundation rather than damage and missed 15 of 18
   visibly flooded fields; (iii) no rainfall threshold in any of four products separated flooded
   from dry fields, because the water came from a levee failure rather than from rain on the field.
   The third finding means **this event is the wrong test case for a rainfall index and the right
   test case for a river stage trigger** — state that as a design recommendation, not as a negative
   result.
   Report as a positive, reusable result that the mulch effect is itself measurable and
   crop-specific, stating both measured ratios and not conflating them (corrected 2026-09-16):
   before any flooding, in the same acquisitions, **50.4% of strawberry fields read as majority
   water-like in VH against 21.2% of neighbouring lettuce fields, a factor of 2.4**, and
   separately the **median VH water-like fraction is 0.503 against 0.115, a factor of 4.4**. That
   is useful to anyone attempting SAR-based monitoring of mulched specialty crops, independent of
   insurance.

No adjectives about how promising this is. Numbers and their sources.

## 9. Repo layout

```
CLAUDE.md               this file
SPEC_CHANGELOG.md       any change to scope, dated, one line each
requirements.txt        pinned package versions
data/raw/               downloaded inputs, never modified
data/derived/           outputs of notebooks
docs/
  ground_truth_aggregate.md   aggregate loss figures used for sanity checks
notebooks/
  01_units.ipynb
  01b_dwr_check.ipynb   DWR vs CDL comparison (report only)
  01c_optical_flood_reference.ipynb
  02_s1_flood.ipynb
  02b_mulch_confound.ipynb
  02c_confound_tests.ipynb
  03b_reference_units.ipynb
  03_s2_ndvi.ipynb
  04_rain.ipynb
  05_truth.ipynb
  06_triggers.ipynb
  common.py, maps.py, cdl.py, dwr.py, download_dwr_crop_mapping.py   shared helpers
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
