import osmnx as ox

from geopandas import GeoDataFrame

def osm_paths_to_geojson(bbox, network_type="walk"):
    """
    download paths from OpenStreetMap as a graph, simplify the graph and convert the data into a geojson file
    """
    bbox_tuple = None
    if isinstance(bbox, str):
        bbox_tuple = tuple(float(coord) for coord in bbox.split(','))
    elif isinstance(bbox, tuple):
        bbox_tuple = bbox

    network_graph = ox.graph_from_bbox(bbox=bbox_tuple, network_type=network_type, truncate_by_edge=True)

    print(network_graph, '\n')
    gdf_edges = ox.graph_to_gdfs(network_graph, nodes=False)

    geojson = gdf_edges.to_json()
    print(geojson, '\n')
    return geojson


def save_geojson(geojson, filename):
    with open(filename, "w") as output:
        output.write(geojson)
