# Download OpenStreetMap paths as Geojson

[![codecov](https://codecov.io/gh/makinacorpus/osm-paths/graph/badge.svg?token=Jg4jytesmP)](https://codecov.io/gh/makinacorpus/osm-paths)
[![Testing](https://github.com/makinacorpus/osm-paths/actions/workflows/tests.yml/badge.svg)](https://github.com/makinacorpus/osm-paths/actions/workflows/tests.yml)

**OpenStreetMap** is a collaborative, open-source mapping platform that provides freely accessible geographic data,
maintained by a global community of contributors.

This application uses **osmnx** to retrieve path data from OpenStreetMap via the **Overpass API**,
converting the paths into **LineString** format. 
The extracted paths are then saved as a **GeoJSON** file compatible with **Geotrek**.

⚠️ **Important**: Before using the exported paths, ensure they meet the requirements outlined in the  
[Geotrek-Admin documentation](https://geotrek.readthedocs.io/en/latest/import-data/import-paths.html).

## Run with docker

### 1. Run the application

1. Run command in a container:
    ```bash
    docker run -v $(pwd):/app --user $(id -u) ghcr.io/makinacorpus/osm-paths osm_paths download --help
    ```

## Download paths with command

Paths can be downloaded using the **Django management command**. 
The desired boundary can be specified using either a **bounding box** or a **polygon**. 
Polygons should be provided in `.wkt` or `.geojson` format. 
This file must be saved in the `var/boundary` directory.

#### Download paths Using a Bounding Box
```bash
osm_paths download OUTPUT_FILE -b BBOX [-n NETWORK_TYPE]
```
**Parameters**
- **OUTPUT_FILE**: path of your output file with the geojson extension: `/app/var/boundary/filename.geojson`.
    The output file will be delivered in the `var/export/` directory.
- **BBOX**: bounding box coordinates in WGS84: ``minlon,minlat,maxlon,maxlat``
- **NETWORK_TYPE** *(optional)*: type of paths to download.
  - `all`
  - `drive`
  - `bike`
  - `walk` (default)

> **Exemples**
> ```bash
> docker run -v $(pwd):/app --user $(id -u) ghcr.io/makinacorpus/osm-paths osm_paths download paths.geojson -b 43.541462,1.364021,43.661376,1.540489 -n "bike"
> ```

#### Download Paths Using a Polygon
```bash
osm_paths download OUTPUT_FILE -p POLYGON_FILE [-n NETWORK_TYPE]
```
**Parameters**
**OUTPUT_FILE**: path of your output file with the geojson extension: `/app/var/boundary/filename.geojson`.
    The output file will be delivered in the `var/export/` directory.

**POLYGON_FILE**: WKT or GeoJSON filename defining the polygon boundary.
    - WKT file exemple
    - GeoJSON file exemple

- **NETWORK_TYPE** *(optional)*: type of paths to download.
  - `all`
  - `drive`
  - `bike`
  - `walk` (default)

⚠️ **Performance Tip**: Using a polygon with fewer nodes improves execution speed. It is recommended to keep the number of nodes below 1000.

> **Exemple**
> ```bash
> docker run -v $(pwd):/app --user $(id -u) ghcr.io/makinacorpus/osm-paths osm_paths download paths.geojson -p boundary.wkt -n "bike"
> ```

## Boundary file exemples

### WKT file

```txt
POLYGON ((13.695831 46.471916,
          13.487091 46.364936,
          13.75351 46.193141,
          13.94577 46.226403,
          14.117432 46.397147,
          13.908691 46.477591,
          13.695831 46.471916))
```

### GeoJSON file

```json
{
    "type": "Polygon", 
    "coordinates": [
        [
            [13.695831, 46.471916], 
            [13.487091, 46.364936], 
            [13.753510, 46.193141], 
            [13.945770, 46.226403], 
            [14.117432, 46.397147], 
            [13.908691, 46.477591], 
            [13.695831, 46.471916]  
        ]
    ]
}

```





