from typing import Type

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenViewBase,
)


def get_token_schema_view(
    view_class: Type[TokenViewBase],
    summary: str,
    description: str = "",
) -> Type[TokenViewBase]:
    return extend_schema(
        tags=["Auth"],
    )(
        extend_schema_view(
            post=extend_schema(
                summary=summary,
                description=description,
                responses=view_class.serializer_class,
            ),
        )(view_class)
    )


TokenObtainPairView = get_token_schema_view(TokenObtainPairView, summary="Obtain JWT token pair")
TokenRefreshView = get_token_schema_view(TokenRefreshView, summary="Refresh JWT token")
TokenVerifyView = get_token_schema_view(TokenVerifyView, summary="Verify JWT token")
