Ódran Farrell – Personal Website
Welcome to the source code of my personal website, hosted on GitHub Pages and powered by Jekyll with the Minimal Mistakes theme.

This site serves as a hub for my research, projects, and data visualizations. It includes:

Research on household adaptation, spatial risk, and environmental shocks.

Projects showcasing my data analysis and visualization work.

Live map visualizations, such as the daily update of the world’s hottest cities based on Open-Meteo data.

Downloadable resources like my CV and data/code links.

🌐 Live Site: https://odranbf.github.io

Features
Dynamic Data Visualizations

A Leaflet-powered map showing yesterday’s hottest cities.

Daily updated JSON data sourced from the Open-Meteo Historical Weather API.

Academic Portfolio

Overview of research projects and working papers.

Links to data and reproducible code where applicable.

Automatic Updates

GitHub Actions fetch new weather data once per day.

Pages rebuild automatically to keep maps and tables current.

Local Development
To preview the site locally:

Clone the repository:

bash
Copy
Edit
git clone https://github.com/OdranBF/odranbf.github.io.git
cd odranbf.github.io
Install dependencies:

bash
Copy
Edit
bundle install
Run Jekyll locally:

bash
Copy
Edit
bundle exec jekyll serve
Open in your browser at:

arduino
Copy
Edit
http://localhost:4000
Automated Data Updates
Python script: wd/scripts/python/fetch_cities_temp.py

Generates assets/data/city_temps.json with yesterday’s max temperatures.

GitHub Actions run daily to refresh data and rebuild the site.

License
Website content © 2025 Ódran Farrell

Theme: Minimal Mistakes (MIT Licensed)

Map and weather data: Open-Meteo

