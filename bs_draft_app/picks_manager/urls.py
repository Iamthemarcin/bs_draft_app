from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
import os

urlpatterns = []

if os.getenv('DEBUGPY_DJANGO'):
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
