from logzero import logger, logfile
import os

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

logfile(
    f"{LOG_DIR}/app.log",
    maxBytes=10_000_000,
    backupCount=5
)

logger.info("Logger.py => Logger initialized")

def get_logger():
    return logger