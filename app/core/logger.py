import logging
from functools import lru_cache
from sys import stdout
from time import gmtime


@lru_cache()
def get_logger():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    log_formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d: [%(process)d:%(thread)d] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
    )
    log_formatter.converter = gmtime
    root_logger = logging.getLogger()

    console_handler = logging.StreamHandler(stdout)
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG)

    return logging


class LogMixin:
    logger = get_logger()

    def log(self, msg, log_mark: str | None = ""):
        self.logger.info(f"{self.__class__.__name__} {log_mark} {msg}")

    def log_debug(self, msg):
        self.logger.debug(f"{self.__class__.__name__} {msg}")

    def log_warning(self, msg):
        self.logger.warning(f"{self.__class__.__name__} {msg}")

    def log_error(self, msg):
        self.logger.error(f"{self.__class__.__name__} {msg}")