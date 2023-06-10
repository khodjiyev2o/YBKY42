from django.urls import path

from .api_endpoints import Availability, Booking, Detail, List


application_urlpatterns = [
    path("", List.RoomListView.as_view(), name="rooms-list"),
    path("<int:pk>/", Detail.RoomDetailView.as_view(), name="rooms-detail"),
    path("<int:pk>/availability/", Availability.RoomAvailabilityRetrieveView.as_view(), name="rooms-availability"),
    path("<int:pk>/book/", Booking.CreateBookingView.as_view(), name="rooms-book"),
]

urlpatterns = application_urlpatterns
