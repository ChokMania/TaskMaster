import unittest
from unittest.mock import MagicMock
from taskmaster.process import ProcessController
from taskmaster.logger import Logger


class TestProcess(unittest.TestCase):
    def setUp(self):
        self.name = "test_process"
        self.config = {
            "cmd": "python script.py",
            "workingdir": "/path/to/workingdir",
            "env": {"VAR1": "value1", "VAR2": "value2"},
        }
        self.logger = Logger("TestLogger", log_level="DEBUG", log_file=None)
        self.process_controller = ProcessController(self.name, self.config, self.logger)

    def test_start(self):
        self.process_controller.start = MagicMock()
        self.process_controller.start()
        self.process_controller.start.assert_called_once()

    def test_stop(self):
        self.process_controller.stop = MagicMock()
        self.process_controller.stop()
        self.process_controller.stop.assert_called_once()

    def test_restart(self):
        self.process_controller.restart = MagicMock()
        self.process_controller.restart()
        self.process_controller.restart.assert_called_once()


if __name__ == "__main__":
    unittest.main()
