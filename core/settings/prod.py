"""Production settings for the project."""

from .base import *  # noqa: F403
from core.logging_config import build_logging_config


DEBUG = False
IS_PROD = True

SECRET_KEY = env("SECRET_KEY")  # noqa: F405
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")  # noqa: F405

SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

LOGGING = build_logging_config(IS_PROD)
