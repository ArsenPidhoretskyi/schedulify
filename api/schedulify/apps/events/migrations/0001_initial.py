# Generated by Django 4.2.11 on 2024-05-21 15:25

import uuid

import django.db.models.deletion

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created")),
                ("updated", models.DateTimeField(auto_now=True, verbose_name="Updated")),
                ("is_active", models.BooleanField(db_index=True, default=True, verbose_name="Active")),
                ("title", models.CharField(default="", max_length=255)),
                ("description", models.TextField(blank=True, default="")),
                ("start", models.DateTimeField(db_index=True, null=True)),
                ("end", models.DateTimeField(db_index=True, null=True)),
                ("location", models.CharField(blank=True, default="", max_length=255)),
                (
                    "attendees",
                    models.ManyToManyField(blank=True, default=[], related_name="events", to=settings.AUTH_USER_MODEL),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owned_events",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "events",
            },
        ),
    ]
