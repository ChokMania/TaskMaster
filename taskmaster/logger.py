import logging
from logging.handlers import RotatingFileHandler, SMTPHandler, SysLogHandler
import os


class Logger:
    _instances = {}

    _max_size = 1024 * 1024 * 10  # 10MB
    _backup_count = 5

    def __new__(cls, name, log_file, log_level="INFO", smtp_config=None, syslog_config=None):
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

            if smtp_config:
                smtp_handler = SMTPHandler(
                    mailhost=smtp_config["mailhost"],
                    fromaddr=smtp_config["fromaddr"],
                    toaddrs=smtp_config["toaddrs"],
                    subject=smtp_config["subject"],
                    credentials=smtp_config["credentials"],
                    secure=smtp_config["secure"],
                )
                smtp_handler.setLevel(logging.ERROR)
                smtp_handler.setFormatter(formatter)
                instance.logger.addHandler(smtp_handler)

            if syslog_config:
                syslog_handler = SysLogHandler(
                    address=syslog_config["address"],
                    facility=syslog_config["facility"],
                )
                syslog_handler.setFormatter(formatter)
                instance.logger.addHandler(syslog_handler)

            cls._instances[name] = instance
        return cls._instances[name]

    def log(self, message, level=logging.INFO):
        print(message)
        self.logger.log(level, message)

    def debug(self, message):
        print(message)
        self.logger.debug(message)

    def info(self, message):
        print(message)
        self.logger.info(message)

    def warning(self, message):
        print(message)
        self.logger.warning(message)

    def error(self, message):
        print(message)
        self.logger.error(message)

    def critical(self, message):
        print(message)
        self.logger.critical(message)
