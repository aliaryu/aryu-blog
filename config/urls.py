from django.contrib import admin
from django.urls import path, include
from config import settings
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
