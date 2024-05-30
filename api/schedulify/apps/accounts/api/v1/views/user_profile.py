from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from schedulify.apps.accounts.api.v1.serializers.user_profile import UserProfileSerializer
from schedulify.apps.accounts.models import User


@extend_schema_view(
    get=extend_schema(
        summary="Me",
        tags=["Accounts"],
    ),
    put=extend_schema(
        summary="Update me",
        tags=["Accounts"],
    ),
    patch=extend_schema(
        summary="Update me",
        tags=["Accounts"],
    ),
)
class UserProfileAPIView(RetrieveUpdateAPIView):
    queryset = User.objects
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class UsersAPIView(ListModelMixin, GenericAPIView):
    queryset = User.objects
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        email = request.query_params.get("email")
        queryset = self.get_queryset().filter(email__icontains=email)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
