from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.utils.translation import gettext

from schedulify.apps.accounts.exceptions import InvalidPasswordError
from schedulify.apps.accounts.models import User
from schedulify.apps.accounts.services.password import PasswordService


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, max_length=128)
    password = serializers.CharField(write_only=True, max_length=128)
    first_name = serializers.CharField(required=True, max_length=30)
    last_name = serializers.CharField(required=True, max_length=30)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password_service = PasswordService()

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError(gettext("Could not create account with this email."))
        return super().validate(email)

    def validate_password(self, new_password):
        try:
            self.password_service.validate_password(new_password)
        except InvalidPasswordError as error:
            raise serializers.ValidationError(error.messages) from error
        return new_password

    def save(self, **kwargs):
        self.instance = super().save(**kwargs)
        raw_password = self.validated_data.get("password")
        self.instance.set_password(raw_password)
        self.instance.save()
        return self.instance
