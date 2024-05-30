from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = "schedulify.apps.accounts"

    def ready(self) -> None:
        from schedulify.apps.accounts.api.v1.schema import SessionAuthenticationExtension  # noqa: F401
