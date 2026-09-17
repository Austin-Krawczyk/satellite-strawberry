# Satellite-confirmed rainfall index for California strawberries

### A feasibility exhibit on the Pajaro River levee breach, 10–11 March 2023

Prepared for USDA RMA, Davis Regional Office, and Agralytica.
Study area: Monterey (06053) and Santa Cruz (06087) counties, California.

*Analysis by Austin Krawczyk, UC Davis, 16–17 September 2026. Repository:
https://github.com/Austin-Krawczyk/CROPCZYK (private; access on request). All inputs are public
datasets except the aggregate loss figures in `docs/ground_truth_aggregate.md`, which were
supplied by the author and are used only as order-of-magnitude checks.*

Every figure in this exhibit was computed in the notebooks listed in §4, and every table names
its dataset, date window and unit count.

> **Stated at the front, because it governs how everything below should be read:** no
> field-level loss data exists for this event. Units can be classified as flooded or not
> flooded against an optical water reference built here; they cannot be classified as lost or
> not lost. Every four-cell table in this exhibit therefore measures **flood detection
> performance, not loss prediction**. Hits and misses are detections and failures to detect.
> The only loss figures available are county aggregates from a voluntary survey with no map.

---

## 1. Question and design principle

For California strawberries, does a rainfall trigger confirmed by satellite imagery separate
**fields that flooded from fields that did not**, better than a rainfall trigger alone? The
question the programme actually needs answered — whether such a trigger separates fields that
*lost crop* from fields that did not — **this analysis could not reach**, because no
field-level loss records exist for this event; it is the first thing more data would buy (§8).
The design under test holds rainfall as the insurable event and uses imagery only as a
confirmation gate that blocks payment to fields showing no visible damage; imagery is never the
loss meter, because rot, mould and internal fruit damage are invisible from orbit. The test
event is the Pajaro River levee breach of 10–11 March 2023, the largest recent flood loss to
California strawberries with a defined date and location. The units are 1,320 strawberry field
polygons totalling 14,683 acres, and the reference is an independent optical water mask built
from Sentinel-2 alone so that it does not restate the Sentinel-1 result it is used to judge.
The answer, developed in §5 and stated in §9, is that on this event the gate confirmed
inundation rather than damage, and that inundation was already implied by the weather trigger.

---

## 2. Data sources

Latency is given in the weakness column where it constrains operational use.

| Purpose | Dataset | Provider | Resolution | Years | Known weaknesses |
|---|---|---|---|---|---|
| Analysis units | DWR / Land IQ Statewide Crop Mapping WY2023 (`i15_crop_mapping_2023_final.gdb`) | CA DWR / Land IQ | field polygons | 2014– | Published 1–2 years in arrears. No strawberry-specific accuracy. WY2023 T20 acreage in the two counties is 132% of the Commission's district projection. Not ground truth. |
| Crop map comparison | `USDA/NASS/CDL` class 221 | USDA NASS | 30 m | 1997– | ~4-month latency. Only 32.6% of its 2023 strawberry area falls inside DWR T20 fields; 31.9% of its 2023 strawberry pixels were shrubland in 2022. |
| Flood detection | `COPERNICUS/S1_GRD` (IW, VV+VH) | ESA | 10 m | 2014– | ~1-day latency, but track-dependent coverage and 12-day revisit in 2023 (§5.4). Specular surfaces (plastic mulch) mimic open water. |
| Water reference, vegetation | `COPERNICUS/S2_SR_HARMONIZED` + `GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED` | ESA / Google | 10–20 m | 2017– | ~1-day latency; cloud is the binding constraint. No usable acquisition existed 11–14 March 2023 (§5.4). |
| Permanent water | `JRC/GSW1_4/GlobalSurfaceWater` (occurrence > 50) | EC JRC | 30 m | 1984–2021 | Static, pre-2022 baseline. |
| Rain, coarse (PRF-like grid) | `NOAA/CPC/Precipitation` | NOAA CPC | 0.5° (~50 km) | 1979– | ~1-day latency. Band is **0.1 mm/day**, not mm/day (§7). Takes 5 distinct values across all 1,320 fields. Resembles PRF in grid coarseness only, not in index design (§6). |
| Rain, 4 km | `OREGONSTATE/PRISM/ANd` | PRISM Group | 4 km | 1981– | Provisional to stable over months. `AN81d` is deprecated and ends 2020-12-30; `ANd` replaces it. |
| Rain, 1 km | `NASA/ORNL/DAYMET_V4` | NASA ORNL | 1 km | 1980–2023 | Annual release, ~1-year latency; not usable for in-season triggering. |
| Rain, satellite | `NASA/GPM_L3/IMERG_V07` | NASA | 0.1° | 2000– | Early run ~4 h, final ~3.5 months. Retrieval-based; lowest event totals of the four here. |
| Elevation | `USGS/3DEP/10m_collection` | USGS | 10 m | static | Replaces deprecated `USGS/3DEP/10m`. |
| River lines | `WWF/HydroSHEDS/v1/FreeFlowingRivers` | WWF | coarse | static | Global network; distances are approximate. |
| River stage and discharge | USGS sites 11159000, 11159500, 11152500 | USGS | point | 1939– | ~1-hour latency, the fastest input here. Three gauges only. |
| Insured loss history | RMA Summary of Business, Cause of Loss (`colsom_2015`–`colsom_2024`) | USDA RMA | county | 1989– | Published annually. **Insured** losses only, and only rows where a loss was paid: it shows neither insured acreage nor participation, so absence of records is not absence of loss (§5.6). |
| Rain, ground stations | CIMIS station `day-precip` (Web API) | CA DWR | point | 1982– | ~1-day latency. 14 reporting stations in and near the study area; none on a strawberry field, nearest 0.2 km from a unit (§5.3). Interface changed mid-2026 — see the reproducibility note below. |
| Counties | `TIGER/2018/Counties` | US Census | — | — | — |

