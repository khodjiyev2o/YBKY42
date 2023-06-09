from django.contrib import admin

from apps.rooms.models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type")
