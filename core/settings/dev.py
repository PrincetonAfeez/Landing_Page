"""Development settings for the project."""

from csp.constants import SELF

from .base import *  # noqa: F403
from core.logging_config import build_logging_config


DEBUG = True
IS_PROD = False
ALLOWED_HOSTS = ["*"]

CONTENT_SECURITY_POLICY = {
    **CONTENT_SECURITY_POLICY,  # noqa: F405
    "DIRECTIVES": {
        **CONTENT_SECURITY_POLICY["DIRECTIVES"],  # noqa: F405
        "connect-src": [SELF, "http://localhost:*", "http://127.0.0.1:*", "ws://localhost:*", "ws://127.0.0.1:*"],
    },
}

LOGGING = build_logging_config(IS_PROD)

