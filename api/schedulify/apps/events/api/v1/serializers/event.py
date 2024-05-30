from datetime import time, timedelta
from typing import List

from rest_framework import serializers

from django.db.models import Q
from django.utils import timezone

from schedulify.apps.accounts.api.v1.serializers.team import TeamReadSerializer
from schedulify.apps.accounts.api.v1.serializers.user_profile import UserProfileSerializer
from schedulify.apps.accounts.models import Team
from schedulify.apps.events.models.event import Event


class EventReadSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer()
    attendees = UserProfileSerializer(many=True)
    teams = TeamReadSerializer(many=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "start",
            "end",
            "owner",
            "attendees",
            "teams",
        )
        read_only_fields = ("owner",)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "start",
            "end",
            "owner",
            "attendees",
            "teams",
        )
        read_only_fields = ("owner",)

    def validate(self, data):
        if data["start"] > data["end"]:
            raise serializers.ValidationError("End time must occur after start time.")
        return data

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("owner", None)
        return super().update(instance, validated_data)


class EventAvailableSlotsSerializer(serializers.Serializer):
    duration = serializers.IntegerField()
    delta = serializers.IntegerField(default=15)
    limit = serializers.IntegerField(default=10)
    after = serializers.DateTimeField(default=timezone.now())
    participants = serializers.ListSerializer(child=serializers.IntegerField(), required=False)
    teams = serializers.ListSerializer(child=serializers.IntegerField(), required=False)
    time_start = serializers.TimeField(default=time(10))
    time_end = serializers.TimeField(default=time(19))

    class Meta:
        fields = (
            "duration",
            "delta",
            "limit",
            "after",
            "participants",
        )

    def save(self) -> List[tuple]:
        data = self.validated_data

        teams = data.get("teams") or []
        for team in Team.objects.filter(id__in=teams).prefetch_related("members"):
            for user in team.members.all():
                data["participants"].append(user.id)
            data["participants"].append(team.owner_id)

        participants = data.get("participants") or []
        participants.append(self.context["request"].user.id)

        duration = data["duration"]
        delta = data.get("delta") or 15
        limit = data.get("limit") or 10
        after = data.get("after") or timezone.now()
        time_start = data.get("time_start") or time(10)
        time_end = data.get("time_end") or time(20)
        if time_end == time():
            time_end = time(23, 59, 59)

        participants_events = Event.objects.filter(
            Q(attendees__in=participants) | Q(owner__in=participants),
            start__gte=after,
        ).order_by("start")
        start_time = after.replace(tzinfo=timezone.get_current_timezone())
        slots = []
        while len(slots) != limit:
            end_time = start_time + timedelta(minutes=duration)

            if not time_start <= start_time.time() <= time_end or not time_start <= end_time.time() <= time_end:
                start_time += timedelta(days=1)
                start_time = start_time.replace(hour=time_start.hour, minute=time_start.minute)
                continue

            slot_found = True
            for event in participants_events:
                if (
                    event.start <= start_time < event.end
                    or event.start < end_time <= event.end
                    or start_time <= event.start <= end_time
                ):
                    slot_found = False
                    break

            if slot_found:
                slots.append((start_time, end_time))

            start_time += timedelta(minutes=delta)

        return slots
