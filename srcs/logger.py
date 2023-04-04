import logging
import os

__all__ = [
    "TaskmasterLogger",
]


class TaskmasterLogger:
    _instance = None
    _log_file = "taskmaster.log"

    def __new__(cls, level=logging.INFO):
        if cls._instance is None:
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            cls._instance = super().__new__(cls)
            cls._instance.logger = logging.getLogger("Taskmaster")
            cls._instance.logger.setLevel(level)
            if not os.path.exists(cls._log_file):
                open(cls._log_file, "a").close()
            handler = logging.FileHandler(cls._log_file)
            handler.setFormatter(formatter)
            cls._instance.logger.addHandler(handler)
        return cls._instance

    def log_event(self, message):
        self.logger.info(message)

    def log_error(self, message):
        import inspect

        method_name = inspect.stack()[1][3]
        print(f"{method_name} => {message}")
        self.logger.error(message)
