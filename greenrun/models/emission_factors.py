"""
emission_factors.py

contains database queries for retrieving emission factors and their sources
"""

def load_factors(conn):
    """{fuel: gCO2/kWh} for every fuel that has a factor"""
    rows = conn.execute("SELECT fuel, g_co2_per_kwh FROM emission_factors WHERE g_co2_per_kwh IS NOT NULL")
    return dict(rows.fetchall())