from cmd import Cmd

from config.config import Configuration
from signal_handler.signal_handler import SignalHandler
from utils.logger import TaskmasterLogger

__all__ = [
    "TaskmasterShell",
]


class TaskmasterShell(Cmd):
    prompt = "Taskmaster> "
    intro = "Welcome to Taskmaster shell. Type help or ? to list commands.\n"

    def __init__(self, config_file):
        super().__init__()
        self.config_file = config_file
        self.programs = {}
        self.logger = TaskmasterLogger()

        self.signal_handler = SignalHandler()
        self.load_config()

    def load_config(self):
        try:
            config = Configuration(self.config_file)
            self.programs = config.programs
            self.logger.log_event("Configuration loaded")
        except Exception as e:
            self.logger.log_error(f"Error loading configuration file: {str(e)}")

    def _find_arg(self, arg):
        if arg not in self.programs:
            print(f"Error: program '{arg}' not found")
            return False
        return True

    def do_start(self, arg):
        "Start a program. Usage: start <program>"
        if self._find_arg(arg):
            self.programs[arg].start()

    def do_stop(self, arg):
        "Stop a program. Usage: stop <program>"
        if self._find_arg(arg):
            self.programs[arg].stop()

    def do_restart(self, arg):
        "Restart a program. Usage: restart <program>"
        if self._find_arg(arg):
            self.programs[arg].restart()

    def do_status(self, arg):
        "Get the status of all programs. Usage: status"
        for name in self.programs:
            status = self.programs[name].get_status()
            print(f"{name} - {status}")

    def do_reload(self, arg):
        "Reload the configuration file. Usage: reload"
        self.load_config()

    def do_exit(self, arg):
        "Exit the Taskmaster shell. Usage: exit"
        return True

    def emptyline(self):
        pass

    def postcmd(self, stop, line):
        self.signal_handler.register_signals()
        return stop
