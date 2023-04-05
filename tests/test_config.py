import unittest
import tempfile
import os
from taskmaster.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.test_config = """
        programs:
          program1:
            cmd: "python script.py"
            workingdir: "/path/to/workingdir"
            env:
              VAR1: "value1"
              VAR2: "value2"
          program2:
            cmd: "python script2.py"
            workingdir: "/path/to/workingdir2"
            env:
              VAR3: "value3"
              VAR4: "value4"
        """

        self.config_file = tempfile.NamedTemporaryFile(delete=False)
        self.config_file.write(self.test_config.encode())
        self.config_file.close()

    def tearDown(self):
        os.unlink(self.config_file.name)

    def test_load_config(self):
        config = Config(self.config_file.name)
        self.assertEqual(len(config["programs"]), 2)

        program1 = config["programs"]["program1"]
        self.assertEqual(program1["cmd"], "python script.py")
        self.assertEqual(program1["workingdir"],
