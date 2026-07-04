import logging
import sys
from pythonjsonlogger import jsonlogger


def configure_logging(level: str) -> None:
    """Configure structured JSON logging for containers and log aggregation."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s %(correlation_id)s"))
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level.upper())
