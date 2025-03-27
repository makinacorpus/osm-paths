import os
import json

from django.test import SimpleTestCase
from django.core.management import call_command
from django.core.management.base import CommandError

from unittest import mock
from . import mocked_osm_paths_to_geojson

@mock.patch('download.osm_to_geojson.osm_paths_to_geojson', mocked_osm_paths_to_geojson)
class CommandTest(SimpleTestCase):
    filename = os.path.join(os.path.dirname(__file__), 'data', 'test.geojson')

    # ---------- BBOX ARGUMENT ----------
    def test_standard_arguments(self):
        arguments = [1.0965738048514198,42.91887785089727,1.118439172740824,42.92538304213781,self.filename,'-n',"all"]

        call_command('download', arguments)

        self.assertTrue(os.path.exists(self.filename))
        with open(self.filename, "r") as f:
            self.assertEqual(json.load(f), {'test': 'validated'})
        os.remove(self.filename)

    def test_lower_lon_argument(self):
        arguments = [-180.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781, self.filename, '-n', "all"]

        with self.assertRaisesRegex(CommandError, "longitude coordinate out of range: it must be between -180 and 180"):
            call_command('download', arguments)

        self.assertFalse(os.path.exists(self.filename))

    def test_higher_lon_argument(self):
        arguments = [180.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781, self.filename, '-n', "all"]

        with self.assertRaisesRegex(CommandError, "longitude coordinate out of range: it must be between -180 and 180"):
            call_command('download', arguments)

        self.assertFalse(os.path.exists(self.filename))

    def test_lower_lat_argument(self):
        arguments = [1.0965738048514198, -92.91887785089727, 1.118439172740824, 42.92538304213781, self.filename, '-n',
                     "all"]

        with self.assertRaisesRegex(CommandError, "latitude coordinate out of range: it must be between -90 and 90"):
            call_command('download', arguments)

        self.assertFalse(os.path.exists(self.filename))

    def test_higher_lat_argument(self):
        arguments = [1.0965738048514198, 90.91887785089727, 1.118439172740824, 42.92538304213781, self.filename, '-n',
                     "all"]

        with self.assertRaisesRegex(CommandError, "latitude coordinate out of range: it must be between -90 and 90"):
            call_command('download', arguments)

        self.assertFalse(os.path.exists(self.filename))

    def test_order_lon_argument(self):
        arguments = [1.118439172740824, 42.91887785089727, 1.0965738048514198, 42.92538304213781, self.filename, '-n',
                     "all"]

        with self.assertRaisesRegex(CommandError, "longitude coordinates are in the incorrect order"):
            call_command('download', arguments)

        self.assertFalse(os.path.exists(self.filename))

    def test_order_lat_argument(self):
        arguments = [1.0965738048514198, 42.92538304213781, 1.118439172740824, 42.91887785089727, self.filename, '-n',
                     "all"]

        with self.assertRaisesRegex(CommandError, "latitude coordinates are in the incorrect order"):
            call_command('download', arguments)

        self.assertFalse(os.path.exists(self.filename))

    def test_missing_bbox_argument(self):
        arguments = [1.0965738048514198, 42.92538304213781, 1.118439172740824, self.filename, '-n',
                     "all"]

        with self.assertRaisesRegex(CommandError, f"Error: argument bbox: invalid float value: '{self.filename}'"):
            call_command('download', arguments)

        self.assertFalse(os.path.exists(self.filename))

    # ---------- FILENAME ARGUMENT ----------
    def test_filename_missing_extension(self):
        filename_without_extension = os.path.join(os.path.dirname(__file__), 'data', 'test')
        arguments = [1.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781, filename_without_extension, '-n',
                     "all"]

        call_command('download', arguments)

        self.assertTrue(os.path.exists(self.filename))
        with open(self.filename, "r") as f:
            self.assertEqual(json.load(f), {'test': 'validated'})
        os.remove(self.filename)

    def test_missing_filename_argument(self):
        arguments = [1.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781, '-n', "all"]

        with self.assertRaisesRegex(CommandError, f"Error: the following arguments are required: filename"):
            call_command('download', arguments)

        self.assertFalse(os.path.exists(self.filename))

    # ---------- NETWORK_TYPE ARGUMENT ----------
    def test_long_network_type_argument(self):
        arguments = [1.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781, self.filename, '--network_type',
                     "all"]

        call_command('download', arguments)

        self.assertTrue(os.path.exists(self.filename))
        with open(self.filename, "r") as f:
            self.assertEqual(json.load(f), {'test': 'validated'})
        os.remove(self.filename)

    def test_default_network_type_argument(self):
        arguments = [1.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781, self.filename]

        call_command('download', arguments)

        self.assertTrue(os.path.exists(self.filename))
        with open(self.filename, "r") as f:
            self.assertEqual(json.load(f), {'test': 'validated_default_network'})
        os.remove(self.filename)

    def test_wrong_network_type_argument(self):
        arguments = [1.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781, self.filename, '-n', 'test']

        with self.assertRaisesMessage(CommandError, "Error: argument --network_type/-n: invalid choice: 'test' (choose from 'all', 'drive', 'bike', 'walk')"):
            call_command('download', arguments)

        self.assertFalse(os.path.exists(self.filename))