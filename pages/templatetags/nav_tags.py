"""Custom template tags for the project."""

from django import template
from django.urls import NoReverseMatch, reverse


register = template.Library()


@register.simple_tag(takes_context=True)
def active_link(context, url_name):
    request = context.get("request")
    if request is None:
        return ""

    try:
        target_path = reverse(url_name)
    except NoReverseMatch:
        return ""

    return "text-brand-primary font-semibold" if request.path == target_path else ""

