import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from django.conf import settings


if not settings.DEBUG:
    from celery import Celery

    app = Celery("aryu_blog")
    app.config_from_object("django.conf:settings", namespace="CELERY")
    app.autodiscover_tasks()
