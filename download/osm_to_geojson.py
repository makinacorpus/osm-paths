import osmnx as ox
from django.contrib.gis.geos import fromstr
from shapely import Polygon

from geopandas import GeoDataFrame

def osm_paths_to_geojson(polygon, network_type="walk"):
    """
    download paths from OpenStreetMap as a graph, simplify the graph and convert the data into a geojson file
    """
    if not isinstance(polygon, Polygon) or not polygon.is_valid:
        raise TypeError("Invalid polygon")

    network_graph = ox.graph_from_polygon(polygon, network_type=network_type, truncate_by_edge=True)

    gdf_edges = ox.graph_to_gdfs(network_graph, nodes=False)

    geojson = gdf_edges.to_json(indent = 4)
    return geojson


def save_geojson(geojson, filename):
    with open(filename, "w") as output:
        output.write(geojson)
