from django.core.management.base import BaseCommand, CommandError
from download.osm_to_geojson import osm_paths_to_geojson, save_geojson
from download.validity import bbox_validity_check

class Command(BaseCommand):
    help = "Download paths from OpenStreetMap and return a geojson file"

    def add_arguments(self, parser):
        parser.add_argument("bbox",
                            nargs=4,
                            type=float,
                            help="Bounding box coordinates in WGS84: minlon minlat maxlon maxlat",)

        parser.add_argument("filename",
                            help="Output filename (must have geojson extension)")

        parser.add_argument("--network_type", "-n",
                            choices=['all', 'drive', 'bike', 'walk'],
                            default="walk",
                            help="Type of paths that will be downloaded: 'all', 'drive', 'bike', 'walk' (default: 'walk')")
        # ajouter la description des parametres dans le help

    def handle(self, *args, **options):
        bbox = tuple(options["bbox"])
        bbox_validity_check(bbox, CommandError)

        filename = options["filename"]
        if not filename.endswith(".geojson"):
            filename = f"{filename}.geojson"

        network_type = options.get("network_type")

        geojson = osm_paths_to_geojson(bbox, network_type)

        save_geojson(geojson, filename)
