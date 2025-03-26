import json

from rest_framework.exceptions import ValidationError
from rest_framework.test import APISimpleTestCase
from django.urls import reverse

from unittest import mock
from download import serializers
from . import mocked_osm_paths_to_geojson

class DownloadAPITest(APISimpleTestCase):

    # ---------- BBOX ATTRIBUT ----------
    @mock.patch('download.osm_to_geojson.osm_paths_to_geojson', mocked_osm_paths_to_geojson)
    def test_api_good_request(self):
        serializer = serializers.DownloadSerializer()
        data = serializer.data
        data["bbox"] = "1.0965738048514198,42.91887785089727,1.118439172740824,42.92538304213781"
        data["network_type"] = "all"

        response = self.client.post(reverse('download:download_paths'), data={"bbox": "1.0965738048514198,42.91887785089727,1.118439172740824,42.92538304213781"}, content_type='application/json')
        response_data = response.json()
        self.assertEqual(response.status_code, 200, response_data)
        self.assertEqual(response_data, {'test': 'validated'})

    """
    @mock.patch('download.osm_to_geojson.osm_paths_to_geojson', mocked_osm_paths_to_geojson)
    def test_lower_lat_argument(self):
        serializer = serializers.DownloadSerializer()
        data = serializer.data
        data["bbox"] = "-90.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781"
        data["network_type"] = "all"

        with self.assertRaisesRegex(ValidationError, "latitude coordinate out of range: it must be between -90 and 90"):
            response = self.client.post(reverse('download:download_paths'), data=data, content_type='application/json')

        response_data = response.json()
        self.assertEqual(response.status_code, 400, response_data)
        self.assertIn('bbox', data)
        self.assertEqual(['This field is required.'], data['bbox'])

    @mock.patch('download.osm_to_geojson.osm_paths_to_geojson', mocked_osm_paths_to_geojson)
    def test_higher_lat_argument(self):
        serializer = serializers.DownloadSerializer()
        data = serializer.data
        data["bbox"] = "90.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781"
        data["network_type"] = "all"

        with self.assertRaisesRegex(ValidationError,
                                    "latitude coordinate out of range: it must be between -90 and 90"):
            response = self.client.post(reverse('download:download_paths'), data=data, content_type='application/json')

        response_data = response.json()
        self.assertEqual(response.status_code, 400, response_data)
        self.assertIn('bbox', data)
        self.assertEqual(['This field is required.'], data['bbox'])

    @mock.patch('download.osm_to_geojson.osm_paths_to_geojson', mocked_osm_paths_to_geojson)
    def test_lower_lon_argument(self):
        serializer = serializers.DownloadSerializer()
        data = serializer.data
        data["bbox"] = "1.0965738048514198, -182.91887785089727, 1.118439172740824, 42.92538304213781"
        data["network_type"] = "all"

        with self.assertRaisesRegex(ValidationError,
                                    "longitude coordinate out of range: it must be between -180 and 180"):
            response = self.client.post(reverse('download:download_paths'), data=data, content_type='application/json')

        response_data = response.json()
        self.assertEqual(response.status_code, 400, response_data)
        self.assertIn('bbox', data)
        self.assertEqual(['This field is required.'], data['bbox'])

    @mock.patch('download.osm_to_geojson.osm_paths_to_geojson', mocked_osm_paths_to_geojson)
    def test_higher_lon_argument(self):
        serializer = serializers.DownloadSerializer()
        data = serializer.data
        data["bbox"] = "1.0965738048514198, 182.91887785089727, 1.118439172740824, 42.92538304213781"
        data["network_type"] = "all"

        with self.assertRaisesRegex(ValidationError,
                                    "longitude coordinate out of range: it must be between -180 and 180"):
            response = self.client.post(reverse('download:download_paths'), data=data, content_type='application/json')

        response_data = response.json()
        self.assertEqual(response.status_code, 400, response_data)
        self.assertIn('bbox', data)
        self.assertEqual(['This field is required.'], data['bbox'])
    """