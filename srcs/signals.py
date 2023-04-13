import signal

from srcs.logger import TaskmasterLogger

__all__ = [
    "SignalHandler",
]


class SignalHandler:
    """
    A class for handling signals.
    """

    def __init__(self):
        """
        Initialize the signal handler with a logger.
        """
        self.logger = TaskmasterLogger()

    def register_signals(self):
        """
        Register signal handlers.
        """
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGINT, self.handle_signal)
        # signal.signal(signal.SIGHUP, self.handle_signal)

    def handle_signal(self, signum, frame):
        """
        Handle a signal.
        """
        self.logger.log_event(f"Received signal {signum}")
        if signum == signal.SIGTERM or signum == signal.SIGINT:
            self.handle_terminate_signal()
        # elif signum == signal.SIGHUP:
        #     self.handle_reload_signal()

    def handle_terminate_signal(self):
        """
        Handle a terminate signal (SIGTERM or SIGINT).
        """
        self.logger.log_event("Taskmaster stopping...")
        # Stop all running programs here
        # ...
        self.logger.log_event("Taskmaster stopped")
        exit(0)

    def handle_reload_signal(self):
        """
        Handle a reload signal (SIGHUP).
        """
        self.logger.log_event("Reloading configuration...")
        # Reload configuration file and restart programs if necessary
        # ...
        self.logger.log_event("Configuration reloaded")
