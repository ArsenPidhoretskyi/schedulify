from unittest import mock

import pytest

from rest_framework import status

from django.test.client import RequestFactory
from django.urls import reverse

from schedulify.apps.accounts.services.login import LoginService


@pytest.mark.django_db
@mock.patch("schedulify.apps.accounts.services.login.django_login")
def test_login_service_login(mocked_django_login, user_account, mocker):
    request = mocker.MagicMock()
    user = user_account()
    service = LoginService

    response = service.login(request, user)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    print(mocked_django_login.calls)
    mocked_django_login.assert_called_once_with(request, user)


@mock.patch("schedulify.apps.accounts.services.login.django_logout")
def test_login_service_logout(mocked_django_logout, user_account):
    user = user_account()
    request = RequestFactory().post(reverse("api-v1-accounts:logout"))
    request.user = user
    service = LoginService

    response = service.logout(request)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    mocked_django_logout.assert_called_once_with(request)
