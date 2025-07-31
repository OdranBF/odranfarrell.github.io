---
layout: single
title: "Welcome"
author_profile: true
classes: wide
---

## Live Map: Yesterday's Hottest Cities

<div id="cities-map" style="height: 600px; width: 100%; margin-bottom: 2em;"></div>


---

## About the Map

This live map visualizes the **maximum temperatures recorded yesterday in the world’s most populous cities.** The data is updated **daily** and sourced from the [Open-Meteo Historical Weather API](https://open-meteo.com/), providing a consistent and open-access view of extreme heat exposure around the globe. The table below shows the top twenty hottest cities yesterday.

_This map is current as of **<span id="current-date"></span>**, and reflects data collected for the previous calendar day._

For more about how I study household adaptation, spatial risk, and environmental shocks in developing economies, see the [Research](/research/) and [Projects](/projects/) sections.

---

## Yesterday’s Hottest Cities (Top 20)

<table id="temp-table" class="temp-ranking">
  <thead>
    <tr>
      <th>Rank</th>
      <th>City</th>
      <th>Country</th>
      <th>Max Temp (°C)</th>
    </tr>
  </thead>
  <tbody>
    <!-- Table rows will be inserted by JS -->
  </tbody>
</table>

<style>
  .temp-ranking {
    width: 100%;
    border-collapse: collapse;
    margin-top: 2em;
    font-size: 0.95em;
  }
  .temp-ranking th, .temp-ranking td {
    padding: 8px 12px;
    border: 1px solid #ccc;
    text-align: left;
  }
  .temp-ranking th {
    background-color: #f0f0f0;
  }
</style>

<script>
  fetch('/assets/data/city_temps.json')
    .then(response => response.json())
    .then(cities => {
      // Filter out missing temperature entries
      const validCities = cities.filter(c => c.max_temp_yesterday !== null);

      // Sort by temp descending
      validCities.sort((a, b) => b.max_temp_yesterday - a.max_temp_yesterday);

      // Take top 20
      const topCities = validCities.slice(0, 20);

      const tbody = document.querySelector("#temp-table tbody");
      topCities.forEach((city, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${index + 1}</td>
          <td>${city.name}</td>
          <td>${city.country}</td>
          <td>${city.max_temp_yesterday.toFixed(1)}°C</td>
        `;
        tbody.appendChild(row);
      });
    })
    .catch(err => {
      console.error("Failed to load temperature data:", err);
    });
</script>


<!-- Leaflet CSS & JS -->
<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

<!-- Your map styles and script -->
<link rel="stylesheet" href="/assets/css/map.css" />
<script src="/assets/js/cities-map.js"></script>

<script>
  document.addEventListener("DOMContentLoaded", function () {
    const today = new Date();
    const formatted = today.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
    document.getElementById("current-date").textContent = formatted;
  });
</script>
