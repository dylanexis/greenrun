import numpy as np
from greenrun.forecast import backtest, fft_forecast, naive_forecast, mean_absolute_error


def grid_like(hours, noise=0.0, seed=0):
    """Daily solar dip plus cleaner weekends, like a real grid"""
    t = np.arange(hours)
    rng = np.random.default_rng(seed)
    return 500 - 80 *np.sin(2*np.pi * t / 24) - 40 * np.sin(2*np.pi * t / 168) + noise * rng.standard_normal(hours)

def test_naive_repeats_last_day():
    history = np.arange(48)
    assert list(naive_forecast(history, 26)) == list(range(24,48)) + [24, 25]

def test_fft_recovers_daily_and_weekly_cycles_exactly():
    series = grid_like(4 * 168 + 24)
    assert mean_absolute_error(fft_forecast(series[:-24]),
                               series[-24:]) < 1e-6

def test_fft_beats_naive_when_week_and_noise_matter():
    # naive copies yesterday's noise and misses the weekly drift; the FFT averages both out
    scores = backtest(grid_like(6*168, noise=20), days = 7)
    assert scores["fft"] < scores["naive"]
