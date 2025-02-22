from typing import Union

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.functional import Promise
from django.utils.translation import gettext_lazy

from schedulify.apps.commons.models import CoreManager, CoreModel


class UserManager(CoreManager, BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must give an email address")

        user = self.model(email=email)
        if not hasattr(user, "set_password"):
            raise TypeError("User doesn't have set_password method")

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(PermissionsMixin, CoreModel, AbstractBaseUser):
    email = models.EmailField(verbose_name=gettext_lazy("Email address"), unique=True)
    first_name = models.CharField(verbose_name=gettext_lazy("First name"), max_length=150, blank=True)
    last_name = models.CharField(verbose_name=gettext_lazy("Last name"), max_length=150, blank=True)
    is_staff = models.BooleanField(
        gettext_lazy("Staff status"),
        default=False,
        help_text=gettext_lazy("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        gettext_lazy("Active"),
        default=True,
        help_text=gettext_lazy(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()  # type: ignore[misc]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("first_name", "last_name")

    def __str__(self):
        return self.email

    def get_short_name(self) -> str:
        return str(self.email)

    def get_full_name(self) -> Union[Promise, str]:
        full_name = self.get_short_name()
        if self.first_name and self.last_name:
            full_name = f"{self.first_name} {self.last_name} <{self.email}>"

        return full_name

    @property
    def notification_salutation(self):
        salutation: Union[Promise, str] = gettext_lazy("Dear client")
        if self.first_name and self.last_name:
            salutation = f"{self.first_name} {self.last_name}"

        return salutation
