import sqlite3
from pathlib import Path


SQL_DIR = Path(__file__).resolve().parent[2] / "sql"

def connect(path):
    """Open the database, creating tables and emission factors for the first time"""
    path = Path(path)
    is_new = not path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    if is_new:
        conn.executescript((SQL_DIR / "schema.sql").read_text())
        conn.executescript((SQL_DIR / "seed_emission_factors.sql").read_text())
    return conn