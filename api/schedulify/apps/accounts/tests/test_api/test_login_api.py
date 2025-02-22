import pytest

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from django.urls import reverse
from django.utils.translation import gettext


LOGIN_SERIALIZER_PATH = "schedulify.apps.accounts.api.v1.serializers.login.LoginSerializer"


@pytest.mark.django_db
def test_login_api_success(user_account, unauthorized_api_client, mocker):
    user = user_account()
    mocked_validate = mocker.patch(f"{LOGIN_SERIALIZER_PATH}.validate", return_value={"user": user})
    mocked_response = Response(status=status.HTTP_204_NO_CONTENT)
    mocked_login = mocker.patch(
        "schedulify.apps.accounts.services.login.LoginService.login", return_value=mocked_response
    )

    data = {"email": "jane@example.com", "password": "super-secret-password"}
    response = unauthorized_api_client.post(reverse("api-v1-accounts:login"), data)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    mocked_validate.assert_called_once_with(data)
    mocked_login.assert_called_once_with(mocker.ANY, user)


@pytest.mark.django_db
def test_login_api_wrong_credentials_failure(user_account, unauthorized_api_client, mocker):
    mocked_validate = mocker.patch(
        f"{LOGIN_SERIALIZER_PATH}.validate", side_effect=[ValidationError(gettext("Incorrect email or password."))]
    )
    mocked_login = mocker.patch("django.contrib.auth.login")

    data = {"email": "jane@example.com", "password": "super-secret-password"}
    response = unauthorized_api_client.post(reverse("api-v1-accounts:login"), data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {"non_field_errors": [gettext("Incorrect email or password.")]}
    mocked_validate.assert_called_once_with(data)
    assert mocked_login.call_count == 0


@pytest.mark.django_db
def test_login_api_already_logged_in_failure(user_account, api_client, mocker):
    user = user_account()
    client = api_client(auth_user=user)
    mocked_validate = mocker.patch(f"{LOGIN_SERIALIZER_PATH}.validate")
    mocked_login = mocker.patch("django.contrib.auth.login")

    response = client.post(reverse("api-v1-accounts:login"))

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert mocked_validate.call_count == 0
    assert mocked_login.call_count == 0