**Reproducibility note on CIMIS.** The legacy CIMIS Web API (`/api/data` and `/api/station`,
with the app key passed as an `appKey` query parameter) was retired on **31 July 2026**. Requests
carrying that parameter are now rejected by the site firewall whatever the key's value, so an
attempt to replicate this step using the interface documented before that date will fail without
an informative error. The station data here came from the replacement,
`https://et.water.ca.gov/StationWeb/GetDataByStationNumber`, which sits behind Azure API
Management and takes the key as an `Ocp-Apim-Subscription-Key` HTTP header, never in a URL. The
station values themselves are unaffected; only the interface changed.

**Not obtained.** No
published inundation polygon for the breach could be found, and every ready-made flood product
for the event derives from Sentinel-1, so using one would have been circular; the reference was
therefore built from optical imagery here (§4, Step 1c).

---

## 3. Event and study area

The Pajaro River levee failed on the night of 10–11 March 2023, flooding the town of Pajaro
and farmland on both sides of the Monterey–Santa Cruz county line. At the Watsonville gauge
(USGS 11159500) the river crested at **32.10 ft and 12,800 cfs at 00:45 on 11 March**; at
Chittenden (11159000) at **29.11 ft and 13,200 cfs**. The Salinas River near Spreckels
(11152500) peaked separately at **26.89 ft and 23,300 cfs on 13 March**. Water reached these
fields because a structure gave way upstream — the distinction governs the whole design and
returns in §5.3 and §9.

Units are DWR WY2023 field polygons carrying strawberries (subclass T20) as the only crop of
the water year — **sequence A**: 1,320 fields, 14,683 acres, 939 in Monterey and 381 in Santa
Cruz, from 1,935 T20 fields in the two counties. The 611 sequence B fields (strawberries then
another crop, 7,489 acres) and 4 sequence C fields are carried in the deliverable table as
flagged non-units; no unit touches permanent water. The CDL-based definition used before
2026-09-15 yielded 127 cells at 250 m and ≥60% class 221, reported for comparison only.

The original design treated the Salinas Valley as a dry control. **That premise was revised on
2026-09-16** when the Step 1c reference showed the Salinas River corridor flooded as well: the
comparison is now flood-corridor fields against fields outside both corridors, in the same
counties, under the same storm and the same coarse rainfall grid. **Figure 1** shows the units
over a Sentinel-2 basemap with county lines and Pajaro town.

---

## 4. Method

**Step 1 — Units.** DWR WY2023 polygons, T20 in any of `CROPTYP1`–`CROPTYP4`, county by
centroid, permanent water excluded, classified into sequences A/B/C from the crop slots and
their `ADOY` peak-greenness dates; sequence A fields are the units.

**Step 1c — Optical flood reference.** Sentinel-2 masked with Cloud Score+ (`cs_cdf` > 0.6),
every acquisition from 11–25 March tabulated with its clear-pixel fraction (§5.4). Water mapped
on 15, 20 and 25 March as NDWI > 0 and MNDWI > 0 with MNDWI at least 0.2 above a 1 February –
8 March baseline, permanent water removed; the reference is their union, each polygon tagged
with the date first seen. **No Sentinel-1 data was used in this step.**

**Step 2 — Sentinel-1 flood mask.** Pre 1 February – 8 March, post 11–20 March, IW, VV and VH,
3×3 focal mean, flooded where the change is below −3 dB and the post value below −15 dB (VV;
−22 dB tested for VH). Tracks were scored by how many unit centroids fall inside each footprint
(§5.4); baseline wetness was measured before differencing, and the mask compared with the
optical reference in both directions.

**Steps 2b, 2c — Mulch and confounds.** Baseline water-like fraction across the units against
800 neighbouring lettuce (T30) and cole-crop (T4) fields in the same acquisitions; pre-to-post
change inside against outside the 15 March extent, for units with a clear view that day; then
pre-event backscatter against elevation, river distance and field size, the change comparison
repeated on 54 matched dry units, and the 19 March result compared with 31 March for persistence.

**Steps 3, 3b — Sentinel-2 vegetation change.** ΔNDVI = median NDVI over 20 March – 30 April
minus median over 1 February – 8 March, cloud-masked, with clear-observation counts per unit;
the sequence A assumption checked against February NDVI and the water-year trajectory; then the
18 reference units reported individually, with ΔNDVI recomputed over four tighter post windows
beside the spec default (§5.2).

**Step 4 — Rainfall,** four products, event totals 9–14 March at each unit centroid, the
4–16 January totals as context, and a threshold test at 50, 75 and 100 mm. **Step 5 — skipped:**
no field-level loss data exists, so `truth` cannot be assigned as lost or not lost, and the
Step 1c reference supplies flooded / not flooded instead.

**Step 6 — Trigger logic.** `truth` = flooded where at least 30% of the field lies inside the
15 March extent (18 units); not flooded where at most 5% does **and** at least half the field
was clear that day (719 units); the rest unknown and excluded. Rain trigger: event total > T for
T ∈ {50, 75, 100} mm per product. Image trigger: S1 flooded fraction > 0.3 **or** (ΔNDVI < −0.15
with ≥ 2 clear post observations). Dual: both. Output: `data/derived/units.csv`.

---

## 5. Results

### 5.1 The four-cell tables

18 flooded units, 719 not flooded, 583 unknown and excluded. **Figure 5.**

**Rain only**

