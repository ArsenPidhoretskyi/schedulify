from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib.auth import authenticate as django_authenticate
from django.utils.translation import gettext

from schedulify.apps.commons.api.serializers import CoreSerializer


class LoginSerializer(CoreSerializer):
    email = serializers.EmailField(write_only=True, max_length=254)
    password = serializers.CharField(max_length=128, style={"input_type": "password"}, write_only=True)

    @staticmethod
    def _authenticate(email, password):
        return django_authenticate(email=email, password=password)  # pragma: no cover

    def validate(self, attrs):
        user = self._authenticate(attrs.get("email"), attrs.get("password"))
        if user:
            return {"user": user}
        raise ValidationError(gettext("Incorrect email or password."))
