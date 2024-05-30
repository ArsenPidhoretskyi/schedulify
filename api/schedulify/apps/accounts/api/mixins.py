from rest_framework.serializers import Serializer

from schedulify.apps.accounts.models import User


class RequestUserMixin(Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.request = self.context.get("request")
        self.user: User = getattr(self.request, "user")