| product > T | hit | miss | false alarm | correct reject | detection | false-alarm rate | units paid |
|---|---|---|---|---|---|---|---|
| cpc > 50 | 18 | 0 | 719 | 0 | 100% | 100% | 737 |
| cpc > 75 | 18 | 0 | 715 | 4 | 100% | 99% | 733 |
| cpc > 100 | 0 | 18 | 2 | 717 | 0% | 0% | 2 |
| prism > 50 | 18 | 0 | 719 | 0 | 100% | 100% | 737 |
| prism > 75 | 15 | 3 | 327 | 392 | 83% | 45% | 342 |
| prism > 100 | 1 | 17 | 93 | 626 | 6% | 13% | 94 |
| daymet > 50 | 18 | 0 | 719 | 0 | 100% | 100% | 737 |
| daymet > 75 | 15 | 3 | 265 | 454 | 83% | 37% | 280 |
| **daymet > 100** | **15** | **3** | **147** | **572** | **83%** | **20%** | **162** |
| imerg > 50 | 18 | 0 | 719 | 0 | 100% | 100% | 737 |
| imerg > 75 | 0 | 18 | 35 | 684 | 0% | 5% | 35 |
| imerg > 100 | 0 | 18 | 0 | 719 | 0% | 0% | 0 |

**Dual (rain and image)**

| product > T | hit | miss | false alarm | correct reject | detection | false-alarm rate | units paid |
|---|---|---|---|---|---|---|---|
| cpc > 50 | 6 | 12 | 9 | 710 | 33% | 1% | 15 |
| cpc > 75 | 6 | 12 | 9 | 710 | 33% | 1% | 15 |
| cpc > 100 | 0 | 18 | 0 | 719 | 0% | 0% | 0 |
| prism > 50 | 6 | 12 | 9 | 710 | 33% | 1% | 15 |
| prism > 75 | 3 | 15 | 2 | 717 | 17% | 0% | 5 |
| prism > 100 | 0 | 18 | 0 | 719 | 0% | 0% | 0 |
| daymet > 50 | 6 | 12 | 9 | 710 | 33% | 1% | 15 |
| daymet > 75 | 3 | 15 | 1 | 718 | 17% | 0% | 4 |
| daymet > 100 | 3 | 15 | 0 | 719 | 17% | 0% | 3 |
| imerg > 50 | 6 | 12 | 9 | 710 | 33% | 1% | 15 |
| imerg > 75 | 0 | 18 | 1 | 718 | 0% | 0% | 1 |
| imerg > 100 | 0 | 18 | 0 | 719 | 0% | 0% | 0 |

**Image only, no rain condition:** 6 hits, 12 misses, 9 false alarms, 710 correct rejects —
detection 33%, false alarm 1%, 15 units paid.

The **image gate caps the dual design**: it detects 6 of the 18 flooded units on its own, so no
rain threshold combined with it can exceed 33% detection. Added to the best rain-only
combination (daymet > 100 mm) it removes all 147 false alarms, and 12 of the 15 detections with
them. **Five of the twelve rain-only combinations have a false-alarm rate above 90%**: at 50 mm
every unit in the study area exceeds the threshold in all four products, so the trigger pays
every field, flooded or not. The two designs fail in opposite directions rather than trading
off along a curve.

### 5.2 Why the gate misses — the 18 reference units, in full

Every unit the reference places in standing water on 15 March, sorted by inundation.
`inund.` and `clear` are percentages of the field; `s1_vv` is the radar flooded fraction;
VV in dB; ΔNDVI over the spec default window.

| unit_id | acres | elev m | inund. | clear | s1_vv | pre_vv | post_vv | d_vv | pre_ndvi | post_ndvi | ΔNDVI | pre_n | post_n | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2717328 | 42.33 | 6.85 | 100 | 100 | 0.00 | −8.26 | −4.16 | +4.10 | 0.08 | 0.07 | −0.02 | 3.0 | 7.0 | none |
| 2726550 | 14.25 | 6.54 | 100 | 100 | 0.00 | −7.93 | −6.81 | +1.13 | 0.10 | 0.05 | −0.04 | 3.0 | 7.0 | none |
| 2726604 | 12.79 | 6.35 | 100 | 100 | 0.00 | −7.28 | −3.20 | +4.09 | 0.16 | 0.06 | −0.10 | 3.0 | 7.0 | none |
| 2726556 | 2.59 | 5.77 | 99 | 100 | 0.00 | −13.38 | −9.46 | +3.92 | 0.17 | 0.09 | −0.08 | 6.0 | 14.0 | none |
| 2726581 | 9.51 | 6.42 | 98 | 98 | 0.00 | −9.16 | −4.32 | +4.84 | 0.09 | 0.07 | −0.02 | 3.0 | 7.0 | none |
| 2725616 | 29.96 | 6.68 | 95 | 96 | 0.00 | −8.45 | −2.32 | +6.13 | 0.13 | 0.08 | −0.04 | 3.2 | 7.4 | none |
| 2700454 | 27.34 | 10.11 | 95 | 100 | 0.62 | −14.39 | −19.92 | −5.54 | 0.07 | 0.05 | −0.03 | 3.0 | 7.7 | radar |
| 2712306 | 22.50 | 7.50 | 92 | 100 | 0.00 | −7.93 | −2.93 | +5.01 | 0.11 | 0.05 | −0.06 | 2.8 | 7.0 | none |
| 2726589 | 2.07 | 2.44 | 91 | 100 | 0.00 | −10.60 | −8.77 | +1.84 | 0.34 | 0.18 | −0.15 | 6.0 | 14.0 | NDVI |
| 2726570 | 4.88 | 6.82 | 89 | 100 | 0.00 | −9.47 | −4.11 | +5.36 | 0.12 | 0.08 | −0.04 | 3.0 | 7.0 | none |
| 2726568 | 3.40 | 5.89 | 88 | 100 | 0.00 | −10.56 | −9.64 | +0.91 | 0.19 | 0.10 | −0.09 | 6.0 | 14.0 | none |
| 2726539 | 1.71 | 2.54 | 71 | 100 | 0.00 | −11.84 | −9.32 | +2.52 | 0.34 | 0.22 | −0.11 | 6.0 | 14.0 | none |
| 2726547 | 23.59 | 6.92 | 69 | 69 | 0.00 | −8.80 | −4.54 | +4.26 | 0.65 | 0.33 | −0.32 | 2.4 | 7.8 | NDVI |
| 2711919 | 9.64 | 3.71 | 66 | 97 | 0.37 | −12.28 | −14.28 | −2.01 | 0.09 | 0.08 | −0.01 | 6.0 | 14.0 | radar |
| 2725632 | 18.05 | 5.51 | 60 | 100 | 0.52 | −11.30 | −17.10 | −5.80 | 0.07 | 0.07 | −0.00 | 3.0 | 9.0 | radar |
| 2716751 | 31.37 | 6.78 | 52 | 52 | 0.00 | −7.16 | −3.24 | +3.92 | 0.20 | 0.14 | −0.05 | 2.6 | 7.0 | none |
| 2724052 | 10.90 | 12.82 | 49 | 100 | 0.00 | −10.95 | −10.63 | +0.32 | 0.10 | 0.11 | +0.01 | 2.0 | 7.8 | none |
| 2726662 | 3.49 | 9.13 | 31 | 100 | 0.06 | −11.92 | −11.64 | +0.27 | 0.60 | 0.45 | −0.15 | 3.0 | 7.1 | NDVI |

