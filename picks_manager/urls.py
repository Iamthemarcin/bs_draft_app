from django.urls import path

from . import views

urlpatterns = [
    path("info/<brawler>", views.brawler_picks, name="brawler_picks"),
]