from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('image', views.update_brawler_pics, name="update_brawler_pics"),
]