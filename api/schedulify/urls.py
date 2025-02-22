from typing import List, Union

from django.conf import settings
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path


PLATFORM_PREFIX = "_platform"
API_PREFIX = "api"
DOCS_PREFIX = "docs"

api_v1_urlpatterns = [
    path(
        f"{API_PREFIX}/v1/{application_name}/",
        include(
            (f"schedulify.apps.{application_name}.api.v1.urls", application_name),
            namespace=f"api-v1-{application_name}",
        ),
    )
    for application_name in ["accounts", "events"]
]

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path("admin/", admin.site.urls),
    *api_v1_urlpatterns,
]

# enable Swagger
if "SWAGGER" in settings.SCHEDULIFY_FEATURES:
    from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

    swagger_urlpatterns = [
        path(f"{PLATFORM_PREFIX}/{DOCS_PREFIX}/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            f"{PLATFORM_PREFIX}/{DOCS_PREFIX}/v1/swagger/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="v1-schema-swagger-ui",
        ),
        path(
            f"{PLATFORM_PREFIX}/{DOCS_PREFIX}/v1/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="v1-schema-redoc",
        ),
    ]

    urlpatterns += swagger_urlpatterns

# enable debug_toolbar for local develop (if installed)
if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]


# enable Sentry check (by raising 500 on demand)
if not settings.DEBUG:
    from django.views.generic.base import View  # pylint: disable=ungrouped-imports

    class ServerErrorTestView(View):
        def dispatch(self, request, *args, **kwargs):
            assert False, "Server error test: response with 500 HTTP status code"  # noqa: S101

    urlpatterns += [path(f"{PLATFORM_PREFIX}/500-error-test/", ServerErrorTestView.as_view())]
