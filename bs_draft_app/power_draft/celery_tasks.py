import os 
from celery import Celery # type: ignore


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'power_draft.settings')
app = Celery("power_draft")
app.config_from_object("django.conf:settings", namespace = "CELERY")

app.autodiscover_tasks()
worker_redirect_stdouts = 0