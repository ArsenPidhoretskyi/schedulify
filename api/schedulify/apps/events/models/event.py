from django.db import models

from schedulify.apps.accounts.models import User
from schedulify.apps.accounts.models.team import Team
from schedulify.apps.commons.models import CoreModel


class Event(CoreModel):
    title = models.CharField(max_length=255, blank=False, default="")
    description = models.TextField(blank=True, default="")
    start = models.DateTimeField(null=True, db_index=True)
    end = models.DateTimeField(null=True, db_index=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_events")
    location = models.CharField(max_length=255, blank=True, default="")
    attendees = models.ManyToManyField(User, blank=True, default=[], related_name="events")
    teams = models.ManyToManyField(Team, blank=True, default=[], related_name="events")

    class Meta:
        db_table = "events"

    @property
    def participants(self) -> list[User]:
        return list(self.attendees.all()) + [self.owner]
