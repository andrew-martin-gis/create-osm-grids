# create-osm-grids

Automates OSM grid creation for use in JOSM. Given a bounding box and building/floor configuration, generates one `.osm` file per floor with the correct bounds, corner nodes, center origin node, and bounding way. Also prints portal coordinates for each generated floor.

## Usage

```
python OSM_setup.py
```

The script prompts for:

1. Site number
2. Top-left and bottom-right coordinates of the overall bounding box (`lat,lon`)
3. Number of buildings
4. For each building: building number, number of floors, and initial floor number

Output `.osm` files are written to the current directory, named `site-building-floor.osm`.

## Requirements

```
pip install osmium shapely
```

Python 3
