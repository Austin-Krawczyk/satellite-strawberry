# Spec changelog

Any change to scope in `CLAUDE.md`, dated, one line each.

- 2026-09-15 — Spec created.
- 2026-09-15 — §5 PRISM: `OREGONSTATE/PRISM/AN81d` → `OREGONSTATE/PRISM/ANd`. AN81d is deprecated, last image 2020-12-30, no 2023 data; ANd has the same `ppt` band and 0.0417° grid and covers both 2023 windows. Approved by user.
- 2026-09-15 — §6 Step 1 unit rule, provisional: default changed from "≥ 60% strawberry in both CDL 2022 and 2023" to "≥ 60% in CDL 2023". The both-years rule was meant to filter crop rotation but is filtering CDL 2022 misclassification: of pixels CDL 2023 labels Strawberries, CDL 2022 labels 32% Shrubland and 16% Grass/Pasture, which is not plausible rotation on intensively farmed coastal land; forward agreement (CDL 2022 strawberry → 2023 strawberry) is 90.5%, and only 2 cells were ≥ 60% strawberry in 2022 but not 2023, so real rotation is low. The 15-unit both-years set is kept as a sensitivity check to report in the exhibit. Final rule to be chosen once the user supplies the March 2023 flood extent reference, from unit counts inside and outside the footprint under both rules. Approved by user.
- 2026-09-15 — Validation note on the strawberry-field definition: CDL 2023 class 221 in Monterey + Santa Cruz = 51,124 pixels ≈ 11,368 acres, about 89% of the California Strawberry Commission's 12,728-acre projection for the Watsonville/Salinas district (figure supplied by user). The district also includes some Santa Clara and San Benito County acreage that the two-county filter excludes.
