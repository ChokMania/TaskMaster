import unittest
from unittest.mock import MagicMock
from taskmaster.control_shell import ControlShell
from taskmaster.process_manager import ProcessManager
from taskmaster.logger import Logger

class TestControlShell(unittest.TestCase):
    def setUp(self):
        self.config_path = "path/to/test_config.yml"
        self.logger = Logger("TestLogger", log_level="DEBUG", log_file=None)
        self.process_manager = ProcessManager(self.config_path, self.logger)
        self.control_shell = ControlShell(self.process_manager, self.logger)

    def test_command_start(self):
        self.control_shell.do_start = MagicMock()
        self.control_shell.onecmd("start")
        self.control_shell.do_start.assert_called_once()

    def test_command_stop(self):
        self.control_shell.do_stop = MagicMock()
        self.control_shell.onecmd("stop")
        self.control_shell.do_stop.assert_called_once()

    def test_command_restart(self):
        self.control_shell.do_restart = MagicMock()
        self.control_shell.onecmd("restart")
        self.control_shell.do_restart.assert_called_once()

if __name__ == '__main__':
    unittest.main()
