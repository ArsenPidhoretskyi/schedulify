from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.utils.translation import gettext

from schedulify.apps.accounts.exceptions import (
    InvalidPasswordError,
    InvalidResetPasswordSignatureError,
    WrongPasswordError,
)
from schedulify.apps.accounts.models import User


class PasswordService:
    @staticmethod
    def change_password(user: User, new_password: str) -> None:
        user.set_password(new_password)
        user.save(update_fields=("password",))

    @staticmethod
    def check_password(user: User, password: str) -> None:
        if not user.check_password(password):
            raise WrongPasswordError(gettext("Incorrect password."))

    @staticmethod
    def validate_password(password, user=None) -> None:
        try:
            password_validation.validate_password(password, user=user)
        except DjangoValidationError as error:
            raise InvalidPasswordError(error.messages) from error

    @classmethod
    def send_reset_password_link(cls, email: str) -> None:
        user = User.objects.active().filter(email=email).first()
        if not user:
            return

        reset_password_signature = cls._generate_reset_password_signature(user)
        domain_name = Site.objects.get_current().domain
        reset_password_link = f"https://{domain_name}/reset-password/{reset_password_signature}"
        context = {
            "user_notification_salutation": user.notification_salutation,
            "domain_name": domain_name,
            "reset_password_link": reset_password_link,
        }
        cls._send_notification(user.pk, context)

    @classmethod
    def reset_password(cls, signature: str, new_password: str) -> None:
        signer = TimestampSigner()
        try:
            user_pk = signer.unsign(signature, max_age=settings.SCHEDULIFY_RESET_PASSWORD_EXPIRATION_DELTA)
            user = User.objects.active().get(pk=user_pk)
        except (SignatureExpired, BadSignature, User.DoesNotExist, ValueError) as error:
            raise InvalidResetPasswordSignatureError(
                gettext("Invalid confirmation code or user does not exist")
            ) from error

        cls.change_password(user, new_password)

    @staticmethod
    def _send_notification(user_pk: str, context: dict):
        # send_notification.delay(user_pk, context)  # TODO: Implement notification sending
        pass

    @staticmethod
    def _generate_reset_password_signature(user: User) -> str:
        signer = TimestampSigner()
        return signer.sign(str(user.pk))
