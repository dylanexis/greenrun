import pytest

from greenrun.carbon import intensity, intensity_series
import numpy as np


FACTORS = {
    "COL": 820,
    "WND": 11,
}

def test_intensity_is_generation_weighted_average():
    # 3 parts coal, 1 part wind; negative/zero generation is ignored
    mix = {"COL": 300, "WND": 100, "SUN": 0}
    assert intensity(mix, FACTORS) == pytest.approx((300 * 820 + 100 * 11) / 400)

def test_intensity_rejects_fuel_without_factor():
    with pytest.raises(ValueError):
        intensity({"COL": 100, "NUC": 50}, FACTORS)

def test_intensity_series_is_hourly_and_fills_gaps():
    mix = {"2026-10-29T02": {"WND": 1}, "2026-10-29T00": {"COL": 1}}
    first, series = intensity_series(mix, FACTORS)
    assert first.hour == 0
    assert np.allclose(series, [820, (820 +11) / 2, 11])
