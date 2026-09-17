# RMA Summary of Business, Cause of Loss — provenance

Publisher: USDA Risk Management Agency. Public data files, no registration required.
Retrieved: 2026-09-17
Landing page: https://www.rma.usda.gov/tools-reports/summary-of-business/cause-loss

Pipe (|) delimited flat files, one per crop year, 30 unnamed fields. Column names are
taken from the record layout PDF below and are reproduced in `download_rma_col.py`;
the notebook imports them rather than guessing a position. Indemnity Amount is field 29,
Cause of Loss Description field 13, Month of Loss fields 14-15, Net Determined Quantity
field 28 (acres lost after the insured's share).

Zips are gitignored; this file is the record of what was downloaded.

| File | URL | SHA-256 | Bytes |
|---|---|---|---|
| `colsom_2015.zip` | https://pubfs-rma.fpac.usda.gov/pub/Web_Data_Files/Summary_of_Business/cause_of_loss/colsom_2015.zip | `dd7e1c6163455ca2c43dc4a0bb05e2d3c1c373fbf7958482139a6684f30db8e6` | 5,101,922 |
| `colsom_2016.zip` | https://pubfs-rma.fpac.usda.gov/pub/Web_Data_Files/Summary_of_Business/cause_of_loss/colsom_2016.zip | `cfd09f3e526cee8549d8a7f49481daf43331f09a6d25eaff33999f4f40260760` | 4,144,230 |
| `colsom_2017.zip` | https://pubfs-rma.fpac.usda.gov/pub/Web_Data_Files/Summary_of_Business/cause_of_loss/colsom_2017.zip | `f0b9bdd5b39fe585b3b810035191812e4b6d1209b25f51afc435667ad188f4ac` | 4,675,992 |
| `colsom_2018.zip` | https://pubfs-rma.fpac.usda.gov/pub/Web_Data_Files/Summary_of_Business/cause_of_loss/colsom_2018.zip | `b72ba7b52c1889ecce79a4d0069f690ce77a5ca8ae971d58e7f59501a3d5f666` | 4,995,844 |
| `colsom_2019.zip` | https://pubfs-rma.fpac.usda.gov/pub/Web_Data_Files/Summary_of_Business/cause_of_loss/colsom_2019.zip | `ef2c998836cff2f3ba20ead49d35357e4de4a52528f7561343513c8634cba32d` | 6,176,347 |
| `colsom_2020.zip` | https://pubfs-rma.fpac.usda.gov/pub/Web_Data_Files/Summary_of_Business/cause_of_loss/colsom_2020.zip | `9a88317fb6d31ce9f3bb2bdddfbf77ba587b0b3413441bbb0f9fc772da93d2ff` | 4,724,146 |
| `colsom_2021.zip` | https://pubfs-rma.fpac.usda.gov/pub/Web_Data_Files/Summary_of_Business/cause_of_loss/colsom_2021.zip | `bfa7697fccb246e954e03db81383292058045df18c798edeca40a8db95a38725` | 4,149,098 |
| `colsom_2022.zip` | https://pubfs-rma.fpac.usda.gov/pub/Web_Data_Files/Summary_of_Business/cause_of_loss/colsom_2022.zip | `39c9d65c2fa7bce6c42dc43b86a29ccb05049ec20ec632a91c884ea0c8c4c032` | 5,471,694 |
| `colsom_2023.zip` | https://pubfs-rma.fpac.usda.gov/pub/Web_Data_Files/Summary_of_Business/cause_of_loss/colsom_2023.zip | `fcf1c7117883e2250070288d450c20b4835d9a3dddbb1f7cbda9c0e46f776d01` | 5,820,368 |
| `colsom_2024.zip` | https://pubfs-rma.fpac.usda.gov/pub/Web_Data_Files/Summary_of_Business/cause_of_loss/colsom_2024.zip | `a5956e2c74305375fd193e9cc9d59adf3c5538fcfcb279a0b3bd8073c1a2f5d8` | 5,874,574 |
| `COL_record_layout.pdf` | https://pubfs-rma.fpac.usda.gov/pub/Web_Data_Files/Summary_of_Business/cause_of_loss/COL_Summary_of_Business_with_Month_All_Years.pdf | `16b0b979fbe8f66b162f0ff0fe80ef0cd244537d8533fb41b70982a889abba35` | 83,491 |
