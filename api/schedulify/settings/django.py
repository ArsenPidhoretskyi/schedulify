from pathlib import Path

from .environment import env


BASE_DIR = Path(__file__).resolve().parent.parent


DEBUG = env.bool("SCHEDULIFY_DEBUG", default=False)

INTERNAL_IPS = env.list("SCHEDULIFY_INTERNAL_IPS", default=[])

ALLOWED_HOSTS = env.list("SCHEDULIFY_ALLOWED_HOSTS", default=[])

SECRET_KEY = env.str("SCHEDULIFY_SECRET_KEY")


PRE_DJANGO_APPS = [
    "admin_interface",
    "colorfield",
]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


THIRD_PARTY_APPS = [
    "django_extensions",
    "django_filters",
    "drf_spectacular",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
]

FIRST_PARTY_APPS = [
    "schedulify.apps.commons",
    "schedulify.apps.accounts",
    "schedulify.apps.events",
]

INSTALLED_APPS = [
    *PRE_DJANGO_APPS,
    *DJANGO_APPS,
    *THIRD_PARTY_APPS,
    *FIRST_PARTY_APPS,
    *env.list("SCHEDULIFY_DEV_INSTALLED_APPS", default=[]),
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
] + env.list("SCHEDULIFY_DEV_MIDDLEWARE", default=[])

ROOT_URLCONF = "schedulify.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "schedulify.wsgi.application"

DATABASES = {
    "default": env.db("SCHEDULIFY_DATABASE_URL"),
}

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

SECURE_CONTENT_TYPE_NOSNIFF = env.bool("SCHEDULIFY_SECURE_CONTENT_TYPE_NOSNIFF", default=True)
SECURE_HSTS_SECONDS = env.int("SCHEDULIFY_SECURE_HSTS_SECONDS", default=31536000)  # 1 year

SESSION_COOKIE_HTTPONLY = env.bool("SCHEDULIFY_SESSION_COOKIE_HTTPONLY", default=True)
SESSION_COOKIE_SECURE = env.bool("SCHEDULIFY_SESSION_COOKIE_SECURE", default=True)
SESSION_COOKIE_NAME = "s"

CSRF_COOKIE_SECURE = env.bool("SCHEDULIFY_CSRF_COOKIE_SECURE", default=True)
CSRF_COOKIE_NAME = "c"

X_FRAME_OPTIONS = env.str("SCHEDULIFY_X_FRAME_OPTIONS", default="SAMEORIGIN")

LANGUAGE_CODE = "en-us"

TIME_ZONE = env.str("SCHEDULIFY_TIME_ZONE", default="UTC")

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [BASE_DIR / ".." / ".." / "api" / "locale"]


DEFAULT_FILE_STORAGE_BACKEND = env.str(
    "SCHEDULIFY_DEFAULT_FILE_STORAGE_BACKEND", default="storages.backends.s3boto3.S3Boto3Storage"
)
DEFAULT_FILE_STORAGE_OPTIONS = {}
if DEFAULT_FILE_STORAGE_BACKEND == "storages.backends.s3boto3.S3Boto3Storage":
    DEFAULT_FILE_STORAGE_OPTIONS = {
        "bucket_name": env.str("SCHEDULIFY_DEFAULT_FILE_STORAGE_BUCKET_NAME"),
        "endpoint_url": env.str("SCHEDULIFY_DEFAULT_FILE_STORAGE_ENDPOINT_URL"),
        "custom_domain": env.str("SCHEDULIFY_DEFAULT_FILE_STORAGE_CUSTOM_DOMAIN"),
        "url_protocol": env.str("SCHEDULIFY_DEFAULT_FILE_STORAGE_URL_PROTOCOL", default="https:"),
        "location": env.str("SCHEDULIFY_DEFAULT_FILE_STORAGE_LOCATION", default="m"),
        "file_overwrite": env.bool("SCHEDULIFY_DEFAULT_FILE_STORAGE_FILE_OVERWRITE", default=False),
    }

STATICFILES_STORAGE_BACKEND = env.str(
    "SCHEDULIFY_STATICFILES_STORAGE_BACKEND", default="storages.backends.s3boto3.S3StaticStorage"
)
STATICFILES_STORAGE_OPTIONS = {}
if STATICFILES_STORAGE_BACKEND == "storages.backends.s3boto3.S3StaticStorage":
    STATICFILES_STORAGE_OPTIONS = {
        "bucket_name": env.str("SCHEDULIFY_DEFAULT_FILE_STORAGE_BUCKET_NAME"),
        "endpoint_url": env.str("SCHEDULIFY_DEFAULT_FILE_STORAGE_ENDPOINT_URL"),
        "custom_domain": env.str("SCHEDULIFY_DEFAULT_FILE_STORAGE_CUSTOM_DOMAIN"),
        "url_protocol": env.str("SCHEDULIFY_DEFAULT_FILE_STORAGE_URL_PROTOCOL", default="https:"),
        "location": env.str("SCHEDULIFY_STATICFILES_STORAGE_LOCATION", default="s"),
        "file_overwrite": env.bool("SCHEDULIFY_STATICFILES_STORAGE_FILE_OVERWRITE", default=True),
    }
elif STATICFILES_STORAGE_BACKEND == "django.contrib.staticfiles.storage.StaticFilesStorage":
    STATIC_URL = "/static/"
    STATIC_ROOT = str(BASE_DIR / ".." / ".." / "public" / "static")

STORAGES = {
    "default": {
        "BACKEND": DEFAULT_FILE_STORAGE_BACKEND,
        "OPTIONS": DEFAULT_FILE_STORAGE_OPTIONS,
    },
    "staticfiles": {
        "BACKEND": STATICFILES_STORAGE_BACKEND,
        "OPTIONS": STATICFILES_STORAGE_OPTIONS,
    },
}

EMAIL_BACKEND = env.str(
    "SCHEDULIFY_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)

if EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend":  # pragma: no cover
    EMAIL_HOST = env.str("SCHEDULIFY_EMAIL_HOST")
    EMAIL_PORT = env.str("SCHEDULIFY_EMAIL_PORT")
    EMAIL_HOST_USER = env.str("SCHEDULIFY_EMAIL_HOST_USER", default=None)
    EMAIL_HOST_PASSWORD = env.str("SCHEDULIFY_EMAIL_HOST_PASSWORD", default=None)
    EMAIL_USE_TLS = env.bool("SCHEDULIFY_EMAIL_USE_TLS", default=True)

SITE_ID = env.int("SCHEDULIFY_SITE_ID", default=1)

USE_X_FORWARDED_HOST = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

APPEND_SLASH = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CORS_ALLOW_ALL_ORIGINS = env.bool("SCHEDULIFY_CORS_ORIGIN_ALLOW_ALL", default=False)
if not CORS_ALLOW_ALL_ORIGINS:
    CORS_ALLOWED_ORIGINS = env.list("SCHEDULIFY_CORS_ALLOWED_HOSTS", default=[])
    CORS_ALLOWED_ORIGIN_REGEXES = env.list("SCHEDULIFY_CORS_ALLOWED_ORIGIN_REGEXES", default=[])
