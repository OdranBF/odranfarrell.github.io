import json
import os
from collections import defaultdict

# Get absolute path to the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define paths
input_path = os.path.join(project_root, "assets", "data", "cities.json")
output_base = os.path.join(project_root, "assets", "data")

# Load the dataset
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Filter valid entries
valid = []
for entry in data:
    try:
        pop = int(entry.get("population", 0))
        coords = entry.get("coordinates")
        name = entry.get("name")
        country = entry.get("cou_name_en") or entry.get("country_code")

        if pop <= 0 or not coords or not name or not country:
            continue

        lat = coords.get("lat")
        lon = coords.get("lon")

        if lat is None or lon is None:
            continue

        valid.append({
            "name": name.strip(),
            "country": country.strip(),
            "population": pop,
            "lat": lat,
            "lon": lon
        })

    except Exception:
        continue

# Sort by population
sorted_valid = sorted(valid, key=lambda x: x["population"], reverse=True)

# Enforce max 3 cities per country
limited = []
country_counts = defaultdict(int)

for city in sorted_valid:
    if country_counts[city["country"]] < 3:
        limited.append(city)
        country_counts[city["country"]] += 1
    if len(limited) >= 200:
        break  # stop once we hit enough total

# Save top N versions
for N in [50, 100, 150, 200]:
    output_path = os.path.join(output_base, f"top_{N}_cities_limited.json")
    top_N = limited[:N]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(top_N, f, indent=2)

    print(f"Extracted {len(top_N)} cities (max 3 per country) to {output_path}")
