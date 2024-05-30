from django.urls import include, path


urlpatterns = [
    path("", include("schedulify.apps.events.api.v1")),
]
