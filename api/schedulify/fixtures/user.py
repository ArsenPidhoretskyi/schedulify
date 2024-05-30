import pytest

from model_bakery import baker


__all__ = ["user_account"]


@pytest.fixture()
def user_account(db):  # pylint: disable=unused-argument
    def _user(**kwargs):
        return baker.make("accounts.User", **kwargs)

    return _user
