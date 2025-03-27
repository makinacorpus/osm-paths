from random import choices

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from download.validity import bbox_validity_check


class DownloadSerializer(serializers.Serializer):
    bbox = serializers.CharField(
        required=True,
        help_text=_("Bounding box coordinates in WGS84: minlon,minlat,maxlon,maxlat"),
    )
    network_type = serializers.ChoiceField(
        required=False,
        allow_blank=True,
        choices=['all', 'drive', 'bike', 'walk'],
        help_text=_("Type of paths that will be downloaded: 'all', 'drive', 'bike', 'walk'"),
        initial="walk",
    )

    def validate_bbox(self, value):
        try:
            bbox = tuple(float(coord) for coord in value.split(','))
            if len(bbox) != 4:
                raise serializers.ValidationError()
        except:
            raise serializers.ValidationError("Bounding box coordinates have 4 coordinates seperated by ',': minlon,minlat,maxlon,maxlat")

        bbox_validity_check(bbox, serializers.ValidationError)

        return value
