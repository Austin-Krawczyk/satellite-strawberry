"""Shared constants for the notebooks. Values come from CLAUDE.md §2, §5 and §6.

Change a dataset ID here only together with a SPEC_CHANGELOG.md entry.
"""
from pathlib import Path

EE_PROJECT = "cropczyk"

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
DERIVED = ROOT / "data" / "derived"
FIGURES = ROOT / "figures"

# Study area (§2): Monterey, Santa Cruz
COUNTY_GEOIDS = ["06053", "06087"]

# Earth Engine datasets (§5)
COUNTIES = "TIGER/2018/Counties"
CDL = "USDA/NASS/CDL"
CDL_STRAWBERRY = 221
S1 = "COPERNICUS/S1_GRD"
S2 = "COPERNICUS/S2_SR_HARMONIZED"
S2_CLOUD = "GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED"
CLEAR_CS_CDF = 0.6          # pixel is clear if cs_cdf > 0.6
GSW = "JRC/GSW1_4/GlobalSurfaceWater"
PERMANENT_WATER = 50        # occurrence > 50 is permanent water
RAIN = {
    "cpc": ("NOAA/CPC/Precipitation", "precipitation"),
    "prism": ("OREGONSTATE/PRISM/ANd", "ppt"),
    "daymet": ("NASA/ORNL/DAYMET_V4", "prcp"),
    "imerg": ("NASA/GPM_L3/IMERG_V07", "precipitation"),
}

# Analysis units (§6 step 1): 250 m cells in California Albers, grid origin at 0,0
GRID_CRS = "EPSG:3310"
CELL_M = 250
CDL_YEARS = (2022, 2023)
MIN_STRAWBERRY_FRAC = 0.6
