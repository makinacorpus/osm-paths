from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from shapely import from_wkt, errors


class DownloadSerializer(serializers.Serializer):
    polygon = serializers.CharField(
        required=True,
        help_text=_("Polygon coordinates in WKT format (WGS84)"),
    )
    network_type = serializers.ChoiceField(
        required=False,
        allow_blank=True,
        choices=["all", "drive", "bike", "walk"],
        help_text=_(
            "Type of paths that will be downloaded: 'all', 'drive', 'bike', 'walk'"
        ),
        initial="walk",
    )

    def validate_polygon(self, value):
        try:
            polygon = from_wkt(value)
            if not polygon.is_valid:
                raise serializers.ValidationError()
        except serializers.ValidationError:
            raise serializers.ValidationError(_("Invalid polygon format"))
        except errors.GEOSException:
            raise serializers.ValidationError(_("Invalid polygon format"))

        return polygon
