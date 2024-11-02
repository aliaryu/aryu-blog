from django.contrib import admin
from django.urls import path, include
from config import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from .views import redirect_to_api


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("apps.api.urls")),
    path("", redirect_to_api)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
