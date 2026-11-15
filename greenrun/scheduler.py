"""
scheduler.py

Picks the start hour before a job's deadline with the lowest average forecast intensity
"""
import math


def best_window(forecast, expected_hours, deadline_hours):
    "(start hour offset, average gCO2/kWh) of the cleanest window that finishes by the deadline"
    length = math.ceil(expected_hours)
    last_start = math.floor(deadline_hours - expected_hours)
    if last_start < 0:
        raise ValueError("Job is longer than the time until its deadline")
    if last_start + length > len(forecast):
        raise ValueError("Forecast does not reach the deadline")
    averages = [sum(forecast[s:s + length]) / length for s in range(last_start + 1)]
    best = min(range(len(averages)), key=averages.__getitem__) # ties go to earliest start

    return best, averages[best]


def co2_saved(immediate, scheduled, kwh):
    """Grams of CO2 avoided by runnint at 'scheduled' instead of 'immediate' gCO2/kWh"""
    return (immediate - scheduled) * kwh
