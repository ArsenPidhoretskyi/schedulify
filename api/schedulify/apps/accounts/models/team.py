from django.db import models

from schedulify.apps.accounts.models import User
from schedulify.apps.commons.models import CoreModel


class Team(CoreModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, related_name="owned_teams", on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name="teams", blank=True)

    class Meta:
        unique_together = ("name", "owner")
        ordering = ("name",)
