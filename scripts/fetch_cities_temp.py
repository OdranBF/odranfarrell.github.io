import json
import os
import requests
from datetime import date, timedelta

# Get yesterday's date
yesterday = date.today() - timedelta(days=1)
yesterday_str = yesterday.isoformat()

# Paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_path = os.path.join(project_root, "assets", "data", "top_100_cities_limited.json")
output_path = os.path.join(project_root, "assets", "data", "city_temps.json")

# Load cities
with open(input_path, "r", encoding="utf-8") as f:
    cities = json.load(f)

# Load existing temps if file exists
previous_data = {}
if os.path.exists(output_path):
    with open(output_path, "r", encoding="utf-8") as f:
        try:
            previous_data = {c["name"]: c for c in json.load(f)}
        except json.JSONDecodeError:
            previous_data = {}

results = []
for city in cities:
    lat = city["lat"]
    lon = city["lon"]
    name = city["name"]
    country = city["country"]
    population = city["population"]

    # Use ERA5 for better reliability
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={yesterday_str}&end_date={yesterday_str}"
        f"&daily=temperature_2m_max&timezone=UTC&models=era5"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        max_temp = data.get("daily", {}).get("temperature_2m_max", [None])[0]

        # If no new data, keep the previous value if available
        if max_temp is None and name in previous_data:
            max_temp = previous_data[name].get("max_temp_yesterday")

        results.append({
            "name": name,
            "country": country,
            "population": population,
            "lat": lat,
            "lon": lon,
            "max_temp_yesterday": max_temp
        })

        if max_temp is None:
            print(f"⚠️ Still no data for {name}, {country}")
        else:
            print(f"{name}, {country}: {max_temp}°C")

    except Exception as e:
        # On error, keep old data if available
        old_temp = previous_data.get(name, {}).get("max_temp_yesterday")
        results.append({
            "name": name,
            "country": country,
            "population": population,
            "lat": lat,
            "lon": lon,
            "max_temp_yesterday": old_temp
        })
        print(f"❌ Failed for {name}, {country}: {e}")

# Save results
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"\n✅ Saved results to {output_path}")
