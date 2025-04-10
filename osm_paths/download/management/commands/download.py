import os

from django.core.management.base import BaseCommand, CommandError
from osm_paths.download.osm_to_geojson import osm_paths_to_geojson, save_geojson
from osm_paths.download.validity import bbox_validity_check
from shapely import Polygon, from_wkt, from_geojson


class Command(BaseCommand):
    help = "Download paths from OpenStreetMap and return a geojson file"

    def add_arguments(self, parser):
        parser.add_argument(
            "filename", help="Output filename (must have geojson extension)"
        )

        parser.add_argument(
            "-b",
            "--bbox",
            type=str,
            help="Bounding box coordinates in WGS84: minlon,minlat,maxlon,maxlat",
        )

        parser.add_argument(
            "-p",
            "--polygon",
            type=str,
            help="File with the polygon coordinates in WKT or geojson format (WGS84)",
        )

        parser.add_argument(
            "-n",
            "--network_type",
            choices=["all", "drive", "bike", "walk"],
            default="walk",
            help="Type of paths that will be downloaded: all, drive, bike, walk (default: walk)",
        )

    def handle(self, *args, **options):
        polygon = None

        bbox_str = options.get("bbox")
        if bbox_str:
            minlon, minlat, maxlon, maxlat = bbox_validity_check(
                options["bbox"], CommandError
            )
            polygon = Polygon.from_bounds(minlon, minlat, maxlon, maxlat)

        polygon_filename = options.get("polygon")
        if polygon_filename:
            if not os.path.exists(polygon_filename):
                raise CommandError(f"{polygon_filename} does not exist")

            with open(polygon_filename, "r") as f:
                file = f.read()

            if ".wkt" in polygon_filename:
                try:
                    polygon = from_wkt(file)
                except Exception:
                    raise CommandError(
                        f"{polygon_filename} does not contain a valid WKT polygon"
                    )
            elif ".geojson" in polygon_filename:
                try:
                    polygon = from_geojson(file)
                except Exception:
                    raise CommandError(
                        f"{polygon_filename} does not contain a valid geojson polygon"
                    )
            else:
                raise CommandError(
                    f"{polygon_filename} must be a .wkt or .geojson file"
                )

        if not polygon:
            raise CommandError("Bounding box or Polygon is required")

        filename = options.get("filename")
        if not filename.endswith(".geojson"):
            filename = f"{filename}.geojson"

        network_type = options.get("network_type")

        geojson = osm_paths_to_geojson(polygon, network_type)

        save_geojson(geojson, filename)
