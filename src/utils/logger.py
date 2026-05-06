import sys
import logging
from src.core.config import settings

def setup_logger():
    logger = logging.getLogger("aina")
    logger.setLevel(settings.LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()
