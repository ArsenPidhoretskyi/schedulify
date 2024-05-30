from rest_framework.authentication import SessionAuthentication as RestSessionAuthentication


class SessionAuthentication(RestSessionAuthentication):
    def enforce_csrf(self, request):
        """
        Exempt CSRF for session based authentication "application/json".
        """
        if request.content_type != "application/json":
            super().enforce_csrf(request)
