from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class CoreQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class CoreManager(models.Manager.from_queryset(CoreQuerySet)):  # type: ignore[misc]
    pass


class CoreModel(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)

    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("Created"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated"))

    is_active = models.BooleanField(_("Active"), default=True, db_index=True)

    objects = CoreManager()

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.pk)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk}>"

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save(update_fields=["is_active", "updated"] if not self._state.adding else None)

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.save(update_fields=["is_active", "updated"] if not self._state.adding else None)