Gates fired: none 12, radar 3, NDVI 3. All 18 are in Monterey County. Six units at 95–100%
inundation carry a radar flooded fraction of **exactly 0.000**, with ΔNDVI between −0.105 and
−0.015 against a −0.15 trigger.

**The radar gate fired on all 3 units where VV fell and on none of the 15 where it rose.** That
one sentence explains the entire radar failure: the specified mask fires on a drop, and on
these fields backscatter went up.

**ΔNDVI by post window,** 18 reference units against 719 dry units:

| post window | median clear obs | reference median ΔNDVI | dry median ΔNDVI | reference units below −0.15 |
|---|---|---|---|---|
| spec default, 20 Mar – 30 Apr | 7.5 | −0.050 | +0.053 | 3 of 18 |
| 15 March only | 1.0 | −0.399 | +0.013 | 18 of 18 |
| 20 March only | 1.0 | −0.062 | +0.014 | 3 of 18 |
| 20–31 March | 2.0 | −0.038 | +0.030 | 2 of 18 |
| 25 March only | 1.0 | −0.037 | +0.036 | 1 of 18 |

**The 15 March row is not independent evidence and must never be quoted without this caveat:**
the reference units were *defined* by the 15 March water mask, and NDWI shares band B8 with
NDVI, so both fall when water covers a field. That row largely restates the reference
definition. The informative rows are the later ones — 3 of 18 on 20 March, 2 over 20–31 March,
1 on 25 March. The signal decays within days. Read together, these rows say that NDVI here
detected **standing water, not crop damage**: once the water drained, the canopy looked
unchanged. The March event is also invisible in the units' water-year NDVI trajectory, which
rises from 0.146 in October 2022 to a peak of 0.689 in August 2023 with no March disturbance.

**Does the gate look better on a larger flooded set?** The 18 reference units are 270 acres,
14% of the 1,919 acres the county reported lost, so it is fair to ask whether a more inclusive
definition — one that covers more of the county figure — flatters the gate. It does the
opposite:

| inclusion rule | units | acres | % of 1,919 ac | radar fires | NDVI fires | either | detection |
|---|---|---|---|---|---|---|---|
| ≥ 30% inundated (spec default) | 18 | 270 | 14.1% | 3 | 3 | 6 | **33%** |
| ≥ 10% inundated | 30 | 564 | 29.4% | 6 | 4 | 9 | 30% |
| any detected water (≥ 0.01%) | 54 | 1,123 | 58.5% | 6 | 4 | 9 | **17%** |

**Detection falls from 33% to 17% as the set widens**, because the units added by relaxing the
threshold are the partly flooded ones and the gate catches almost none of them — the absolute
count moves from 6 to 9 across a set three times the size. The mechanism reappears intact: on
the 54-unit set the radar gate fired on 6 of the 7 units where VV fell and **0 of the 47 where
it rose**. So the 33% on the reference set is the gate's **best case, not a threshold artefact**,
and the more of the county's reported loss the set covers, the worse the gate looks.

**Figure 2** — Sentinel-1 pre, post and mask. **Figure 3** — ΔNDVI map with the
clear-observation inset. Supplementary figures cover the mulch confound, the confound tests,
the reference units and the NDVI trajectory.

### 5.3 Rainfall: product disagreement is as large as the trigger choice

Event totals 9–14 March 2023 at the unit centroid (mm):

| product | reference median | reference min–max | dry median | difference | all units min–max |
|---|---|---|---|---|---|
| cpc | 79.2 | 79.2 – 79.2 | 79.2 | **0.0** | 67.3 – 143.3 |
| prism | 92.3 | 57.4 – 104.3 | 85.1 | 7.2 | 52.1 – 177.3 |
| daymet | 104.9 | 54.3 – 109.2 | 96.6 | 8.2 | 53.0 – 171.8 |
| imerg | 65.4 | 65.4 – 74.7 | 67.7 | −2.3 | 60.8 – 88.9 |

For the same field the four products disagree by a **median of 28.5 mm**, 57.3 mm at the 90th
percentile and 100.0 mm at most. That spread is comparable to the 25 mm spacing between the
tested thresholds, so **the choice of rainfall product moves the outcome as much as the choice
of trigger level.** That is a rating problem, independent of basis risk: two insurers using
different reanalyses would price and pay differently on identical fields. And the ground
network cannot referee the disagreement, as the station check below shows.

**CPC, whose grid is the closest of the four to the one PRF's Rainfall Index uses, takes only
five distinct values across all 1,320 fields** at its 0.5° (~50 km) cell size, and gives the reference units and the dry
units **the same median total, 79.2 mm against 79.2 mm**. At that grid size a PRF-style index
cannot distinguish a flooded field from its dry neighbour. Beside it, the best case across all
four products and three thresholds is **Daymet at 100 mm: 83% of reference units (15 of 18)
against 43% of dry units (556 of 1,288) — still paying 556 fields that never flooded.**
At 100 mm the products disagree among themselves about who is paid at all: cpc 2 units,
imerg 0, prism 373, daymet 578.

