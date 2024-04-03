from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("map_change", views.map_change, name = "map_change"),
    path("brawler_pick", views.brawler_pick, name = "brawler_pick"),
]