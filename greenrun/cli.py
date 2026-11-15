"""
cli.py

greenrun --deadline 6h [--hours 1] -- <command>
Waits for the cleanest window before the deadline, then runs the command and logs the job
"""
import argparse
import math
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone

from greenrun import config
from greenrun.carbon import HOUR_FORMAT, intensity_series, known_fuels_only
from greenrun.forecast import fft_forecast
from greenrun.grid import fetch_fuel_mix
from greenrun.models import connect
from greenrun.models.emission_factors import load_factors
from greenrun.models.jobs import insert_job, update_job
from greenrun.models.readings import latest_period, load_fuel_mix, save_fuel_mix
from greenrun.scheduler import best_window, co2_saved

UNITS = {"m": 1 / 60, "h": 1, "d": 24}


def parse_duration(text):
    """ '90m', '6h', '1d12h or a bare '2' (hours) -> hours as a float' """
    if re.fullmatch(r"\d+(\.\d+)?", text):
        return float(text)
    if not re.fullmatch(r"(\d+(\.\d+)?[mhd])+", text):
        raise argparse.ArgumentTypeError(f"bad duration {text!r}; use e.g. 90m, 6h, 1d12h")
    return sum(float(n) * UNITS[unit] for n, _, unit in re.findall(r"(\d+(\.\d+)?)([mhd])", text))

def refresh(conn, region, now):
    """Fetch all hours since the last stored one so the forecast starts from fresh data"""
    last = latest_period(conn, region)
    if last is None:
        raise SystemExit("greenrun: no history yet; run python 'scripts/backfill_eia.py' first")
    try:
        mix = fetch_fuel_mix(region, last, now.strftime(HOUR_FORMAT))
    except Exception as err: # stale data is still usable; say so and carry on
        print(f"greenrun: could not refresh grid data ({err}); using stored history",
              file=sys.stderr)
        return save_fuel_mix(conn, region, known_fuels_only(mix, load_factors(conn)))


def main(argv=None):
    parser = argparse.ArgumentParser(prog="greenrun", description="Run a command when the grid is cleanest")
    parser.add_argument("--deadline", type=parse_duration, required=True, help="latest finish e.g. 6h")
    parser.add_argument("--hours", type=parse_duration, required=True, help="expected run time (default 1h)")
    parser.add_argument("--region", default=config.REGION, help=f"EIA balancing authority (default {config.REGION})")
    parser.add_argument("--dry-run", action="store_true", help="print the plan without waiting or running")
    parser.add_argument("command", nargs=argparse.REMAINDER,help="-- command to run")

    args = parser.parse_args(argv)
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("give the command after --")
    
    now = datetime.now(timezone.utc)
    this_hour = now.replace(minute=0, second=0, microsecond=0)
    conn = connect(config.DB_PATH)
    refresh(conn, args.region, now)
    first, series = intensity_series(load_fuel_mix(conn, args.region), load_factors(conn))

    # EIA data lags real time by a few hours: forecast across the gap, then drop it so index 0 is this hour
    last = first + timedelta(hours=len(series) - 1)
    skip = max((this_hour - last) // timedelta(hours=1) - 1, 0)
    forecast = fft_forecast(series, skip + math.ceil(args.deadline))[skip:]
    try:
        start, scheduled = best_window(forecast, args.hours, args.deadline)
    except ValueError as err:
        parser.error(str(err))
    
    immediate = float(forecast[:math.ceil(args.hours)].mean())

    saved_g = co2_saved(immediate, scheduled, config.POWER_KW * args.hours)
    run_at = this_hour + timedelta(hours=start)

    print(f"Now: {immediate:.0f} gCO2/kWh. Cleanest start: {run_at:%Y-%m-%d%H:%M} UTC "
          f"at {scheduled:.0f} gCO2/kWh, saving ~{saved_g:.0f} g CO2 ({100 * (1 - scheduled / immediate):.0f}%)")
    if args.dry_run:
        return 0

    job_id = insert_job(conn, command = " ".join(command), region=args.region, 
                        submitted_at=now.isoformat(), deadline = (now + timedelta(hours=args.deadline)).isoformat(),
                        expected_hours=args.hours, scheduled_for=run_at.isoformat(), immediate_g_co2_per_kwh=immediate,
                        scheduled_g_co2_per_kwh=scheduled)

    time.sleep(max(0.0, (run_at - datetime.now(timezone.utc)).total_seconds()))
    update_job(conn, job_id, status="running", started_at=datetime.now(timezone.utc).isoformat())
    exit_code = subprocess.run(command).returncode
    update_job(conn, job_id, status="done" if exit_code == 0 else "failed", finished_at=datetime.now(timezone.utc).isoformat(),
               exit_code=exit_code)
    return exit_code

if __name__ == "__main__":
    sys.exit(main())

