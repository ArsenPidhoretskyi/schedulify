# Generated by Django 4.2.11 on 2024-05-27 23:32

import uuid

import django.db.models.deletion

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Team",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created")),
                ("updated", models.DateTimeField(auto_now=True, verbose_name="Updated")),
                ("is_active", models.BooleanField(db_index=True, default=True, verbose_name="Active")),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("members", models.ManyToManyField(blank=True, related_name="teams", to=settings.AUTH_USER_MODEL)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owned_teams",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
                "unique_together": {("name", "owner")},
            },
        ),
    ]
