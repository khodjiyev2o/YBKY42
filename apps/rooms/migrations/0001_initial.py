# Generated by Django 4.2 on 2023-06-09 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("focus", "Focus"),
                            ("team", "Team"),
                            ("conference", "Conference"),
                        ],
                        max_length=63,
                        verbose_name="Room Type",
                    ),
                ),
                ("capacity", models.PositiveIntegerField(verbose_name="Capacity")),
            ],
            options={
                "verbose_name": "Room",
                "verbose_name_plural": "Rooms",
            },
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                ("start_time", models.DateTimeField(verbose_name="Start Time")),
                ("end_time", models.DateTimeField(verbose_name="End Time")),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookings",
                        to="rooms.room",
                    ),
                ),
            ],
            options={
                "verbose_name": "Room",
                "verbose_name_plural": "Rooms",
            },
        ),
    ]