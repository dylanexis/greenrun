"""
grid.py

Fetches hourly generation by fuel type for a region from the EIA Open Data API
"""
from greenrun.config import API_KEY
import requests
from datetime import datetime, timezone

BASE_URL = "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/" 


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
        "offset": "0",
        "length": "5000"
    }
    # Make JSON request, page through results
    try: 
        response = requests.get(BASE_URL, json=params, timeout=5)
        response.raise_for_status()
        body = response.json()

        fuel_mix = {}

        for row in body["data"]:
            if row["value"] is None: 
                continue
            fuel_mix.setdefault(row["period"], {})[row["fueltype"]] = float(row["value"])

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")

    except requests.exceptions.JSONDecodeError:
        print(f"Response content not valid JSON")

    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")


    

    
