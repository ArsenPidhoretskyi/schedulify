from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout


class LoginService:
    @classmethod
    def login(cls, request, user):
        django_login(request, user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @classmethod
    def logout(cls, request):
        django_logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