No threshold in the specified range separates flooded from dry units in any product, and the
reason is physical rather than statistical: the water on these fields came from a levee
failure upstream, not from rain falling on the field.

**Ground stations cannot say which product is right (Step 4b).** Fourteen CIMIS stations reported
over the event window, the nearest 0.2 km from a unit and one of them in Pajaro itself, though
none sits on a strawberry field. Sampling each product at each station's own coordinates:

| product | March: mean abs. error | March: mean abs. % | January: mean abs. error | January: mean abs. % |
|---|---|---|---|---|
| cpc | 25.4 mm | 45% | 91.2 mm | 102% |
| prism | 21.0 mm | 33% | **42.7 mm** | 65% |
| daymet | **20.0 mm** | 35% | 61.6 mm | 75% |
| imerg | 20.1 mm | 30% | 48.0 mm | 70% |

**No product is vindicated.** Over the event window the best (Daymet, 20.0 mm) and the worst
(CPC, 25.4 mm) differ by a factor of 1.3, and the four products' mutual spread at those same
points is 25.2 mm — so **the station errors are as large as the disagreement they were meant to
adjudicate.** The ranking also flips between events: Daymet is closest in March, PRISM in
January. The 28.5 mm spread across products is therefore **not resolvable with available ground
data**, which is a rating problem in its own right: the input uncertainty cannot be priced away
by picking the right product, because the ground network cannot say which one is right.

**The stations are the strongest evidence in this exhibit for the grid argument**, because
they are measurements rather than products disagreeing with each other. Over the event window
they range from **33.8 mm at Arroyo Seco to 137.3 mm at De Laveaga — a factor of four across
the study area** — while CPC returns four distinct values across all fourteen and **the same
79.2 mm at eight of them, including both Pajaro and Salinas**, which are 29 km apart and, on
the ground, 98.1 mm and 58.5 mm respectively.

**That spread is real rainfall structure, not station noise.** Mean absolute difference between
station pairs rises with separation — **13.7 mm for pairs within 15 km against 42.0 mm beyond
50 km, a factor of 3.1** — which is what spatially coherent rainfall looks like and not what
instrument or siting error looks like. Neighbouring stations mostly agree closely: Arroyo Seco
and Soledad II differ by 3.1 mm at 13 km, the two Salinas stations by 3.4 mm at 17 km, Gilroy
and Pajaro by 0.9 mm at 22 km. The exception is instructive — De Laveaga sits 55.3 mm above
Watsonville West II just 18 km away, on the flank of the Santa Cruz Mountains. The gradient is
not a simple function of terrain proxies at this sample size (rank correlation with elevation
+0.20, with distance to the coast +0.05), so it is storm structure rather than a standing
orographic pattern. **A denser network in the producing districts would therefore resolve real
structure rather than chase noise** — which is what makes this a resolution problem.

At annual scale, across 28 station-years at all fourteen stations, the pattern is **regression
to the cell mean rather than a coastal bias**: the coarse products under-read the wettest sites
and over-read the driest. CPC gives 53% of the station total at De Laveaga in 2022 but 214% at
Arroyo Seco and 291% there in 2023; its median across all station-years is 123%, and it reads
more than 15% low at only 5 of 28. The tendency runs with distance inland, not seaward
(rank correlation of CPC against distance to the coast **+0.33**). This also confirms the CPC
units correction of §7 independently: at the corrected 0.1 mm/day scaling CPC's annual totals
sit in the right range, where the uncorrected reading would have been ten times the station's.

**Figure 4** — event totals, four products, shared colour scale. A supplementary figure shows
each product against each station for both windows.

### 5.4 Sensor availability — a finding, not a caveat

**Optical.** Clear-pixel fraction (Cloud Score+ `cs_cdf` > 0.6), 11–25 March 2023:

| date | days after peak | scenes | study area | the two valleys | lower Pajaro Valley |
|---|---|---|---|---|---|
| 12 Mar | 1 | 5 | 2.2% | **0.0%** | **0.0%** |
| 15 Mar | 4 | 7 | 74.9% | 66.2% | 45.4% |
| 17 Mar | 6 | 5 | 34.5% | **0.0%** | **0.0%** |
| 20 Mar | 9 | 7 | 20.7% | 50.1% | 98.9% |
| 22 Mar | 11 | 5 | 0.1% | **0.0%** | **0.0%** |
| 25 Mar | 14 | 7 | 90.7% | 100.0% | 100.0% |

**No Sentinel-2 acquisition exists at all for 11–14 March**, when water was at its peak, and
the valleys were 0% clear on 12, 17 and 22 March. The first usable optical view of the flood is
four days late.

**Radar.** Five Sentinel-1 acquisitions between 1 February and 31 March cover ≥95% of the units
(11 and 23 February, 7, 19 and 31 March). The **longest gap over the unit area is 12 days, and
the breach falls inside it**: the last usable pass before the event was 7 March and the first
after it was 19 March, eight days late. Three passes did fall in the event window and none was
usable: descending orbit 115 on 12 March covers **7 of 1,320 units**, ascending 137 on 14 March
covers 6, and descending 144 on 14 March covers none. Choosing a track by date rather than by
coverage would have produced a flood mask over the wrong ground.

Every 2023 scene over this area came from **Sentinel-1A alone**. Sentinel-1B failed in December
2021 and was retired in August 2022, cutting per-track revisit from 6 days to 12; Sentinel-1C
launched in December 2024 and appears in the collection from 2025 (157 scenes in 2025, 120 by
this date in 2026). **A product designed today faces a materially better radar coverage regime
than this event did** — but not a better optical one, because cloud at a flood peak is weather,
not constellation design.

Together these are the operational constraint on any imagery-confirmed trigger: at peak
inundation, the state the gate is supposed to verify, **neither sensor could see the fields.**

