"""Sentinel-2 optical water detection (CLAUDE.md §6 step 1c).

Shared by 01c_optical_flood_reference (which builds the reference) and 02_s1_flood (which
compares the radar mask against it), so both use one definition. No Sentinel-1 data here.
"""
import ee

from common import CLEAR_CS_CDF, GSW, PERMANENT_WATER, S2, S2_CLOUD

DATES = ["2023-03-15", "2023-03-20", "2023-03-25"]
PRE_WINDOW = ("2023-02-01", "2023-03-09")   # 1 Feb - 8 Mar 2023 inclusive
NDWI_MIN = 0.0        # default index minimum; 0.1 is the sensitivity variant
MNDWI_MIN = 0.0
D_MNDWI_MIN = 0.2     # minimum MNDWI rise over the pre-event baseline


def clear_s2(region, start, end):
    """Sentinel-2 SR over `region`, Cloud Score+ linked, cloudy pixels masked."""
    return (ee.ImageCollection(S2).filterBounds(region).filterDate(start, end)
            .linkCollection(ee.ImageCollection(S2_CLOUD), ["cs_cdf"])
            .map(lambda im: im.updateMask(im.select("cs_cdf").gt(CLEAR_CS_CDF))))


def indices(img):
    """NDWI = (B3 - B8)/(B3 + B8) and MNDWI = (B3 - B11)/(B3 + B11)."""
    return (img.normalizedDifference(["B3", "B8"]).rename("ndwi")
            .addBands(img.normalizedDifference(["B3", "B11"]).rename("mndwi")))


def baseline(region, window=PRE_WINDOW):
    return indices(clear_s2(region, *window).median())


def permanent_water():
    return ee.Image(GSW).select("occurrence").unmask(0).gt(PERMANENT_WATER)


def water_on(region, date, pre=None, idx_min=NDWI_MIN, d_min=D_MNDWI_MIN):
    """0/1 standing-water mask for one date: both indices above `idx_min`, MNDWI risen by
    more than `d_min` over the pre-event baseline, permanent water removed."""
    pre = baseline(region) if pre is None else pre
    end = ee.Date(date).advance(1, "day").format("YYYY-MM-dd")
    post = indices(clear_s2(region, date, end).mosaic())
    rise = post.select("mndwi").subtract(pre.select("mndwi"))
    return (post.select("ndwi").gt(idx_min)
            .And(post.select("mndwi").gt(idx_min))
            .And(rise.gt(d_min))
            .And(permanent_water().Not())
            .unmask(0).rename("water"))


def union_water(region, dates=DATES, pre=None, idx_min=NDWI_MIN, d_min=D_MNDWI_MIN):
    """Union of the per-date masks: the Step 1c reference extent."""
    pre = baseline(region) if pre is None else pre
    out = None
    for d in dates:
        w = water_on(region, d, pre, idx_min, d_min)
        out = w if out is None else out.Or(w)
    return out.rename("water")


def first_seen_code(region, dates=DATES, pre=None, idx_min=NDWI_MIN, d_min=D_MNDWI_MIN):
    """1, 2, 3 for the date in `dates` on which a pixel was first seen as water; 0 otherwise."""
    pre = baseline(region) if pre is None else pre
    seen, code = None, None
    for i, d in enumerate(dates, start=1):
        w = water_on(region, d, pre, idx_min, d_min)
        new = w if seen is None else w.And(seen.Not())
        code = new.multiply(i) if code is None else code.add(new.multiply(i))
        seen = w if seen is None else seen.Or(w)
    return code.rename("first_seen_code")
