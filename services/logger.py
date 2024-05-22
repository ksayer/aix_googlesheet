import logging
from logging.handlers import RotatingFileHandler

from settings.settings import BASE_DIR


def init_logger():
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_directory = 'logs'
    log_file = BASE_DIR / log_directory / 'app.log'

    # Create log directory if it doesn't exist
    import os
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # File handler
    file_handler = RotatingFileHandler(log_file, maxBytes=10 ** 6, backupCount=5)
    file_handler.setFormatter(log_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)

    # Configure root logger
    logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])
    logger = logging.getLogger(__name__)
    return logger
