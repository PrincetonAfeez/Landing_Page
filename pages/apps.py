"""App configuration for the project."""

from pathlib import Path

from django.apps import AppConfig


SITE_VERSION = "0.0.0"


def _read_version() -> str:
    version_path = Path(__file__).resolve().parent.parent / "VERSION"
    try:
        return version_path.read_text(encoding="utf-8").strip() or "0.0.0"
    except OSError:
        return "0.0.0"


def get_site_version() -> str:
    return SITE_VERSION


class PagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pages"

    def ready(self) -> None:
        global SITE_VERSION
        SITE_VERSION = _read_version()

