# Download OpenStreetMap paths as Geojson

**OpenStreetMap** is a collaborative, open-source mapping platform that provides freely accessible geographic data,
maintained by a global community of contributors.

This application uses **osmnx** to retrieve path data from OpenStreetMap via the **Overpass API**,
converting the paths into LineString format. 
The extracted paths are then saved as a GeoJSON file compatible with **Geotrek**.

⚠️ Before use, paths should be verified according to the 
[Geotrek-Admin documentation](https://geotrek.readthedocs.io/en/latest/import-data/import-paths.html).

## Load paths with Django-admin command

## Load paths with the API
