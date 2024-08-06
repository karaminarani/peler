from .config import config
from .logger import logger

BOT_ID = config.BOT_TOKEN.split(":", 1)[0]

__all__ = ["config", "logger", "expired_date", "BOT_ID"]
