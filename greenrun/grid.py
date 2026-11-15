"""
grid.py

Fetches hourly generation by fuel type for a region from the EIA Open Data API
"""
from greenrun.config import API_KEY
import requests
from datetime import datetime, timezone

BASE_URL = "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/" 
PAGE_SIZE = 5000 # EIA's maximum rows per request


def fetch_fuel_mix(region, start, end):
    """{period: {fuel: MWh}} for each UTC hour in [start,end], oldest first"""
    # Throw error for no API key configured
    if not API_KEY:
        raise RuntimeError("Set EIA_API_KEY (free key: eia.gov/opendata)")
    # Build parameter list
    params = {
        "api_key": API_KEY,
        "frequency": "hourly",
        "data[]": "value",
        "facets[respondent][]": region,
        "start": start,
        "end": end,
        "sort[0][column]": "period",
        "sort[0][direction]": "asc",
        "length": PAGE_SIZE
    }
    fuel_mix = {}
    offset = 0
    # Make JSON request, page through results
    while True:
            response = requests.get(BASE_URL, params={**params, "offset": offset}, timeout=30)
            response.raise_for_status()
            rows = response.json()["response"]["data"]

            for row in rows:
                if row["value"] is None: 
                    continue
                # Format: "period": {"fueltype": value}
                fuel_mix.setdefault(row["period"], {})[row["fueltype"]] = float(row["value"])
            if len(rows) < PAGE_SIZE:
                return fuel_mix
            offset += PAGE_SIZE



    

    
