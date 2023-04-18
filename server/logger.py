import logging
from logging.handlers import RotatingFileHandler, SMTPHandler, SysLogHandler
import os


class Logger:
    display_cli_prompt_method = None

    _instances = {}
    _max_size = 1024 * 1024 * 10  # 10MB
    _backup_count = 5

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[33m",  # Yellow
        "INFO": "\033[37m",  # White
        "WARNING": "\033[35m",  # Purple
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[31m",  # Red
        "RESET": "\033[0m",  # Reset
    }

    def __new__(
        cls, name, log_file, log_level="INFO", smtp_config=None, syslog_config=None
    ):
        if name not in cls._instances:
            instance = super().__new__(cls)
            instance.logger = logging.getLogger(name)
            instance.logger.setLevel(log_level)

            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            if log_file:
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
                file_handler = RotatingFileHandler(
                    log_file, maxBytes=cls._max_size, backupCount=cls._backup_count
                )
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

    def log(self, message, level=logging.INFO, display_cli_prompt=False):
        self.display_on_cli(message, level, display_cli_prompt)
        self.logger.log(level, message)

    def debug(self, message, display_cli_prompt=False):
        self.display_on_cli(message, logging.DEBUG, display_cli_prompt)
        self.logger.debug(message)

    def info(self, message, display_cli_prompt=False):
        self.display_on_cli(message, logging.INFO, display_cli_prompt)
        self.logger.info(message)

    def warning(self, message, display_cli_prompt=False):
        self.display_on_cli(message, logging.WARNING, display_cli_prompt)
        self.logger.warning(message)

    def error(self, message, display_cli_prompt=False):
        self.display_on_cli(message, logging.ERROR, display_cli_prompt)
        self.logger.error(message)

    def redisplay_cli_prompt(self):
        if self.display_cli_prompt_method is not None:
            self.display_cli_prompt_method()

    def display_on_cli(self, message, level, display_cli_prompt=False):
        color = self.COLORS.get(logging.getLevelName(level), "")
        print(color + message + self.COLORS["RESET"])
        if display_cli_prompt:
            self.redisplay_cli_prompt()

    def critical(self, message, display_cli_prompt=False):
        self.display_on_cli(message, logging.CRITICAL, display_cli_prompt)
        self.logger.critical(message)


if __name__ == "__main__":
    print("This module is not meant to be run directly.")
    print("Please run main.py instead.")
