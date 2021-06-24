import logging.config
from typing import Final

from aiohttp.log import access_logger, web_logger

from .presentation.request_id import get_request_id


def setup() -> None:
    logging.config.dictConfig(CONFIG)


class ServiceNameFilter(logging.Filter):

    def __init__(self, name: str = ""):
        self.service_name = "com_portfolio"

        super().__init__(name)

    def filter(self, record: logging.LogRecord) -> bool:
        setattr(record, "service_name", self.service_name)

        return super().filter(record)


class RequestIDFilter(logging.Filter):

    def filter(self, record: logging.LogRecord) -> bool:
        request_id = get_request_id() or "-"
        setattr(record, "request_id", request_id)

        return super().filter(record)


LEVEL: Final = "INFO"
DATETIME_FORMAT: Final = "%Y-%m-%d %H:%M:%S"

GUNICORN_ACCESS_LOG_FORMAT: Final = (
    'request_id="%{X-Request-ID}o" '
    'remote_addr="%a" '
    'user_agent="%{User-Agent}i" '
    'protocol="%r" '
    'response_code="%s" '
    'request_time="%Tf" '
)

CONFIG: Final = {
    "version": 1,
    "disable_existing_loggers": True,
    "loggers": {
        access_logger.name: {
            "level": LEVEL,
            "handlers": [
                "access",
            ],
            "propagate": False,
        },
        web_logger.name: {
            "level": LEVEL,
            "handlers": [
                "console",
            ],
            "propagate": False,
        },
        "gunicorn.access": {
            "level": LEVEL,
            "handlers": [
                "access",
            ],
            "propagate": False,
        },
        "gunicorn.error": {
            "level": LEVEL,
            "handlers": [
                "console",
            ],
            "propagate": False,
        },
    },
    "handlers": {
        "console": {
            "level": LEVEL,
            "formatter": "console",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "filters": [
                "service_name",
                "request_id",
            ],
        },
        "access": {
            "level": LEVEL,
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "filters": [
                "service_name",
                "request_id",
            ],
        },
    },
    "formatters": {
        "console": {
            "format": (
                'time="%(asctime)s" '
                'level="%(levelname)s" '
                'logger="%(name)s" '
                'service_name="%(service_name)s" '
                'pid="%(process)d" '
                'request_id="%(request_id)s" '
                'message="%(message)s" '
            ),
            "datefmt": DATETIME_FORMAT,
        },
        "access": {
            "format": (
                'time="%(asctime)s" '
                'level="%(levelname)s" '
                'logger="%(name)s" '
                'service_name="%(service_name)s" '
                'pid="%(process)d" '
                "%(message)s "
            ),
            "datefmt": DATETIME_FORMAT,
        },
    },
    "filters": {
        "service_name": {
            "()": "com_portfolio.log.ServiceNameFilter",
        },
        "request_id": {
            "()": "com_portfolio.log.RequestIDFilter",
        },
    },
}
