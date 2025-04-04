from rest_framework.test import APISimpleTestCase
from django.urls import reverse

from unittest import mock
from download import serializers
from . import mocked_osm_paths_to_geojson, mocked_overpass_API_error


class DownloadAPITest(APISimpleTestCase):

    @mock.patch('download.views.osm_paths_to_geojson', mocked_osm_paths_to_geojson)
    def download_geojson(self, polygon, network_type):
        serializer = serializers.DownloadSerializer()
        data = serializer.data
        data["polygon"] = polygon
        data["network_type"] = network_type

        response = self.client.post(reverse('download:download_paths'), data=data)
        response_data = response.json()

        return response, response_data

    # ---------- POLYGON ATTRIBUT ----------
    def test_standard_polygon_argument(self):
        response, response_data = self.download_geojson(
            "POLYGON ((13.818054 46.286698, 13.815994 46.26724, 13.898392 46.2708, 13.900108 46.286936, 13.862343 46.300695, 13.818054 46.286698))",
            "all")

        self.assertEqual(response.status_code, 200, response_data)
        self.assertEqual(response_data, {'test': 'validated'})

    def test_incorrect_WKT_format(self):
        response, response_data = self.download_geojson(
            "POLYGON ((13.818054, 46.286698), (13.815994, 46.26724), (13.898392, 46.2708), (13.900108, 46.286936), (13.862343, 46.300695), (13.818054, 46.286698))",
            "all")

        self.assertEqual(response.status_code, 400, response_data)
        self.assertIn("polygon", response_data)
        self.assertEqual(response_data["polygon"], ['Invalid polygon format'])

    # ---------- NETWORK TYPE ATTRIBUT ----------
    @mock.patch('download.views.osm_paths_to_geojson', mocked_osm_paths_to_geojson)
    def test_default_network_type_argument(self):
        serializer = serializers.DownloadSerializer()
        data = serializer.data
        data["polygon"] = "POLYGON ((13.818054 46.286698, 13.815994 46.26724, 13.898392 46.2708, 13.900108 46.286936, 13.862343 46.300695, 13.818054 46.286698))"

        response = self.client.post(reverse('download:download_paths'), data=data)
        response_data = response.json()

        self.assertEqual(response.status_code, 200, response_data)
        self.assertEqual(response_data, {'test': 'validated_default_network'})

    def test_wrong_network_type_argument(self):
        response, response_data = self.download_geojson(
            "POLYGON ((13.818054 46.286698, 13.815994 46.26724, 13.898392 46.2708, 13.900108 46.286936, 13.862343 46.300695, 13.818054 46.286698))", "test")

        self.assertEqual(response.status_code, 400, response_data)
        self.assertIn("network_type", response_data)
        self.assertEqual(response_data["network_type"], ['"test" is not a valid choice.'])

    # ---------- SERVER ERROR ----------
    @mock.patch('download.views.osm_paths_to_geojson', mocked_overpass_API_error)
    def test_server_error(self):
        serializer = serializers.DownloadSerializer()
        data = serializer.data
        data["polygon"] = "POLYGON ((13.818054 46.286698, 13.815994 46.26724, 13.898392 46.2708, 13.900108 46.286936, 13.862343 46.300695, 13.818054 46.286698))"
        data["network_type"] = "all"

        response = self.client.post(reverse('download:download_paths'), data=data)
        response_data = response.json()

        self.assertEqual(response.status_code, 500, response_data)
        self.assertIn("errors", response_data)
        self.assertEqual(response_data["errors"], "test")
