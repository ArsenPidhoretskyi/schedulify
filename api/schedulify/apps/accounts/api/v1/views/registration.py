from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView

from schedulify.apps.accounts.api.permissions import IsNotAuthenticated
from schedulify.apps.accounts.api.v1.serializers.registration import RegistrationSerializer
from schedulify.apps.accounts.services.login import LoginService


class RegistrationAPIView(GenericAPIView):
    permission_classes = [IsNotAuthenticated]
    serializer_class = RegistrationSerializer

    @extend_schema(
        summary="Registration", tags=["Accounts"], responses={status.HTTP_204_NO_CONTENT: OpenApiResponse()}
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return LoginService.login(request, user)
