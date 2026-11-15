"""
backfill_eia.py

Loads weeks of past hourly fuel mix from the EIA API so the forecast has history to fit
usage = python scripts/backfill_eia.py [weeks]
"""
import sys
from datetime import datetime, timedelta, timezone

from greenrun.carbon import HOUR_FORMAT, known_fuels_only
from greenrun.grid import fetch_fuel_mix
from greenrun.config import DB_PATH, REGION
from greenrun.models import connect
from greenrun.models.emission_factors import load_factors
from greenrun.models.readings import save_fuel_mix

weeks = int(sys.argv[1]) if len(sys.argv) > 1 else 8
end = datetime.now(timezone.utc)
start = end - timedelta(weeks=weeks)

conn = connect(DB_PATH)
mix = fetch_fuel_mix(REGION, start.strftime(HOUR_FORMAT), end.strftime(HOUR_FORMAT))
# Returns dict of dicts {period: {fuel: mwh}} 
mix = known_fuels_only(mix, load_factors(conn))
print(f"Saved {save_fuel_mix(conn,REGION, mix)} rows covering {len(mix)} hours of {REGION} to {DB_PATH}")