### 5.5 The mulch mechanism, and what it is worth on its own

Before any flooding, in the 1 February – 8 March baseline, the median unit is **50.3% water-like
in VH**, and 1,068 of 1,320 units are more than 10% water-like in VH. Against 800 neighbouring
fields measured in the same acquisitions:

| crop | VH median water-like fraction | share of fields >50% water-like (VH) | VV median | share >50% (VV) |
|---|---|---|---|---|
| T20 strawberries (units, n = 1,320) | 0.503 | 50.4% | 0.035 | 14.3% |
| T30 lettuce / leafy greens (n = 400) | 0.115 | 21.2% | 0.000 | 2.2% |
| T4 cole crops (n = 400) | 0.199 | 32.0% | 0.000 | 3.0% |

Strawberry fields carry **4.4 times** the median VH water-like fraction of neighbouring lettuce
and are **2.4 times** as likely to read as majority open water, in the same passes. Plastic
mulch is specular at C-band and reads as open water before any water is present — a reusable,
crop-specific result for anyone attempting SAR monitoring of mulched specialty crops.

Its consequence here is that flooding **raises** backscatter on these beds rather than lowering
it. Restricted to units with a clear optical view on 15 March, the flooded group's VV change is
+3.22 dB against +0.56 dB for dry units — a 2.66 dB difference in the *wrong* direction for the
specified mask, rank separation 0.72 (0.5 is chance). The specified rule cannot fire on mulched
strawberry beds at any threshold; that is the mask definition failing, not a tuning problem.

A brightening-based rule is a lead, not a detector, and it was tested rather than assumed.
Position is a live confound — the flooded units sit lower and were already brighter before the
event — but it does not account for the change: against 54 dry units matched on elevation and
river distance the pre-event separation falls from 0.77 to 0.68 while the **change** separation
holds at 0.74, and the difference persists to the 31 March pass (+1.64 dB, 62% retained,
separation 0.79), consistent with a lasting surface change rather than transient standing water.
That rests on 18 units in one event with a confound reduced but not eliminated.

### 5.6 Insured loss history: there is almost none (Figure 6)

Across crop years 2015–2024, the entire federal cause-of-loss record for strawberries in these
two counties is **two rows**. Both are Monterey, both are March 2023, both are coded **Flood**,
and together they net **\$497,559** against 80.4 determined acres. **Santa Cruz County has no
strawberry loss record at all in ten years.** Statewide over the same decade there are five
strawberry rows: these two, one Ventura insect loss in 2015, and two small Ventura
excess-moisture rows in 2023.

**So March 2023 is not an outlier within a distribution — it is very nearly the whole
distribution**, and the reason is exposure rather than weather. The county agricultural
commissioner put March 2023 strawberry losses at 1,919 acres and \$160 million; the indemnity
record for the same crop, counties and event is \$497,559, a gap of roughly 320×. Strawberries
account for **0.51%** of insured loss in these counties over the decade (\$497,559 of \$97.7
million), against grapes at \$73.1 million. The cause-of-loss file lists only rows where a loss
was paid, so it cannot measure participation directly — but a peril that destroyed 1,919 acres
while generating two claims is not a peril the federal book is currently carrying.

**Three explanations fit that gap and this data cannot choose between them:** growers here may
largely not buy the coverage, which would be consistent with the low uptake in the strawberry
programme that RMA's Davis office has described; losses may have fallen below deductibles on the
policies that do exist; or they may have been indemnified under other plans or crop codes and so
not appear under Strawberries. Nothing in the cause-of-loss file distinguishes these, and the
choice matters for product design, so it is stated as an open question rather than resolved.

For the wider picture, excess moisture and flood across **all** commodities in these counties
total \$4.81 million over ten years, **4.9%** of insured loss, behind fire (\$35.2 million) and
heat (\$19.0 million). 2023 is the peak wet year at \$2.99 million, 20.0% of that year's total.

Two things follow for the product question. The absence of a loss history is **an argument for
building something rather than against it** — it is what a protection gap looks like, and it is
presumably why RMA is asking. But it also means **there is no insured loss experience in these
counties to rate a strawberry flood product against**, so rating would have to lean on other
districts, other crops, or non-insurance loss records (§8).

**Figure 6** — insured cause-of-loss experience, both counties, 2015–2024.

---

## 6. Basis risk

Stated as detection error against the Step 1c optical reference, **not** as loss outcomes.

| design | detection rate (flooded units paid) | false-alarm rate (dry units paid) | units paid of 737 |
|---|---|---|---|
| Rain only, best (daymet > 100 mm) | 83% | 20% | 162 |
| Rain only, CPC > 75 mm (CPC grid) | 100% | 99% | 733 |
| Dual, best (any product > 50 mm) | 33% | 1% | 15 |
| Image only | 33% | 1% | 15 |

**The CPC row is not a simulation of PRF.** PRF indexes rainfall relative to a long-term
average for a grid area rather than against an absolute millimetre threshold, and it pays on a
shortfall against that average rather than on an excess. What the row shows is the *resolution*
problem PRF's grid would inherit — at a 0.5° cell a flooded field and its dry neighbour are the
same pixel — not how PRF itself would have performed on this event.

The miss rate of the dual design is **67%** — two of every three fields the reference places in
standing water receive nothing. The rain-only design's false-alarm rate runs from 0% to 100%
across the twelve combinations without ever occupying a useful middle: the best of them still
pays 147 of 719 dry units in the tables, and 556 of 1,288 dry units across the full unit set.
No design tested here is rateable on these numbers, and because `truth` is inundation rather
than loss, even the best of them would need re-measuring against loss records before its basis
risk could be quoted to a grower.

---

## 7. Limitations

