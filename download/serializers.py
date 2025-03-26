from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from download.validity import bbox_validity_check


class DownloadSerializer(serializers.Serializer):
    bbox = serializers.CharField(
        required=True,
        help_text=_("Bounding box coordinates in WGS84: minlat,minlon,maxlat,maxlon"),
    )
    network_type = serializers.CharField(
        required=False,
        help_text=_("Type of paths that will be downloaded: 'all', 'drive', 'bike', 'walk'"),
        default="walk",
    )

    def validate_bbox(self, value):
        try:
            bbox = tuple(float(coord) for coord in value.split(','))
            if len(bbox) != 4:
                raise serializers.ValidationError()
        except:
            raise serializers.ValidationError("Bounding box coordinates must be seperated by ',': minlat,minlon,maxlat,maxlon")

        bbox_validity_check(bbox, serializers.ValidationError)

        return value
