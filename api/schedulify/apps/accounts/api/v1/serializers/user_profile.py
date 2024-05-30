from rest_framework import serializers

from schedulify.apps.accounts.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")
