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

# Fetch temperature data
results = []
for city in cities:
    lat = city["lat"]
    lon = city["lon"]
    name = city["name"]
    country = city["country"]
    population = city["population"]

    # First attempt (regular model)
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={yesterday_str}&end_date={yesterday_str}"
        f"&daily=temperature_2m_max&timezone=UTC"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        max_temp = data.get("daily", {}).get("temperature_2m_max", [None])[0]

        # Fallback to ERA5 if temp is missing
        if max_temp is None:
            fallback_url = url + "&models=era5"
            fallback_response = requests.get(fallback_url)
            fallback_response.raise_for_status()
            fallback_data = fallback_response.json()
            max_temp = fallback_data.get("daily", {}).get("temperature_2m_max", [None])[0]

        if max_temp is None:
            print(f"⚠️ No temperature data for {name}, {country} at ({lat}, {lon})")
        else:
            print(f"{name}, {country}: {max_temp}°C")

        results.append({
            "name": name,
            "country": country,
            "population": population,
            "lat": lat,
            "lon": lon,
            "max_temp_yesterday": max_temp
        })

    except Exception as e:
        print(f"❌ Failed for {name}, {country}: {e}")

# Save results
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"\n✅ Saved results to {output_path}")

