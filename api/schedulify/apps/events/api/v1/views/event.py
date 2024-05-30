
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Q

from schedulify.apps.accounts.models import User
from schedulify.apps.commons.api.mixins import MultiSerializerMixin
from schedulify.apps.events.api.v1.serializers.event import (
    EventAvailableSlotsSerializer,
    EventReadSerializer,
    EventSerializer,
)
from schedulify.apps.events.models.event import Event


class EventViewSet(MultiSerializerMixin, viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventReadSerializer
    permission_classes = (IsAuthenticated,)
    serializer_classes = {
        "create": EventSerializer,
        "update": EventSerializer,
        "partial_update": EventSerializer,
        "slots": EventAvailableSlotsSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def filter_queryset(self, queryset):
        if self.action == "my":
            queryset = queryset.filter(Q(owner=self.request.user) | Q(attendees=self.request.user))

        if start_date := self.request.query_params.get("start"):
            queryset = queryset.filter(start__date__gte=start_date)

        if end_date := self.request.query_params.get("end"):
            queryset = queryset.filter(end__date__lte=end_date)

        return queryset

    @action(detail=False, methods=["GET"])
    def my(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=False, methods=["POST"])
    def slots(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.save())


class StatisticView(GenericAPIView):
    queryset = Event.objects
    serializer_class = EventReadSerializer

    def get(self, request, *args, **kwargs):
        response = {
            "users": User.objects.count(),
            "allEvents": Event.objects.count(),
            "myEvents": Event.objects.filter(Q(owner=self.request.user) | Q(attendees=self.request.user)).count(),
        }
        return Response(response)
