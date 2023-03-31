import os
import subprocess
import time
import unittest

from config.config import Configuration
from shell.shell import TaskmasterShell


class TestIntegration(unittest.TestCase):
    def setUp(self):
        # Create a temporary configuration file
        self.config_file = "test_config.yaml"
        with open(self.config_file, "w") as f:
            f.write(
                """
programs:
  sleep:
    cmd: "sleep 5"
    autostart: true
            """
            )

    def tearDown(self):
        # Remove the temporary configuration file
        os.remove(self.config_file)

    def test_start_stop(self):
        # Create a TaskmasterShell instance
        shell = TaskmasterShell(self.config_file)

        # Verify that the program is not running
        config = Configuration(self.config_file)
        self.assertEqual(config.get_program("sleep").get_status(), "stopped")

        # Start the program
        shell.onecmd("start sleep")

        # Verify that the program is running
        time.sleep(1)
        self.assertEqual(config.get_program("sleep").get_status(), "running")

        # Stop the program
        shell.onecmd("stop sleep")

        # Verify that the program has stopped
        time.sleep(1)
        self.assertEqual(config.get_program("sleep").get_status(), "stopped")
