# scripts/fetch_cities_temp.py
import json
import os
import time
from datetime import datetime, timedelta, timezone

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ---------- Paths ----------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(PROJECT_ROOT, "assets", "data", "top_100_cities_limited.json")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "assets", "data", "city_temps.json")

# ---------- Dates (UTC) ----------
YDAY_UTC = (datetime.now(timezone.utc) - timedelta(days=1)).date().isoformat()

# ---------- Robust HTTP session ----------
TIMEOUT = 12  # seconds per request
RETRIES = Retry(
    total=3,
    connect=3,
    read=3,
    backoff_factor=1.5,  # 0s, 1.5s, 3s...
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=("GET",),
)
SESSION = requests.Session()
SESSION.mount("https://", HTTPAdapter(max_retries=RETRIES))
SESSION.mount("http://", HTTPAdapter(max_retries=RETRIES))

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def _extract_first_daily_value(obj: dict, key: str):
    daily = obj.get("daily") or {}
    arr = daily.get(key) or []
    if isinstance(arr, list) and arr:
        return arr[0]
    return None


def fetch_archive_max(lat: float, lon: float):
    """Try the archive (ERA5) for yesterday's max temp."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": YDAY_UTC,
        "end_date": YDAY_UTC,
        "daily": "temperature_2m_max",
        "timezone": "UTC",
        "models": "era5",
    }
    r = SESSION.get(ARCHIVE_URL, params=params, timeout=TIMEOUT)
    r.raise_for_status()
    return _extract_first_daily_value(r.json(), "temperature_2m_max")


def fetch_forecast_pastday_max(lat: float, lon: float):
    """Fallback: forecast endpoint with past_days=1 also returns yesterday."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max",
        "timezone": "UTC",
        "past_days": 1,  # includes yesterday
    }
    r = SESSION.get(FORECAST_URL, params=params, timeout=TIMEOUT)
    r.raise_for_status()
    return _extract_first_daily_value(r.json(), "temperature_2m_max")


def fetch_city_max_temp(lat: float, lon: float):
    """
    Try archive first (better reproducibility), then forecast as a fallback.
    Return float or None.
    """
    try:
        t = fetch_archive_max(lat, lon)
        if t is not None:
            return float(t)
    except requests.exceptions.RequestException:
        # Archive slow or failing -> fall back
        pass

    try:
        t = fetch_forecast_pastday_max(lat, lon)
        return float(t) if t is not None else None
    except requests.exceptions.RequestException:
        return None


def main():
    # Load inputs
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        cities = json.load(f)

    # Load previous outputs (for graceful fallback)
    previous_data = {}
    if os.path.exists(OUTPUT_PATH):
        try:
            with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
                previous_data = {c["name"]: c for c in json.load(f)}
        except json.JSONDecodeError:
            previous_data = {}

    results = []
    failures = 0
    started = time.time()

    for idx, city in enumerate(cities, 1):
        name = city["name"]
        country = city.get("country")
        lat = float(city["lat"])
        lon = float(city["lon"])

        tmax = fetch_city_max_temp(lat, lon)

        if tmax is None:
            # Keep old value if available, else None
            old = previous_data.get(name, {}).get("max_temp_yesterday")
            tmax = old
            failures += 1
            print(f"⚠️  No fresh data for {name}, {country}; keeping {tmax}", flush=True)
        else:
            print(f"✅ {name}, {country}: {tmax} °C", flush=True)

        results.append({
            "name": name,
            "country": country,
            "population": city.get("population"),
            "lat": lat,
            "lon": lon,
            "max_temp_yesterday": tmax
        })

        # Gentle pacing (tune/raise if you still hit rate limits)
        time.sleep(0.12)

        # Flush logs periodically in Actions UI
        if idx % 50 == 0:
            print(f"...processed {idx}/{len(cities)} cities", flush=True)

    # Save output
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    elapsed = time.time() - started
    print(f"\n✅ Saved results to {OUTPUT_PATH} | cities={len(results)} | failures={failures} | {elapsed:.1f}s")


if __name__ == "__main__":
    main()
