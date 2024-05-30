from drf_spectacular.authentication import OpenApiAuthenticationExtension
from drf_spectacular.types import OpenApiTypes

from schedulify.apps.accounts.api.authentication import SessionAuthentication


class SessionAuthenticationExtension(OpenApiAuthenticationExtension):
    name = "SessionAuthentication"
    target_class = SessionAuthentication

    def get_security_definition(self, auto_schema):
        return []

    def get_operation_parameters(self, auto_schema):
        return [
            {
                "name": "sessionid",
                "in": "header",
                "type": OpenApiTypes.UUID,
                "required": False,
                "description": "Session ID for authentication.",
            }
        ]
