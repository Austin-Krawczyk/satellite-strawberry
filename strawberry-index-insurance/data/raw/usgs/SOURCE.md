# USGS streamflow gauges — provenance

Service: https://waterservices.usgs.gov/nwis/dv/ (daily values)
Retrieved (UTC): 2026-09-16
Request: sites 11159000, 11159500, 11152500; 2023-01-01 to 2023-03-31; parameters 00060
(discharge, cubic feet per second) and 00065 (gage height, feet); statistics 00001 (max)
and 00003 (mean). `.rdb` is the raw service response; the `.csv` is that same response
reshaped long at download time.

| Site | Name | Why |
|---|---|---|
| 11159000 | Pajaro River at Chittenden | Named in the spec; upstream of the breach reach |
| 11159500 | Pajaro River at Watsonville | Gauge closest to the breach reach |
| 11152500 | Salinas River near Spreckels | Downstream Salinas gauge nearest the strawberry area |

Nothing here may be modified (CLAUDE.md §11). January values are context only; the event
window is March.
