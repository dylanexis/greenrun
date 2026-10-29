PRAGMA foreign_keys = ON;


-- Keyed by EIA fuel type code (COL, NG, NUC, ...)
CREATE TABLE emission_factors(
    fuel TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    g_co2_per_kwh REAL,
    source_url TEXT
);

-- Hourly generation by fuel from the EIA API; period is the UTC hour, e.g. '2026-10-29T14'
CREATE TABLE fuel_mix(
    region TEXT NOT NULL,
    period TEXT NOT NULL,
    fuel TEXT NOT NULL,
    mwh REAL NOT NULL,
    PRIMARY KEY (region, period, fuel),
    FOREIGN KEY (fuel) REFERENCES emission_factors(fuel)
);

-- Saved intensities are what the CO2-saved numbers come from, so they stay fixed after the job runs
CREATE TABLE jobs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command TEXT NOT NULL,
    region TEXT NOT NULL,
    submitted_at TEXT NOT NULL,
    deadline TEXT NOT NULL,
    expected_hours REAL NOT NULL,
    scheduled_for TEXT,
    started_at TEXT,
    finished_at TEXT,
    exit_code INTEGER,
    immediate_g_co2_per_kwh REAL,
    scheduled_g_co2_per_kwh REAL,
    status TEXT NOT NULL DEFAULT 'waiting',
    CHECK(status IN ('waiting', 'running', 'done', 'failed'))
);
