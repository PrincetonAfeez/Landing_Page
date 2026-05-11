"""Logging configuration for the project."""

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"


def build_logging_config(is_prod: bool) -> dict:
    if not is_prod:
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "human": {
                    "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "human",
                },
            },
            "loggers": {
                "django": {"handlers": ["console"], "level": "INFO"},
                "pages": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
                "core": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
            },
        }

    LOG_DIR.mkdir(exist_ok=True)
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(levelname)s %(name)s %(message)s %(module)s %(funcName)s %(lineno)d",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": str(LOG_DIR / "aboveboard.log"),
                "maxBytes": 10485760,
                "backupCount": 5,
                "formatter": "json",
            },
        },
        "loggers": {
            "django": {"handlers": ["console", "file"], "level": "WARNING"},
            "pages": {"handlers": ["console", "file"], "level": "INFO", "propagate": False},
            "core": {"handlers": ["console", "file"], "level": "INFO", "propagate": False},
        },
    }

