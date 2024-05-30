import pytest

from schedulify.apps.accounts.models import User


@pytest.mark.django_db
def test_core_queryset_active(user_account):
    assert User.objects.count() == 0

    active_user = user_account(is_active=True)
    user_account(is_active=False)
    user_account(is_active=False)

    assert User.objects.count() == 3
    assert User.objects.active().count() == 1
    assert User.objects.active().first() == active_user


@pytest.mark.django_db
def test_core_queryset_inactive(user_account):
    assert User.objects.count() == 0

    inactive_user = user_account(is_active=False)
    user_account(is_active=True)
    user_account(is_active=True)

    assert User.objects.count() == 3
    assert User.objects.inactive().count() == 1
    assert User.objects.inactive().first() == inactive_user


@pytest.mark.django_db
def test_core_queryset_activate(user_account):
    assert User.objects.count() == 0

    user = user_account(is_active=False)

    assert User.objects.count() == 1
    assert User.objects.active().count() == 0
    assert User.objects.inactive().count() == 1
    assert User.objects.inactive().first() == user

    user.activate()

    assert User.objects.count() == 1
    assert User.objects.active().count() == 1
    assert User.objects.inactive().count() == 0
    assert User.objects.active().first() == user


@pytest.mark.django_db
def test_core_queryset_deactivate(user_account):
    assert User.objects.count() == 0

    user = user_account(is_active=True)

    assert User.objects.count() == 1
    assert User.objects.active().count() == 1
    assert User.objects.inactive().count() == 0
    assert User.objects.active().first() == user

    user.deactivate()

    assert User.objects.count() == 1
    assert User.objects.active().count() == 0
    assert User.objects.inactive().count() == 1
    assert User.objects.inactive().first() == user


@pytest.mark.django_db
def test_create_user_success():
    assert User.objects.count() == 0

    user_email = "jane@example.com"
    user_password = "super-secret-password"
    user = User.objects.create_user(user_email, user_password)

    assert User.objects.count() == 1
    assert User.objects.first() == user
    assert user.email == user_email
    assert not user.is_staff
    assert not user.is_superuser
    assert user.check_password(user_password)


@pytest.mark.django_db
def test_create_user_no_email_failure():
    assert User.objects.count() == 0

    with pytest.raises(ValueError) as error:
        User.objects.create_user(None)

    assert User.objects.count() == 0
    assert "Users must give an email address" in str(error.value)


@pytest.mark.django_db
def test_create_superuser_success():
    assert User.objects.count() == 0

    superuser_email = "admin@example.com"
    superuser_password = "super-secret-password"
    superuser = User.objects.create_superuser(superuser_email, superuser_password)

    assert User.objects.count() == 1
    assert User.objects.first() == superuser
    assert superuser.email == superuser_email
    assert superuser.is_staff
    assert superuser.is_superuser
    assert superuser.check_password(superuser_password)


@pytest.mark.django_db
def test_create_superuser_no_email_failure():
    assert User.objects.count() == 0

    with pytest.raises(ValueError) as error:
        User.objects.create_superuser(None, None)

    assert User.objects.count() == 0
    assert "Users must give an email address" in str(error.value)


@pytest.mark.parametrize("email", ["jane@example.com", "john@example.com"])
@pytest.mark.django_db
def test_get_short_name(user_account, email):
    assert User.objects.count() == 0

    user = user_account(email=email)

    assert User.objects.count() == 1
    assert User.objects.first() == user
    assert user.get_short_name() == user.email


@pytest.mark.parametrize(
    "first_name,last_name,email,expected",
    [
        ("Jane", "Doe", "jane@example.com", "Jane Doe <jane@example.com>"),
        ("", "", "jane@example.com", "jane@example.com"),
        ("", "Doe", "jane@example.com", "jane@example.com"),
        ("Jane", "", "jane@example.com", "jane@example.com"),
    ],
)
@pytest.mark.django_db
def test_get_full_name(user_account, first_name, last_name, email, expected):
    assert User.objects.count() == 0

    user = user_account(first_name=first_name, last_name=last_name, email=email)

    assert User.objects.count() == 1
    assert User.objects.first() == user
    assert user.get_full_name() == expected


@pytest.mark.parametrize("first_name,last_name,expected", [("Jane", "Doe", "Jane Doe"), ("", "", "Dear client")])
@pytest.mark.django_db
def test_notification_salutation(user_account, first_name, last_name, expected):
    user = user_account(first_name=first_name, last_name=last_name)
    assert user.notification_salutation == expected
