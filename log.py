import logging
from logging.handlers import RotatingFileHandler

import config

log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s(%(lineno)d) - %(message)s")

log_file = "logs/bot_log.txt"
file_handler = RotatingFileHandler(
    log_file,
    mode="a",
    maxBytes=49 * 1024 * 1024,
    backupCount=20,
    encoding="utf8",
)

error_log_file = "logs/error_bot_log.txt"
error_file_handler = RotatingFileHandler(
    error_log_file,
    mode="a",
    maxBytes=49 * 1024 * 1024,
    backupCount=10,
    encoding="utf8",
)

app_log = logging.getLogger("root")
app_log.setLevel(config.LOG_LEVEL)

file_handler.setFormatter(log_formatter)
file_handler.setLevel(config.LOG_LEVEL)

error_file_handler.setFormatter(log_formatter)
error_file_handler.setLevel(logging.ERROR)

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(log_formatter)

app_log.addHandler(file_handler)
app_log.addHandler(error_file_handler)
app_log.addHandler(streamHandler)
