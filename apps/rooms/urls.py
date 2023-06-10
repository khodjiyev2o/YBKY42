from django.urls import path

from .api_endpoints import List, Detail, Availability


application_urlpatterns = [
    path("", List.RoomListView.as_view(), name="rooms-list"),
    path("<int:pk>/", Detail.RoomDetailView.as_view(), name="rooms-detail"),
    path("<int:pk>/availability/", Availability.RoomAvailabilityRetrieveView.as_view(), name="rooms-availability"),
]

urlpatterns = application_urlpatterns
