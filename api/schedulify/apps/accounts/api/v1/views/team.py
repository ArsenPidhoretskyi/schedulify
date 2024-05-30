from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Q

from schedulify.apps.accounts.api.v1.serializers.team import (
    TeamInviteSerializer,
    TeamReadSerializer,
    TeamRemoveMemberSerializer,
    TeamSerializer,
)
from schedulify.apps.accounts.models import Team, User
from schedulify.apps.commons.api.mixins import MultiSerializerMixin


class TeamViewSet(MultiSerializerMixin, viewsets.ModelViewSet):
    queryset = Team.objects.prefetch_related("members").select_related("owner")
    serializer_class = TeamReadSerializer
    permission_classes = (IsAuthenticated,)
    serializer_classes = {
        "create": TeamSerializer,
        "update": TeamSerializer,
        "partial_update": TeamSerializer,
        "invite": TeamInviteSerializer,
        "remove_member": TeamRemoveMemberSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(Q(owner=self.request.user) | Q(members=self.request.user))

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        title = self.request.query_params.get("title")
        if title:
            queryset = queryset.filter(name__icontains=title)
        return queryset

    @action(detail=True, methods=["POST"])
    def invite(self, request, *args, **kwargs):
        team = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(email=serializer.validated_data["email"]).first()
        team.members.add(user)

        return Response(status=204)

    @action(detail=True, methods=["POST"])
    def remove_member(self, request, *args, **kwargs):
        team = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        team.members.remove(serializer.validated_data["member"])

        return Response(status=204)
