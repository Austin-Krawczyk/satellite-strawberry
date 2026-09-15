"""DWR / Land IQ Statewide Crop Mapping helpers: load fields and place strawberries (T20)
in the water-year crop sequence. Definitions follow the DWR metadata; see 01b_dwr_check."""
import warnings

import numpy as np
import pandas as pd
import pyogrio

from common import GRID_CRS, RAW

DWR_DIR = RAW / "dwr_crop_mapping"
FILES = {2022: ("i15_crop_mapping_2022.gdb.zip", "i15_Crop_Mapping_2022"),
         2023: ("i15_crop_mapping_2023_final.gdb.zip", "i15_Crop_Mapping_2023")}
T20 = "T20"
SLOTS = [f"CROPTYP{i}" for i in range(1, 5)]
ADOYS = [f"ADOY{i}" for i in range(1, 5)]
SEQUENCES = {
    "A": "strawberries the only crop of the water year",
    "B": "strawberries first, then another crop",
    "C": "strawberries planted after another crop",
}


def adoy_to_date(v, wy):
    """DWR Adjusted Day Of Year -> date. For WY2023: -92 = 1 Oct 2022, -1 = 31 Dec 2022,
    1 = 1 Jan 2023, 273 = 30 Sep 2023."""
    if pd.isna(v):
        return pd.NaT
    jan1 = pd.Timestamp(f"{wy}-01-01")
    return jan1 + pd.Timedelta(days=int(v) - 1) if v > 0 else jan1 + pd.Timedelta(days=int(v))


def load_fields(year, counties):
    """All DWR fields whose centroid county (DWR `COUNTY`) is in `counties`, in GRID_CRS."""
    zf, lyr = FILES[year]
    cols = ["UniqueID", "COUNTY", "MULTIUSE", "ACRES", "MAIN_CROP", "MAIN_CROP_DATE"] + SLOTS + ADOYS
    where = "COUNTY IN (%s)" % ", ".join(f"'{c}'" for c in counties)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message=".*Measured.*")
        g = pyogrio.read_dataframe(DWR_DIR / zf, layer=lyr, where=where, columns=cols)
    return g.set_geometry(g.geometry.force_2d()).to_crs(GRID_CRS)


def strawberry_sequences(g, wy):
    """T20 fields with their place in the crop sequence and the T20 peak-greenness date.

    sequence A: T20 is the only crop; B: T20 is the first crop and another follows;
    C: another crop comes before T20. An unclassified-fallow slot ("X") counts as a slot.
    """
    t = g[g[SLOTS].eq(T20).any(axis=1)].copy()
    filled = t[SLOTS].apply(lambda c: c.notna() & c.astype(str).str.strip("*").ne(""))
    t["n_crops"] = filled.sum(axis=1)
    t["t20_slot"] = t[SLOTS].eq(T20).to_numpy().argmax(axis=1) + 1
    first = filled.to_numpy().argmax(axis=1) + 1
    t["sequence"] = np.select([t.n_crops == 1, t.t20_slot == first, t.t20_slot > first],
                              ["A", "B", "C"], default="?")
    t["t20_peak_adoy"] = [r[f"ADOY{k}"] for k, (_, r) in zip(t.t20_slot, t.iterrows())]
    t["t20_peak_date"] = [adoy_to_date(v, wy) for v in t.t20_peak_adoy]

    before, after, after_adoy, seq = [], [], [], []
    for (idx, r), k in zip(t.iterrows(), t.t20_slot):
        used = [j for j in range(1, 5) if filled.loc[idx, f"CROPTYP{j}"]]
        earlier, later = [j for j in used if j < k], [j for j in used if j > k]
        before.append(r[f"CROPTYP{earlier[-1]}"] if earlier else "")
        after.append(r[f"CROPTYP{later[0]}"] if later else "")
        after_adoy.append(r[f"ADOY{later[0]}"] if later else np.nan)
        seq.append(" > ".join(str(r[f"CROPTYP{j}"]) for j in used))
    t["crop_before"], t["crop_after"], t["crop_sequence"] = before, after, seq
    t["crop_after_peak_date"] = [adoy_to_date(v, wy) for v in after_adoy]
    return t
