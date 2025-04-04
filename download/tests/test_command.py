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
    filename_wkt = os.path.join(os.path.dirname(__file__), 'data', 'polygon.wkt')
    filename_geojson = os.path.join(os.path.dirname(__file__), 'data', 'polygon.geojson')

    # ---------- BBOX ARGUMENT ----------
    def test_standard_bbox_arguments(self):
        arguments = ['-b', "1.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781", self.filename, '-n', "all"]

        call_command('download', arguments)

        self.assertTrue(os.path.exists(self.filename))
        with open(self.filename, "r") as f:
            self.assertEqual(json.load(f), {'test': 'validated'})
        os.remove(self.filename)

    def test_standard_long_bbox_arguments(self):
        arguments = ['--bbox', "1.0965738048514198,42.91887785089727,1.118439172740824,42.92538304213781",self.filename,'-n',"all"]

        call_command('download', arguments)

        self.assertTrue(os.path.exists(self.filename))
        with open(self.filename, "r") as f:
            self.assertEqual(json.load(f), {'test': 'validated'})
        os.remove(self.filename)

    def test_lower_lon_argument(self):
        arguments = ['-b', "-180.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781", self.filename, '-n', "all"]

        with self.assertRaisesRegex(CommandError, "longitude coordinate out of range: it must be between -180 and 180"):
            call_command('download', arguments)

        self.assertFalse(os.path.exists(self.filename))

    def test_higher_lon_argument(self):
        arguments = ['-b', "180.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781", self.filename, '-n', "all"]

        with self.assertRaisesRegex(CommandError, "longitude coordinate out of range: it must be between -180 and 180"):
            call_command('download', arguments)

        self.assertFalse(os.path.exists(self.filename))

    def test_lower_lat_argument(self):
        arguments = ['-b', "1.0965738048514198, -92.91887785089727, 1.118439172740824, 42.92538304213781", self.filename, '-n',
                     "all"]

        with self.assertRaisesRegex(CommandError, "latitude coordinate out of range: it must be between -90 and 90"):
            call_command('download', arguments)

        self.assertFalse(os.path.exists(self.filename))

    def test_higher_lat_argument(self):
        arguments = ['-b', "1.0965738048514198, 90.91887785089727, 1.118439172740824, 42.92538304213781", self.filename, '-n',
                     "all"]

        with self.assertRaisesRegex(CommandError, "latitude coordinate out of range: it must be between -90 and 90"):
            call_command('download', arguments)

        self.assertFalse(os.path.exists(self.filename))

    def test_order_lon_argument(self):
        arguments = ['-b', "1.118439172740824, 42.91887785089727, 1.0965738048514198, 42.92538304213781", self.filename, '-n',
                     "all"]

        with self.assertRaisesRegex(CommandError, "longitude coordinates are in the incorrect order"):
            call_command('download', arguments)

        self.assertFalse(os.path.exists(self.filename))

    def test_order_lat_argument(self):
        arguments = ['-b', "1.0965738048514198, 42.92538304213781, 1.118439172740824, 42.91887785089727", self.filename, '-n',
                     "all"]

        with self.assertRaisesRegex(CommandError, "latitude coordinates are in the incorrect order"):
            call_command('download', arguments)

        self.assertFalse(os.path.exists(self.filename))

    def test_missing_bbox_argument(self):
        arguments = ['-b', "1.0965738048514198, 42.92538304213781, 1.118439172740824", self.filename, '-n',
                     "all"]

        with self.assertRaisesRegex(CommandError, "Bounding box coordinates have 4 coordinates seperated by ',': minlon,minlat,maxlon,maxlat"):
            call_command('download', arguments)

        self.assertFalse(os.path.exists(self.filename))

    # ---------- POLYGON ARGUMENT ----------
    def test_standard_polygon_wkt_arguments(self):
        arguments = ['-p', self.filename_wkt, self.filename, '-n', "all"]

        call_command('download', arguments)

        self.assertTrue(os.path.exists(self.filename))
        with open(self.filename, "r") as f:
            self.assertEqual(json.load(f), {'test': 'validated'})
        os.remove(self.filename)

    def test_standard_polygon_geojson_arguments(self):
        arguments = ['-p', self.filename_geojson, self.filename, '-n', "all"]

        call_command('download', arguments)

        self.assertTrue(os.path.exists(self.filename))
        with open(self.filename, "r") as f:
            self.assertEqual(json.load(f), {'test': 'validated'})
        os.remove(self.filename)

    def test_standard_polygon_wkt_long_arguments(self):
        arguments = ['--polygon', self.filename_wkt, self.filename, '-n', "all"]

        call_command('download', arguments)

        self.assertTrue(os.path.exists(self.filename))
        with open(self.filename, "r") as f:
            self.assertEqual(json.load(f), {'test': 'validated'})
        os.remove(self.filename)

    def test_standard_polygon_geojson_long_arguments(self):
        arguments = ['--polygon', self.filename_geojson, self.filename, '-n', "all"]

        call_command('download', arguments)

        self.assertTrue(os.path.exists(self.filename))
        with open(self.filename, "r") as f:
            self.assertEqual(json.load(f), {'test': 'validated'})
        os.remove(self.filename)

    def test_invalid_polygon_geojson_argument(self):
        filename_invalid_geojson = os.path.join(os.path.dirname(__file__), 'data', 'invalid_polygon.geojson')
        arguments = ['--polygon', filename_invalid_geojson, self.filename, '-n', "all"]

        with self.assertRaisesRegex(CommandError,f"{filename_invalid_geojson} does not contain a valid geojson polygon"):
            call_command('download', arguments)

    def test_invalid_polygon_wkt_argument(self):
        filename_invalid_wkt = os.path.join(os.path.dirname(__file__), 'data', 'invalid_polygon.wkt')
        arguments = ['--polygon', filename_invalid_wkt, self.filename, '-n', "all"]

        with self.assertRaisesRegex(CommandError,f"{filename_invalid_wkt} does not contain a valid WKT polygon"):
            call_command('download', arguments)

    def test_invalid_filename_argument(self):
        invalid_filename = os.path.join(os.path.dirname(__file__), 'data', 'invalid_filename.wkt')
        arguments = ['--polygon', invalid_filename, self.filename, '-n', "all"]

        with self.assertRaisesRegex(CommandError,f"{invalid_filename} does not exist"):
            call_command('download', arguments)

    def test_invalid_filename_extension_argument(self):
        invalid_filename = os.path.join(os.path.dirname(__file__), 'data', 'invalid_filename.txt')
        arguments = ['--polygon', invalid_filename, self.filename, '-n', "all"]

        with self.assertRaisesRegex(CommandError,f"{invalid_filename} must be a .wkt or .geojson file"):
            call_command('download', arguments)

    # ---------- NO BOUNDARY ARGUMENT ----------
    def test_no_boundary_argument(self):
        arguments = [self.filename, '-n', "all"]

        with self.assertRaisesRegex(CommandError,"Bounding box or Polygon is required"):
            call_command('download', arguments)

    # ---------- FILENAME ARGUMENT ----------
    def test_filename_missing_extension(self):
        filename_without_extension = os.path.join(os.path.dirname(__file__), 'data', 'test')
        arguments = ['-b', "1.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781", filename_without_extension, '-n',
                     "all"]

        call_command('download', arguments)

        self.assertTrue(os.path.exists(self.filename))
        with open(self.filename, "r") as f:
            self.assertEqual(json.load(f), {'test': 'validated'})
        os.remove(self.filename)

    def test_missing_filename_argument(self):
        arguments = ['-b', "1.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781", '-n', "all"]

        with self.assertRaisesRegex(CommandError, f"Error: the following arguments are required: filename"):
            call_command('download', arguments)

        self.assertFalse(os.path.exists(self.filename))

    # ---------- NETWORK_TYPE ARGUMENT ----------
    def test_long_network_type_argument(self):
        arguments = ['-b', "1.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781", self.filename, '--network_type',
                     "all"]

        call_command('download', arguments)

        self.assertTrue(os.path.exists(self.filename))
        with open(self.filename, "r") as f:
            self.assertEqual(json.load(f), {'test': 'validated'})
        os.remove(self.filename)

    def test_default_network_type_argument(self):
        arguments = ['-b', "1.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781", self.filename]

        call_command('download', arguments)

        self.assertTrue(os.path.exists(self.filename))
        with open(self.filename, "r") as f:
            self.assertEqual(json.load(f), {'test': 'validated_default_network'})
        os.remove(self.filename)

    def test_wrong_network_type_argument(self):
        arguments = ['-b', "1.0965738048514198, 42.91887785089727, 1.118439172740824, 42.92538304213781", self.filename, '-n', 'test']

        with self.assertRaisesMessage(CommandError, "Error: argument -n/--network_type: invalid choice: 'test' (choose from 'all', 'drive', 'bike', 'walk')"):
            call_command('download', arguments)

        self.assertFalse(os.path.exists(self.filename))
