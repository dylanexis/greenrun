"""
forecast.py

Forecasts the next 24 hours of carbon intensity from daily and weekly cycles (FFT),
and scores it against a same-hour-yesterday baseline
"""
import numpy as np

DAY = 24
WEEK = 168
PERIODS = (WEEK, DAY, DAY / 2, DAY / 3) # weekly cycle, daily cycle, first two harmonics


def naive_forecast(history, hours=24):
    """Repeat the last 24 hours"""
    history = np.asarray(history, dtype=float)
    return np.array([history[-DAY + h % DAY] for h in range(hours)])

def fft_forecast(history, hours=24):
    """Keep only the daily/weekly frequencies of the last whole weeks of history and extend them"""
    history = np.asarray(history, dtype=float)
    n = len(history) // WEEK * WEEK
    if n == 0:
        raise ValueError(f"Need at least {WEEK} hours of history, got {len(history)}")
    window = history[-n:]
    spectrum = np.fft.rfft(window)
    keep = np.zeros_like(spectrum)
    keep[0] = spectrum[0]
    for period in PERIODS:
        k = round(n / period) # n is whole number of weeks, so every period lands on exact bin
        keep[k] = spectrum[k]
    fitted = np.fft.irfft(keep, n)
    # the cycles all repeat every week and n is whole weeks, so the future is the fit continued
    return np.array([fitted[(n + h) % n] for h in range(hours)])

def mean_absolute_error(predicted, actual):
    return float(np.mean(np.abs(np.asarray(predicted) - np.asarray(actual))))

def backtest(series, days = 7):
    """MAE of each method, forecasting each of the last 'days' days from the data before fit"""
    errors = {"naive": [], "fft": []}
    for d in range(days, 0, -1):
            cut = len(series) - d * DAY
            history, actual = series[:cut], series[cut:cut + DAY]
            errors["naive"].append(mean_absolute_error(naive_forecast(history), actual))
            errors["fft"].append(mean_absolute_error(fft_forecast(history), actual))
    return {method: float(np.mean(e)) for method, e in errors.items()}
