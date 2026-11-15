"""
readings.py

contains database queries for storing and retrieving hourly fuel mix readings
"""


def save_fuel_mix(conn, region, fuel_mix_by_hour):
    rows = [(region, period, fuel, mwh)
            for period, mix in fuel_mix_by_hour.items() for fuel, mwh in mix.items()]

    conn.executemany("INSERT OR REPLACE INTO fuel_mix(region, period, fuel, mwh) VALUES (?, ?, ?, ?)", rows)
    conn.commit()
    return len(rows)

def load_fuel_mix(conn, region):
    """{period: {fuel: MWh}} for every stored hour of the region"""
    fuel_mix = {}
    for period, fuel, mwh in conn.execute("SELECT period, fuel, mwh FROM fuel_mix WHERE region = ? ORDER BY period",
                                           (region,)):
        fuel_mix.setdefault(period, {})[fuel] = mwh
    return fuel_mix

def latest_period(conn, region):
    return conn.execute("SELECT MAX(period) FROM fuel_mix WHERE region = ?", (region,)).fetchone()[0]
