import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file, level=logging.DEBUG):
    """Function to setup as many loggers as you want"""
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

# Create a default logger
default_logger = setup_logger('ami-logger', '/logs/ami-logger.log')

# Function to get logger
def get_logger(name=None):
    if name:
        return setup_logger(f'ami-logger.{name}', f'/logs/{name}.log')
    return default_logger