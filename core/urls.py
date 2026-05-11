"""URLs for the project."""

from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from pages import views
from pages.sitemaps import StaticViewSitemap


sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("", include("pages.urls")),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

handler404 = "pages.views.page_not_found"
handler500 = "pages.views.server_error"

