import json
from http.client import responses

from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.test import APISimpleTestCase
from django.urls import reverse

from unittest import mock
from download import serializers
from . import mocked_osm_paths_to_geojson, mocked_overpass_API_error

class DownloadAPITest(APISimpleTestCase):

    @mock.patch('download.views.osm_paths_to_geojson', mocked_osm_paths_to_geojson)
    def download_geojson(self, bbox, network_type):
        serializer = serializers.DownloadSerializer()
        data = serializer.data
        data["bbox"] = bbox
        data["network_type"] = network_type

        response = self.client.post(reverse('download:download_paths'), data=data)
        response_data = response.json()

        return response, response_data

    # ---------- BBOX ATTRIBUT ----------
    def test_api_good_request(self):
        response, response_data = self.download_geojson(
            "1.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781", "all")

        self.assertEqual(response.status_code, 200, response_data)
        self.assertEqual(response_data, {'test': 'validated'})

    def test_lower_lon_argument(self):
        response, response_data = self.download_geojson(
            "-180.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781", "all")

        self.assertEqual(response.status_code, 400, response_data)
        self.assertIn("bbox", response_data)
        self.assertEqual(response_data["bbox"], ["longitude coordinate out of range: it must be between -180 and 180"])

    def test_higher_lon_argument(self):
        response, response_data = self.download_geojson(
            "180.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781", "all")

        self.assertEqual(response.status_code, 400, response_data)
        self.assertIn("bbox", response_data)
        self.assertEqual(response_data["bbox"], ["longitude coordinate out of range: it must be between -180 and 180"])

    def test_lower_lat_argument(self):
        response, response_data = self.download_geojson(
            "1.0965738048514198, -90.91887785089727, 1.118439172740824, 42.92538304213781", "all")

        self.assertEqual(response.status_code, 400, response_data)
        self.assertIn("bbox", response_data)
        self.assertEqual(response_data["bbox"], ["latitude coordinate out of range: it must be between -90 and 90"])

    def test_higher_lat_argument(self):
        response, response_data = self.download_geojson(
            "1.0965738048514198, 90.91887785089727, 1.118439172740824, 42.92538304213781", "all")

        self.assertEqual(response.status_code, 400, response_data)
        self.assertIn("bbox", response_data)
        self.assertEqual(response_data["bbox"], ["latitude coordinate out of range: it must be between -90 and 90"])

    def test_order_lon_argument(self):
        response, response_data = self.download_geojson(
            "1.118439172740824, 42.91887785089727, 1.0965738048514198, 42.92538304213781", "all")

        self.assertEqual(response.status_code, 400, response_data)
        self.assertIn("bbox", response_data)
        self.assertEqual(response_data["bbox"], ["longitude coordinates are in the incorrect order"])

    def test_order_lat_argument(self):
        response, response_data = self.download_geojson(
            "1.0965738048514198, 42.92538304213781, 1.118439172740824, 42.91887785089727", "all")

        self.assertEqual(response.status_code, 400, response_data)
        self.assertIn("bbox", response_data)
        self.assertEqual(response_data["bbox"], ["latitude coordinates are in the incorrect order"])

    @mock.patch('download.views.osm_paths_to_geojson', mocked_osm_paths_to_geojson)
    def test_missing_bbox_argument(self):
        serializer = serializers.DownloadSerializer()
        data = serializer.data
        data["network_type"] = "all"

        response = self.client.post(reverse('download:download_paths'), data=data)
        response_data = response.json()
        self.assertEqual(response.status_code, 400, response_data)
        self.assertIn("bbox", response_data)
        self.assertEqual(response_data["bbox"], ["This field may not be blank."])

    def test_wrong_bbox_typo(self):
        response, response_data = self.download_geojson(
            "1.0965738048514198 42.91887785089727 1.118439172740824 42.92538304213781", "all")

        self.assertEqual(response.status_code, 400, response_data)
        self.assertIn("bbox", response_data)
        self.assertEqual(response_data["bbox"], ["Bounding box coordinates have 4 coordinates seperated by ',': minlon,minlat,maxlon,maxlat"])

    # ---------- NETWORK TYPE ATTRIBUT ----------
    @mock.patch('download.views.osm_paths_to_geojson', mocked_osm_paths_to_geojson)
    def test_default_network_type_argument(self):
        serializer = serializers.DownloadSerializer()
        data = serializer.data
        data["bbox"] = "1.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781"

        response = self.client.post(reverse('download:download_paths'), data=data)
        response_data = response.json()

        self.assertEqual(response.status_code, 200, response_data)
        self.assertEqual(response_data, {'test': 'validated_default_network'})

    def test_wrong_network_type_argument(self):
        response, response_data = self.download_geojson(
            "1.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781", "test")

        self.assertEqual(response.status_code, 400, response_data)
        self.assertIn("network_type", response_data)
        self.assertEqual(response_data["network_type"], ['"test" is not a valid choice.'])

    # ---------- SERVER ERROR ----------
    @mock.patch('download.views.osm_paths_to_geojson', mocked_overpass_API_error)
    def test_server_error(self):
        serializer = serializers.DownloadSerializer()
        data = serializer.data
        data["bbox"] = "1.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781"
        data["network_type"] = "all"

        response = self.client.post(reverse('download:download_paths'), data=data)
        response_data = response.json()

        self.assertEqual(response.status_code, 500, response_data)
        self.assertIn("errors", response_data)
        self.assertEqual(response_data["errors"],"test")
