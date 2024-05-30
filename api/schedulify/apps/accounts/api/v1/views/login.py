from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView

from schedulify.apps.accounts.api.permissions import IsNotAuthenticated
from schedulify.apps.accounts.api.v1.serializers.login import LoginSerializer
from schedulify.apps.accounts.services.login import LoginService
from schedulify.apps.commons.api.serializers import NullSerializer


class LoginView(GenericAPIView):
    permission_classes = [IsNotAuthenticated]
    serializer_class = LoginSerializer

    @extend_schema(summary="Login", tags=["Accounts"], responses={status.HTTP_204_NO_CONTENT: OpenApiResponse()})
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        return LoginService.login(request, user)


class LogoutView(GenericAPIView):
    serializer_class = NullSerializer

    @extend_schema(summary="Log out", tags=["Accounts"], responses={status.HTTP_204_NO_CONTENT: OpenApiResponse()})
    def post(self, request):
        return LoginService.logout(request)
