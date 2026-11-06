"""
carbon.py

Turns an hour's fuel mix into carbon intensity (gCO2/kWh) using emission factors
"""
from greenrun.grid import fetch_fuel_mix


def intensity(fuel_mix, factors):
    weighted = 0
    total = 0
    for fuel, mWh in fuel_mix.items():
        if mWh <= 0: continue
        factor = factors.get(fuel)
        if factor is None:
            raise ValueError(f"No emission factor for fuel {fuel!r}")
        weighted += mWh * factor
        total += mWh
    if total == 0:
        raise ValueError(f"Fuel mix has no generation")
    return weighted / total


def intensity_series(region, start, end, factors):
    # one gCO2/kWh value per hour in [start, end); fetch_fuel_mix returns one {fuel: MWh} dict per hour
    return [intensity(mix, factors) for mix in fetch_fuel_mix(region, start, end)]
