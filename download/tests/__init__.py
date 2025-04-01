import json

def mocked_osm_paths_to_geojson(polygon, network_type):
    response = {'test': 'validated'}
    if network_type == "walk":
        response = {'test': 'validated_default_network'}
    return json.dumps(response)

def mocked_overpass_API_error(polygon, network_type):
    raise Exception('test')
