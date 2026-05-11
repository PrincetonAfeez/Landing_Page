"""Views for the project."""

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .content import FEATURES, HERO, PRICING_TIERS
from .og_image import OG_CARD_PNG


def home(request):
    return render(
        request,
        "pages/home.html",
        {
            "hero": HERO,
            "features": FEATURES,
            "pricing_tiers": PRICING_TIERS,
        },
    )


def open_graph_card(_request):
    response = HttpResponse(OG_CARD_PNG, content_type="image/png")
    response["Cache-Control"] = "public, max-age=86400"
    return response


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("sitemap"))
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def page_not_found(request, exception):
    return render(request, "404.html", status=404)


def server_error(request):
    return render(request, "500.html", status=500)