**No field-level loss data.** Units are flooded or not flooded, never lost or not lost. The
18 reference units total **270 acres, about 14% of the 1,919 acres** the county reported lost;
the gap is accounted for by cloud (571 of the 1,320 units, 30% of unit acreage, had no clear
optical view on 15 March, so they could not be classified either way), by the 30% inundation
threshold for inclusion (relaxing it to any detected water raises the set to 54 units and
1,123 acres, 58% of the county figure — on which the gate does *worse*, not better, §5.2), and
by the 615 sequence B and C fields, 7,536 acres,
that sit outside the sequence A unit set entirely. The
1,919-acre March strawberry figure (Monterey County Agricultural Commissioner, 2023-05-12) is a
county aggregate from a voluntary survey with no map, and the "roughly one fifth of farms"
figure is an industry estimate. The January 2023 atmospheric-river losses (15,705 acres) are
kept strictly separate from the March event throughout.

**The reference is a water mask built here, not a surveyed extent.** Its first clear view is
four days after the peak, so it under-counts flooded area — which biases *against* this method,
not for it. Its nested extents are 3,729 acres seen on 15 March, 1,426 added by 20 March (33%
of which was cloud-hidden earlier) and 1,034 added by 25 March (9.8% cloud-hidden), 6,189 acres
in union; later additions are as likely to be long-standing water or irrigation as flood.
Analyst choices move it substantially: raising the index minimum from 0.0 to 0.1 cuts mapped
area by about a third (to 0.66× at the default change threshold), while moving the MNDWI change
threshold between 0.15 and 0.25 moves it about 5% (1.05× to 0.95×). Minimum polygon size moves
it from 5,576 acres at 0.1 ha to 4,866 at 0.5 ha. Every agreement figure in §5 therefore carries
a sensitivity band, not a point value.

**Crop-map uncertainty propagates into every result, and is not resolved here.** Neither map is
ground truth. DWR defines the units and publishes no strawberry-specific accuracy; its WY2023
T20 acreage in the two counties is 132% of the Commission's district projection for a smaller
area — though DWR `ACRES` is whole-polygon area while the Commission figure is planted acreage,
which plausibly explains part of the gap. CDL 2023 places only 32.6% of its strawberry area
inside DWR T20 fields, and 31.9% of its 2023 strawberry pixels were shrubland in its own 2022
map. That sequence A fields had a crop in the ground in March 2023 is **agronomic reasoning, not
something either dataset states.** The February NDVI check could not confirm it: DWR class X
("not cropped") land in a wet winter carries weeds and reads *higher* (median 0.290) than
mulched strawberry beds (0.245), and lettuce reads 0.219, so February NDVI cannot separate a
planted strawberry field from idle ground. The water-year trajectory (0.146 in October rising
to 0.689 in August) is indirect support only: NDVI shows that something green grew on the
expected schedule, not what it was. The unit definition rests on DWR's classification plus a
visual check across a sample by the project owner, not on grower-confirmed field records —
which is why the 18 units the conclusion hinges on are reported individually in §5.2.

**Product-documentation risk, as a worked example.** The `NOAA/CPC/Precipitation` band is stored
in **0.1 mm/day**, not mm/day. Taken at face value it gave 792 mm over the six-day event and
5,053 mm for calendar 2021 at Pajaro, against 592 mm from PRISM for the same point and year; no
part of coastal California receives five metres of rain. Caught only by an independent
plausibility check, an unscaled CPC would have produced a confident, precise and entirely wrong
conclusion — that a coarse-grid index triggers easily on this event. Any index built on gridded
reanalysis needs unit verification against station data as a standing control. That check was
completed here, after this exhibit was first drafted, once a CIMIS key became available (§5.3):
the station record confirms the corrected scaling independently. **What the station check does
not do is validate the products over the fields.** Fourteen stations is a sparse network, none
of them sits on a strawberry field, and their errors against the products are as large as the
products' disagreement with each other, so absolute accuracy is established at a handful of
points and nowhere else.

**Other limits.** Cloud at the flood peak and 12-day radar revisit (§5.4). Mulch and bare-soil
confounds (§5.5). At 10–30 m a pixel spans several raised beds, so no result here is bed-level,
and internal fruit damage, rot and mould are invisible to both sensors at any resolution.
**A single event, in two counties, in one crop** — 18 reference units carry the conclusion, and
all of them are in Monterey County. Flood from a levee breach and damage from direct rainfall
are **different perils** that a real product would treat differently; this event tests the
former. Sentinel-1 area statistics exceeded Earth Engine's interactive limits, so mask acreages
are computed over a 325,548-acre Pajaro-to-northern-Salinas valley box and are never two-county
totals; per-unit fractions cover all 1,320 units. The river network used for distance is a
coarse global product. The RMA cause-of-loss record is now included (§5.6), but it carries its
own limit: it reports **insured** losses only, and only rows where a loss was paid, so it shows
neither insured acreage nor participation and its near-emptiness for strawberries cannot be
read as evidence that the peril is rare.

---

## 8. What it would take to be rateable

1. **Field-level loss records** — RMA claim records with field locations, or grower block-level
   reports. Until units can be labelled lost or not lost, no design here can be evaluated as an
   index, only as a flood detector. Note that the county-level record will not supply them
   either: it holds two strawberry rows in ten years (§5.6), so rating would have to borrow
   experience from other districts or from non-insurance loss records.
2. **More events and more counties** — the January 2023 atmospheric rivers, February 2017, and
   the Oxnard and Santa Maria districts. Eighteen reference units in one valley cannot support a
   rating parameter.
3. **A trigger matched to the peril:** for levee-breach flooding, river stage is observable
   within the hour, has a long record, and is causally upstream of the damage (§9).
4. **Imagery that arrives at the peril** — commercial 3 m optical with daily revisit, or tasked
   SAR — weighed against §9's finding that the gate confirmed inundation rather than damage.
5. **A way to choose among rainfall products that the ground network can support.** Step 4b
   shows the present network cannot: station errors are as large as the products' mutual
   disagreement and the ranking flips between events (§5.3). A denser gauge network in the
   producing districts is worth building, because the station spread is spatially coherent and
   would resolve real structure; until it exists, a documented convention should fix the product
   by rule and price the residual uncertainty rather than pretend it away.

