import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from django.http import JsonResponse
from .serializers import DownloadSerializer

from download.osm_to_geojson import osm_paths_to_geojson

class PathsAPIView(APIView):
    serializer_class = DownloadSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def get_serializer(self, *args, **kwargs):
        """
        Keep this method to see json structure in API html view
        """
        return self.serializer_class()

    def serializer_invalid(self, serializer):
        return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)

    def serializer_valid(self, serializer):
        try:
            response_data = json.loads(osm_paths_to_geojson(**serializer.validated_data))
            response = JsonResponse(response_data, status=http_status.HTTP_200_OK, json_dumps_params={'indent': 4})
            response['Content-Disposition'] = 'attachment; filename=paths.geojson'
        except Exception as exc:
            response = Response({'errors': f'{exc}'}, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        return self.serializer_valid(serializer) \
            if serializer.is_valid() else self.serializer_invalid(serializer)