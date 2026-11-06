import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EIA_API_KEY")
REGION = os.getenv("GREENRUN_REGION", "MISO") # Grid machine is on - defaults to MISO
# TODO DB_PATH  - where SQLite file lives; pick default that works from any folder
# TODO kW       - average power draw for CO2 estimates (L7); .env values are strings*
