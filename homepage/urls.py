from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("map_change", views.map_change),
]