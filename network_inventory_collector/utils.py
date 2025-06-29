# utils.py

import logging
import time
from network_inventory_collector.config import RETRY_ATTEMPTS, RETRY_BACKOFF
from functools import wraps

def load_hosts(path: str) -> list:
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]

def load_credentials(path: str) -> dict:
    creds = {}
    with open(path) as f:
        for line in f:
            if '=' in line:
                user, pwd = line.strip().split("=", 1)
                creds[user] = pwd
    return creds

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler("collector.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

def retry_with_backoff(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        delay = RETRY_BACKOFF
        for attempt in range(1, RETRY_ATTEMPTS + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.warning(
                    f"Attempt {attempt}/{RETRY_ATTEMPTS} failed: {e}"
                )
                if attempt == RETRY_ATTEMPTS:
                    logging.error(f"Max retries reached for {func.__name__}. Giving up.")
                    raise
                time.sleep(delay)
                delay *= 2  # exponential backoff
    return wrapper
