from django.urls import path

from .api_endpoints import List


application_urlpatterns = [
    path("", List.RoomListView.as_view(), name="rooms-list"),
]

urlpatterns = application_urlpatterns
