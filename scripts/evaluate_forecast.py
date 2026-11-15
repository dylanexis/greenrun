"""
evaluate_forecast.py

Backtests the FFT forecast against the naive baseline on stored history and plots the last week
usage: python scripts/evaluate_forecast.py [days]

"""

import sys

from greenrun.carbon import intensity_series
from greenrun.config import DB_PATH, REGION
from greenrun.forecast import backtest, fft_forecast, naive_forecast
from greenrun.models import connect
from greenrun.models.emission_factors import load_factors
from greenrun.models.readings import load_fuel_mix

days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
conn = connect(DB_PATH)

_,series = intensity_series(load_fuel_mix(conn, REGION), load_factors(conn))
scores = backtest(series, days)
print(f"{REGION}, {len(series)} hours of history, last {days} days held out one day at a time")
for method, mae in scores.items():
    print(f"    {method:>5} MAE: {mae:6.1f} gCO2/kWh")

try:
    import matplotlib.pyplot as plt
except ImportError:
    sys.exit("pip install matplotlib to save forecast.png")
history, actual = series[:-24], series[-24:]
hours = range(-72, 24)
plt.figure(figsize=(9, 3.5))
plt.plot(hours[:72], history[-72:], color="gray", label="history")
plt.plot(hours[72:], actual, color="black", label="actual")
plt.plot(hours[72:], naive_forecast(history), "--", label=f"naive (MAE {scores['naive']:.0f})")
plt.plot(hours[72:], fft_forecast(history), label=f"FFT (MAE {scores['fft']:.0f})")
plt.xlabel("hours from forecast start")
plt.ylabel("gCO2/kWh")
plt.title(f"{REGION} carbon intensity: last 24 h forecast")
plt.legend()
plt.tight_layout()
plt.savefig("docs/forecast.png", dpi=150)
print("Saved forecast.png")