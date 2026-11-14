"""
carbon.py

Turns an hour's fuel mix into carbon intensity (gCO2/kWh) using emission factors
"""
import sys
from datetime import datetime, timedelta, timezone

import numpy as np

HOUR_FORMAT = "%Y-%m-%dT%H" # EIA's UTC hour format


def intensity(fuel_mix, factors):
    weighted = 0
    total = 0
    for fuel, mWh in fuel_mix.items():
        if mWh <= 0: continue
        # batteries/pumped storage go negative while charging
        factor = factors.get(fuel)
        if factor is None:
            raise ValueError(f"No emission factor for fuel {fuel!r}")
        weighted += mWh * factor
        total += mWh
    if total == 0:
        raise ValueError(f"Fuel mix has no generation")
    return weighted / total

def known_fuels_only(fuel_mix_by_hour, factors):
    """Drops fuels with no emission factors (fuel_mix foreign keys would reject) and say which"""
    unknown = {fuel for mix in fuel_mix_by_hour.values() for fuel in mix} - set(factors)
    if unknown: 
        print(f"greenrun: ignoring fuels with no emission factor: {sorted(unknown)}",
              file=sys.stderr)
    return {period: {f: mwh for f, mwh in mix.items() if f in factors}
            for period, mix in fuel_mix_by_hour.items()}

def parse_hour(period):
    return datetime.strptime(period, HOUR_FORMAT).replace(tzinfo=timezone.utc)

def intensity_series(fuel_mix_by_hour, factors):
   """(first hour, hourly gCO2/kWh array) with missing hours filled with linear interpolation"""
   periods = sorted(fuel_mix_by_hour)
   if not periods:
       raise ValueError("No fuel mix data; run scripts/backfill_eia.py first")
   first = parse_hour(periods[0])
   offsets = [(parse_hour(p) - first) // timedelta(hours=1) for p in periods]
   values = [intensity(fuel_mix_by_hour[p], factors) for p in periods]
   # FFT needs evenly spaced samples, gaps in EIA data are interpolated
   return first, np.interp(np.arange(offsets[-1] + 1), offsets, values)