import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EIA_API_KEY")
REGION = os.getenv("GREENRUN_REGION", "MISO") # Grid machine is on - defaults to MISO
DB_PATH = Path(os.getenv("GREENRUN_DB", Path.home() / ".greenrun" / "greenrun.sqlite3")).expanduser()
POWER_KW = float(os.getenv("GREENRUN_POWER_KW", "0.3")) 