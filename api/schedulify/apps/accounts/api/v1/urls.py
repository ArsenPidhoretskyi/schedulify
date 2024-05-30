from rest_framework.routers import DefaultRouter

from django.urls import path

from schedulify.apps.accounts.api.v1.views.login import LoginView, LogoutView
from schedulify.apps.accounts.api.v1.views.password import (
    ChangePasswordAPIView,
    ConfirmResetPasswordAPIView,
    ResetPasswordAPIView,
)
from schedulify.apps.accounts.api.v1.views.registration import RegistrationAPIView
from schedulify.apps.accounts.api.v1.views.team import TeamViewSet
from schedulify.apps.accounts.api.v1.views.token import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from schedulify.apps.accounts.api.v1.views.user_profile import UserProfileAPIView, UsersAPIView


router = DefaultRouter()
router.register("teams", TeamViewSet, basename="teams")


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", UserProfileAPIView.as_view(), name="user-profile"),
    path("users/", UsersAPIView.as_view(), name="user-teams"),
    path("password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("password/confirm/", ConfirmResetPasswordAPIView.as_view(), name="confirm-reset-password"),
    path("password/reset/", ResetPasswordAPIView.as_view(), name="reset-password"),
    path("registration/", RegistrationAPIView.as_view(), name="registration"),
    path("token/create/", TokenObtainPairView.as_view(), name="token-create"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),
] + router.urls
