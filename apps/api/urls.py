from django.urls import path, include
from .api.views import APIRootView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)


urlpatterns = [
    path("", APIRootView.as_view(), name="api-root"),

    path("api-auth/", include("rest_framework.urls")),
    
    path("users/", include("apps.users.urls")),
    path("blog/", include("apps.blog.urls")),

    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="token-blacklist"),
]
