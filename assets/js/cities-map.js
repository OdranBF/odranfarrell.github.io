// Initialize the map
var map = L.map('cities-map', {
  zoomControl: true,
  zoomAnimation: true,
  zoomSnap: 1,            // Use full zoom levels to reduce tile glitches
  zoomDelta: 1,           // Only integer zoom steps (faster and less janky)
  worldCopyJump: true,
  minZoom: 2,
  maxZoom: 10,
  maxBounds: [
    [-85, -180],
    [85, 180]
  ],
  maxBoundsViscosity: 1.0
}).setView([20, 0], 2);


// Use smooth Carto basemap
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; OpenStreetMap contributors &copy; Carto',
  subdomains: 'abcd',
  maxZoom: 19
}).addTo(map);

// Wait for DOM to render, then fix sizing
document.addEventListener("DOMContentLoaded", function () {
  setTimeout(() => map.invalidateSize(), 200);
});

// Load top cities with temperatures
fetch('/assets/data/city_temps.json')
  .then(response => response.json())
  .then(cities => {
    cities.forEach(city => {
      const { name, country, lat, lon, population, max_temp_yesterday } = city;

      L.circleMarker([lat, lon], {
        radius: 6,
        color: '#cc0000',
        fillColor: '#ff6666',
        fillOpacity: 0.85,
        weight: 1
      })
      .addTo(map)
      .bindPopup(
        `<strong>${name}</strong><br>` +
        `Country: ${country}<br>` +
        `Population: ${population.toLocaleString()}<br>` +
        `Max Temp: ${max_temp_yesterday !== null ? max_temp_yesterday + "°C" : "N/A"}`
      );
    });
  })
  .catch(err => {
    console.error("Failed to load city data:", err);
  });

document.addEventListener("DOMContentLoaded", function () {
  setTimeout(() => map.invalidateSize(), 200);
});
