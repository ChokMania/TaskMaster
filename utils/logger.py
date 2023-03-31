import logging
from logging.handlers import RotatingFileHandler
import os

__all__ = [
    "TaskmasterLogger",
]


class TaskmasterLogger:
    _instance = None
    _log_file = "taskmaster.log"
    _max_size = 1024 * 1024 * 10 # 10MB
    _backup_count = 5

    def __new__(cls, level=logging.INFO):
        if cls._instance is None:
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            cls._instance = super().__new__(cls)
            cls._instance.logger = logging.getLogger("Taskmaster")
            cls._instance.logger.setLevel(level)
            if not os.path.exists(cls._log_file):
                open(cls._log_file, "a").close()
            handler = logging._handlers.RotatingFileHandler(cls._log_file, maxBytes=cls._max_size, backupCount=cls._backup_count)
            handler.setFormatter(formatter)
            cls._instance.logger.addHandler(handler)
            # Ajouter la journalisation des métriques
            cls._instance.metrics_logger = logging.getLogger("TaskmasterMetrics")
            cls._instance.metrics_logger.setLevel(logging.DEBUG)
            if not os.path.exists("taskmaster_metrics.log"):
                open("taskmaster_metrics.log", "a").close()
            metrics_handler = logging._handlers.RotatingFileHandler("taskmaster_metrics.log", maxBytes=cls._max_size, backupCount=cls._backup_count)
            metrics_handler.setFormatter(formatter)
            cls._instance.metrics_logger.addHandler(metrics_handler)

        return cls._instance

    def log_event(self, message, level=logging.INFO):
        self.logger.log(level, message)

    def log_error(self, message, level=logging.ERROR):
        import inspect, traceback
        exc_info = traceback.format_exc()
        method_name = inspect.stack()[1][3]
        print(f"{method_name} => {message}\n{exc_info}")
        self.logger.log(level, f"{message}\n{exc_info}")

    # Ajouter la journalisation des métriques
    def log_metric(self, message, level=logging.INFO):
        self.metrics_logger.log(level, message)