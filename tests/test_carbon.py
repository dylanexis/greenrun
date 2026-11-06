import pytest

from greenrun.carbon import intensity

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
