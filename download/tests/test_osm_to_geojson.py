import os
import json

import osmnx as ox

from django.test import SimpleTestCase

from unittest import mock
from download.osm_to_geojson import osm_paths_to_geojson, save_geojson
from geopandas import GeoDataFrame
from shapely import Polygon


class OpenStreetMapExtractTest(SimpleTestCase):
    network = None

    @classmethod
    def setUp(cls):
        # ---------- GRAPH_FROM_POLYGON ----------
        filename = os.path.join(os.path.dirname(__file__), 'data', 'network.graphml')
        cls.network = ox.io.load_graphml(filename)

        filename2 = os.path.join(os.path.dirname(__file__), 'data', 'network2.graphml')
        cls.network2 = ox.io.load_graphml(filename2)

        # ---------- RESULTS ----------
        filename_results = os.path.join(os.path.dirname(__file__), 'data', 'results.geojson')
        with open(filename_results, 'r') as f:
            cls.results = json.load(f)

    @mock.patch('download.osm_to_geojson.ox.graph_from_polygon')
    def test_good_method_response(self, mocked):
        polygon = Polygon ([(13.818054, 46.286698), (13.815994, 46.26724), (13.898392, 46.2708), (13.900108, 46.286936), (13.862343, 46.300695), (13.818054, 46.286698)])
        network_type = "walk"

        mocked.return_value = self.network

        geojson = osm_paths_to_geojson(polygon, network_type)

        self.assertEqual(json.loads(geojson), self.results)

    @mock.patch('download.osm_to_geojson.ox.graph_from_polygon')
    def test_different_polygon(self, mocked):
        polygon = Polygon([(13.818054, 46.286698), (13.815994, 46.26724), (13.898392, 46.2720), (13.900108, 46.286936), (13.862343, 46.300695), (13.818054, 46.286698)])
        network_type = "walk"

        mocked.return_value = self.network2

        geojson = osm_paths_to_geojson(polygon, network_type)

        self.assertNotEqual(json.loads(geojson), self.results)

    @mock.patch('download.osm_to_geojson.ox.graph_from_polygon')
    def test_incorrect_polygon(self, mocked):
        polygon = Polygon([(0,0), (0,3), (3,3), (3,0), (2,0), (2,2), (1,2), (1,1), (2,1), (2,0), (0,0)])
        network_type = "walk"

        mocked.return_value = self.network

        with self.assertRaisesRegex(TypeError, "Invalid polygon"):
            osm_paths_to_geojson(polygon, network_type)

    @mock.patch('download.osm_to_geojson.ox.graph_from_polygon')
    def test_incorrect_polygon_type(self, mocked):
        polygon = "POLYGON ((13.818054 46.286698, 13.815994 46.26724, 13.898392 46.2708, 13.900108 46.286936, 13.862343 46.300695, 13.818054 46.286698))"
        network_type = "walk"

        mocked.return_value = self.network

        with self.assertRaisesRegex(TypeError, "Invalid polygon"):
            osm_paths_to_geojson(polygon, network_type)

    def test_save_file(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', 'test_save.geojson')
        geojson = json.dumps(self.results)

        save_geojson(geojson, filename)

        self.assertTrue(os.path.exists(filename))
        with open(filename, "r") as f:
            self.assertEqual(json.load(f), json.loads(geojson))
        os.remove(filename)



