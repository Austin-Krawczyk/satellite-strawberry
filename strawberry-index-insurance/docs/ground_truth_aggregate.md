# Aggregate validation figures

Supplied by the project owner on 2026-09-15 for sanity-checking totals. These are
**aggregate** figures, not per-unit ground truth, and they have not been re-checked
against the original documents here; the source is named for each.

**The January and March 2023 events are kept strictly separate.** The analysis event
window is March. The January figures are context only.

## March 2023 (the event)

| Figure | Source |
|---|---|
| ~8,736 acres of crops destroyed or unable to be planted due to March flooding, of which an estimated **1,919 acres of strawberries** with **$160 million** in losses. Half those acres were newly impacted and not in the January survey. | Monterey County Agricultural Commissioner, second survey, released 2023-05-12 |
| Roughly one fifth of strawberry farms in the Watsonville and Salinas areas flooded. | Industry estimates after the breach |

## January 2023 (context only, not the event)

| Figure | Source |
|---|---|
| 15,705 acres damaged, $336 million, mostly southern Monterey County. Combined winter total ≈ 20,073 acres and $600 million. | Monterey County Agricultural Commissioner, first survey, January 2023 |
| 537 acres around the Pajaro River in Santa Cruz and north Monterey County; 467 acres on the Salinas River in Monterey County. | California Strawberry Commission, January 2023 preliminary |

## How these are used

- Step 2 compares flooded unit acreage against the 1,919-acre March strawberry figure,
  and the Sentinel-1 mask against the Step 1c optical mask, in both directions. Neither
  is treated as truth (CLAUDE.md §6 step 2, §8).
- County-level totals cover all crops unless stated, and county boundaries differ from
  the study area's two-county filter, so treat comparisons as order-of-magnitude checks.
