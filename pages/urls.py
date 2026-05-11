"""URLs for the project."""

from django.urls import path

from . import views


app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("og/card.png", views.open_graph_card, name="og_card"),
]

