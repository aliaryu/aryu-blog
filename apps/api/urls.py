from django.urls import path, include
from .api.views import APIRootView


urlpatterns = [
    path("", APIRootView.as_view(), name="api-root"),

    path('api-auth/', include('rest_framework.urls')),
    
    path("users/", include("apps.users.urls")),
]
