import os
import json

import osmnx as ox

from django.test import SimpleTestCase

from unittest import mock
from download.osm_to_geojson import osm_paths_to_geojson
from geopandas import GeoDataFrame

class OpenStreetMapExtractTest(SimpleTestCase):
    network = None

    @classmethod
    def setUp(self):
        # ---------- GRAPH_FROM_BBOX ----------
        filename = os.path.join(os.path.dirname(__file__), 'data', 'network.graphml')
        self.network = ox.io.load_graphml(filename)

        filename2 = os.path.join(os.path.dirname(__file__), 'data', 'network2.graphml')
        self.network2 = ox.io.load_graphml(filename2)

        # ---------- RESULTS ----------
        filename_results = os.path.join(os.path.dirname(__file__), 'data', 'results.geojson')
        with open(filename_results, 'r') as f:
            self.results = json.load(f)


    @mock.patch('download.osm_to_geojson.ox.graph_from_bbox')
    def test_good_method_response_str_bbox(self, mocked):
        bbox = "1.1300408465969936,42.98442863311549,1.1355071885693446,42.98605326403185"
        network_type = "walk"

        mocked.return_value = self.network

        geojson = osm_paths_to_geojson(bbox, network_type)

        self.assertEqual(json.loads(geojson), self.results)

    @mock.patch('download.osm_to_geojson.ox.graph_from_bbox')
    def test_good_method_response_str_bbox(self, mocked):
        bbox = "1.1300408465969936,42.97442863311549,1.1355071885693446,42.99605326403185"
        network_type = "walk"

        mocked.return_value = self.network2

        geojson = osm_paths_to_geojson(bbox, network_type)

        self.assertNotEqual(json.loads(geojson), self.results)




