# Satellite-confirmed rainfall index for California strawberries — summary

*Austin Krawczyk, UC Davis, 16 September 2026. Prepared for USDA RMA, Davis Regional Office,
and Agralytica. Full analysis in `EXHIBIT.md`.*

**What was tested.** The design under examination holds rainfall as the insurable event and uses
satellite imagery as a confirmation gate that blocks payment to fields showing no visible damage.
We tested it on the Pajaro River levee breach of 10–11 March 2023, in Monterey and Santa Cruz
counties, across 1,320 strawberry fields totalling 14,683 acres defined from the California DWR
crop map. The rainfall trigger was tested at 50, 75 and 100 mm across four precipitation products
spanning grid sizes from 1 km to 50 km. The imagery gate was tested as specified: a Sentinel-1
radar flood mask, or a Sentinel-2 NDVI drop. Because no field-level loss records exist for this
event, fields were classified as flooded or not flooded against an independent optical water
reference built from Sentinel-2 alone — never as lost or not lost. **That is the one caveat that
governs everything below: these results measure flood detection, not loss prediction.**

**What was found.** The design failed, for three independent reasons, none of which is a
threshold that could be retuned. First, no usable imagery existed when the water was at its
peak: there was no Sentinel-2 acquisition at all for 11–14 March, and no radar pass covering
the fields between 7 and 19 March. Second, the gate missed the fields it most needed to catch.
Of the 18 fields the reference places in standing water, the radar gate fired on 3 and the NDVI
gate on 3. Fifteen fields at 95–100% inundation carried a radar flooded fraction of exactly
zero, because plastic mulch is radar-dark and flooding therefore *raises* backscatter on these
beds rather than lowering it — the specified mask fires on a drop, and the radar gate fired on
all 3 fields where backscatter fell and none of the 15 where it rose. Third, no rainfall
threshold in any of the four products separated flooded fields from dry ones. At 50 mm all four
products pay every field in the study area; the coarse product most like RMA's existing Rainfall
Index takes only five distinct values across all 1,320 fields and assigns flooded and dry fields
the identical median total of 79.2 mm. The reason is physical: the water came from a levee
failure upstream, not from rain falling on the field.

**What it means for an index product.** The most transferable finding is not about strawberries.
What the imagery detected was standing water, and once the water drained the canopy looked
unchanged — the signal decays to 1 field in 18 within two weeks, and the event is invisible in
the crop's seasonal growth curve. The gate therefore confirmed *inundation*, which the weather
trigger already implies, rather than *damage*, which it never saw. A gate that only re-detects
the hazard adds verification cost without adding information about loss, and that holds for any
peril where the visible signal is the hazard itself rather than its effect on the crop. Against
this, the two designs fail in opposite directions rather than trading off usefully: rainfall
alone pays nearly every field or almost none, and adding the gate caps detection at 33% because
it finds only 6 of the 18 flooded fields on its own. A second practical finding: checked against fourteen CIMIS
ground stations, no one product proved more accurate than the others — their errors against the
stations are as large as their disagreement with each other, so the choice of rainfall product
cannot currently be settled by evidence and has to be fixed by convention and priced. The
constructive conclusion is that this event is the wrong test for a rainfall index and the right
test for a **river stage trigger** —
gauge stage is observed hourly, has a long record, and is causally upstream of the damage. One
reusable result came out of the failure: before any flooding, mulched strawberry beds read as
majority open water to radar about two and a half times as often as neighbouring lettuce fields,
which is worth knowing to anyone attempting radar monitoring of mulched specialty crops.
