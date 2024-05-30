from rest_framework import serializers

from schedulify.apps.accounts.api.v1.serializers.user_profile import UserProfileSerializer
from schedulify.apps.accounts.models import User
from schedulify.apps.accounts.models.team import Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("id", "name", "description", "members")
        read_only_fields = ("id", "owner")


class TeamReadSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer()
    members = UserProfileSerializer(many=True)

    class Meta:
        model = Team
        fields = ("id", "name", "description", "members", "owner")
        read_only_fields = ("id", "owner")

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("owner", None)
        return super().update(instance, validated_data)


class TeamInviteSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value).exists():
            return value
        raise serializers.ValidationError("User with this email does not exist")


class TeamRemoveMemberSerializer(serializers.Serializer):
    member = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate_member(self, value: User) -> User:
        if self.context["request"].user == value:
            raise serializers.ValidationError("You can't remove yourself from the team")
        return value
