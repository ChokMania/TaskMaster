import unittest
from unittest.mock import MagicMock
from taskmaster.process_manager import ProcessManager
from taskmaster.logger import Logger

class TestProcessManager(unittest.TestCase):
    def setUp(self):
        self.config_path = "path/to/test_config.yml"
        self.logger = Logger("TestLogger", log_level="DEBUG", log_file=None)
        self.process_manager = ProcessManager(self.config_path, self.logger)

    def test_load_configuration(self):
        self.process_manager.load_configuration = MagicMock()
        self.process_manager.load_configuration()
        self.process_manager.load_configuration.assert_called_once()

    def test_start_all(self):
        self.process_manager.start_all = MagicMock()
        self.process_manager.start_all()
        self.process_manager.start_all.assert_called_once()

    def test_stop_all(self):
        self.process_manager.stop_all = MagicMock()
        self.process_manager.stop_all()
        self.process_manager.stop_all.assert_called_once()

    def test_restart_all(self):
        self.process_manager.restart_all = MagicMock()
        self.process_manager.restart_all()
        self.process_manager.restart_all.assert_called_once()

if __name__ == '__main__':
    unittest.main()
