import osmnx as ox
from django.conf import settings
from shapely import Polygon

ox.settings.use_cache = True
ox.settings.cache_folder = settings.CACHE_DIR


def osm_paths_to_geojson(polygon, network_type="walk"):
    """
    download paths from OpenStreetMap as a graph, simplify the graph and convert the data into a geojson file
    """
    if not isinstance(polygon, Polygon) or not polygon.is_valid:
        raise TypeError("Invalid polygon")

    # Simplify the boundary with a tolerance of 0.00001°
    simplified_polygon = polygon.simplify(0.00001)

    network_graph_directed = ox.graph_from_polygon(
        simplified_polygon, network_type=network_type, truncate_by_edge=True
    )

    # convert to undirected MultiDiGraph to avoid double path
    network_graph_undirected = ox.convert.to_undirected(network_graph_directed)

    gdf_edges = ox.graph_to_gdfs(network_graph_undirected, nodes=False)

    geojson = gdf_edges.to_json(indent=4)

    return geojson


def save_geojson(geojson, filename):
    with open(filename, "w") as output:
        output.write(geojson)
