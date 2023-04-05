import logging
from logging.handlers import RotatingFileHandler
import os


class Logger:
    _instances = {}

    _max_size = 1024 * 1024 * 10  # 10MB
    _backup_count = 5

    def __new__(cls, name, log_file, log_level="INFO"):
        if name not in cls._instances:
            instance = super().__new__(cls)
            instance.logger = logging.getLogger(name)
            instance.logger.setLevel(log_level)

            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

            if log_file:
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
                file_handler = RotatingFileHandler(log_file, maxBytes=cls._max_size, backupCount=cls._backup_count)
                file_handler.setFormatter(formatter)
                instance.logger.addHandler(file_handler)

            cls._instances[name] = instance
        return cls._instances[name]

    def log(self, message, level=logging.INFO):
        self.logger.log(level, message)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