---

## 9. Verdict against the kill criteria

**The specified design — a rainfall trigger confirmed by a radar flood mask — did not work on
California strawberries for this event.** Three independent failures, each a physical or
structural constraint rather than a parameter choice:

**1. The design-level failure: the imagery gate confirmed inundation, not damage.** What the
imagery detected was standing water. Once the water drained, the canopy looked unchanged — the
NDVI signal decays to 3 of 18 units by 20 March and 1 of 18 by 25 March (§5.2), and the March
event does not appear in the crop's seasonal trajectory at all. **Inundation is already implied
by the weather trigger.** A gate that only re-detects it adds verification cost without adding
information about loss. Within this event it holds regardless of timing, threshold or sensor.
**Whether it generalises is a proposition worth testing, not a result established here:** it
rests on one peril, one crop and one event, and the mechanism — a hazard whose visible signature
is the hazard itself rather than its effect on the crop — is plausible but untested elsewhere.
It would be **confirmed** by finding the same decay in other perils of that shape, where the
visible signature passes with the hazard while the damage persists: brief inundation of other
row crops, hail on a crop that regrows, wind lodging that stands back up. It would be
**refuted** by a peril where an imagery gate adds detection over the weather trigger *after* the
hazard has passed. That comparison needs only loss records and two or three events per peril,
and it is the cheapest next test in this whole programme.

**2. The measurement-level failure: the gate misses the fields it most needs to catch.** Of the
18 units the reference places in standing water on 15 March, the radar gate fires on 3, the
NDVI gate on 3, and either on 6. Fifteen units at 95–100% inundation carry a radar flooded
fraction of exactly 0.000 and NDVI changes of −0.02 to −0.11 against a −0.15 trigger (§5.2, full
table). **That 33% is the gate's best case, not an artefact of a strict inclusion rule:** widen
the flooded set to any detected water — 54 units, 58% of the county's reported acreage — and
detection falls to 17% (§5.2). The mechanism is mulch: **the radar gate fired on all 3 units where VV fell and on none
of the 15 where it rose.** Plastic mulch is radar-dark, so flooding raises backscatter rather
than lowering it, and the specified mask cannot fire at any threshold. The mulch mechanism
explains the radar failure **but not the NDVI failure**, which is the decay described above. The
`18 of 18` figure from the 15 March window is not independent evidence and must not be quoted
without the caveat in §5.2.

**3. The trigger-level failure: no rainfall threshold separated flooded from dry fields, in any
of four products.** At 50 mm all four pay every field in the study area; at 100 mm the best
product detects 83% of reference units while still paying 556 dry ones, and the four products
disagree about who is paid at all (2, 0, 373, 578 units). CPC, on the coarsest grid, assigns
reference and dry units the identical median total of 79.2 mm — **and ground measurement says
that is a resolution failure, not a modelling quibble. Fourteen CIMIS stations recorded between
33.8 mm and 137.3 mm across the study area over the same six days, a factor of four, while CPC
returned the same 79.2 mm at eight of them, Pajaro and Salinas included.** The station spread is
spatially coherent — pairs within 15 km differ by 13.7 mm on average against 42.0 mm beyond
50 km — so the variation the coarse grid erases is real rainfall, measured on the ground, and
not instrument noise (§5.3). **The water itself came from a levee failure, not from rain on the
field.** The Pajaro crested at 32.10 ft at
Watsonville at 00:45 on 11 March; no amount of rainfall measured over a field explains which
side of a failed levee it sat on.

**The compact form of the Step 6 result:** the two designs fail in opposite directions rather
than trading off along a curve, and the imagery gate caps the dual design at 33% detection
regardless of rain threshold, because it detects 6 of the 18 flooded units on its own.

**This third finding is a design recommendation, not a negative result.** It means this event is
the **wrong test case for a rainfall index and the right test case for a river stage trigger**:
stage at USGS 11159000 and 11159500 is observed hourly, has a long record, is causally upstream
of the damage, and would have fired unambiguously and on time. A strawberry flood product for
the Pajaro and Salinas corridors should be indexed on river stage, with rainfall reserved for
the separate peril of direct rain damage, which this event does not test.

**Against §4's kill criteria.** Rainfall alone does *not* already discriminate flooded from
unflooded units well, so the first criterion is not what failed — but the gate does not rescue
it, and caps detection at 33%. Sentinel-1 and Sentinel-2 could **not** resolve flooded
strawberry beds at usable accuracy in this event, for reasons that are physical (mulch, cloud,
revisit) rather than tunable; on that criterion the design should pivot to farmer photo
verification, or to a gauge-based trigger that needs no gate. And ground truth could **not** be
established at the field level, so the four-cell tables are flood detection performance and
nothing more.

**On whether the peril is worth indexing at all.** The insured record cannot say it is
recurring: two loss records in ten years, both from this event (§5.6). But that near-emptiness
measures exposure, not weather — 1,919 acres were reported lost against \$497,559 of indemnity —
so it reads as a protection gap rather than as evidence the peril is rare. It does mean any
product here would be rated without local loss experience.

**One positive, reusable result.** The mulch effect is itself measurable and crop-specific:
strawberry fields carry 4.4 times the median VH water-like fraction of neighbouring lettuce and
are 2.4 times as likely to read as majority open water, before any flooding, in the same
acquisitions (§5.5). That is useful to anyone attempting SAR-based monitoring of mulched
specialty crops, independent of insurance. The brightening response to flooding is a lead worth
testing on more events; on 18 units with a confound reduced but not eliminated, it is not a
detector.

---

*Reproduction: `notebooks/01_units` through `06_triggers`, run top to bottom against Earth
Engine project `cropczyk`. Per-unit values in `data/derived/units.csv` (1,935 rows: 1,320 units
and 615 flagged sequence B/C fields, 38 columns). Scope changes are dated in `SPEC_CHANGELOG.md`.*
