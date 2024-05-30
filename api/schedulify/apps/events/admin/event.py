from django.contrib import admin

from schedulify.apps.events.models.event import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "owner",
        "start",
        "end",
        "location",
    )
