import logging
import re
import sys
from app.core.config import settings

class SecretMaskingFilter(logging.Filter):
    """
    Production Security Filter:
    Redacts sensitive credentials, API keys, and bearer tokens from all application logs.
    """
    PATTERNS = [
        (re.compile(r'(nvapi-[A-Za-z0-9_-]{8})[A-Za-z0-9_-]+'), r'\1...[REDACTED]'),
        (re.compile(r'(AQ\.[A-Za-z0-9_-]{6})[A-Za-z0-9_-]+'), r'\1...[REDACTED]'),
        (re.compile(r'(AIza[A-Za-z0-9_-]{6})[A-Za-z0-9_-]+'), r'\1...[REDACTED]'),
        (re.compile(r'(Bearer\s+)[A-Za-z0-9_.-]{10,}'), r'\1[TOKEN_REDACTED]'),
        (re.compile(r'(api_key["\']?\s*[:=]\s*["\']?)([^"\'\s]{4})[^"\'\s]+'), r'\1\2***[REDACTED]'),
        (re.compile(r'(password["\']?\s*[:=]\s*["\']?)([^"\'\s]{2})[^"\'\s]+'), r'\1**[REDACTED]')
    ]

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            for pattern, repl in self.PATTERNS:
                record.msg = pattern.sub(repl, record.msg)
        return True

def setup_logging():
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    
    handler = logging.StreamHandler(sys.stdout)
    handler.addFilter(SecretMaskingFilter())
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"))

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers = [handler]

logger = logging.getLogger("zyra")
logger.addFilter(SecretMaskingFilter())
