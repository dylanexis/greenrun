import pytest
from greenrun.scheduler import best_window, co2_saved

def test_best_window_finds_lowest_average():
    forecast = [500, 400, 100, 200, 450, 450]
    assert best_window(forecast, expected_hours=2, deadline_hours=6) == (2, 150)

def test_best_window_must_finish_before_deadline():
    # the cleanest hour (index 4) would end after the 4-hour deadline
    forecast = [300, 200, 250, 300, 10, 10]
    assert best_window(forecast, expected_hours=1, deadline_hours=4) == (1, 200)

def test_best_window_rejects_job_longer_than_deadline():
    with pytest.raises(ValueError):
        best_window([1,2,3], expected_hours=4, deadline_hours=3)

def test_co2_saved_is_intensity_difference_times_energy():
    assert co2_saved(immediate=500, scheduled=200, kwh=0.3) == pytest.approx(90)
