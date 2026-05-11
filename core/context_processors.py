"""Context processors for the project."""

from urllib.parse import urlsplit, urlunsplit

from django.conf import settings
from django.urls import NoReverseMatch, reverse

from pages.apps import get_site_version
from pages.content import FOOTER_LINKS, NAV_ITEMS, SITE_NAME, TAGLINE


def site_context(request):
    canonical_url = ""
    og_image_url = ""
    if request is not None:
        canonical_url = urlunsplit(urlsplit(request.build_absolute_uri())[:3] + ("", ""))
        try:
            og_image_url = request.build_absolute_uri(reverse("pages:og_card"))
        except NoReverseMatch:
            og_image_url = ""

    return {
        "SITE_NAME": SITE_NAME,
        "TAGLINE": TAGLINE,
        "SITE_VERSION": get_site_version(),
        "IS_PROD": settings.IS_PROD,
        "NAV_ITEMS": NAV_ITEMS,
        "FOOTER_LINKS": FOOTER_LINKS,
        "canonical_url": canonical_url,
        "og_image_url": og_image_url,
    }

