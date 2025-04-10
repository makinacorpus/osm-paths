from django.urls import path
from . import views

app_name = "download"
urlpatterns = [
    path('', views.PathsAPIView.as_view(), name="download_paths"),
]
