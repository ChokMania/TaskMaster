import yaml
from typing import Literal

class Config:
    def __init__(self, config_path):
        self.config_path = config_path
        self.load()

    def validate_config(self):
        if not isinstance(self.data, dict):
            raise ValueError("Config file must be a dictionary")

        if not self.data or self.data == {} or not self.data["programs"] or self.data["programs"] == {}:
            return

        for program_name, program in self.data["programs"].items():
            if not isinstance(program, dict):
                raise ValueError("The 'program' key must have a dictionary value")

            if "cmd" not in program:
                raise ValueError("Mandatory field 'cmd' is missing in the program configuration")
            if "numprocs" not in program:
                raise ValueError("Mandatory field 'numprocs' is missing in the program configuration")
            if "autostart" not in program:
                raise ValueError("Mandatory field 'autostart' is missing in the program configuration")
            if "autorestart" not in program:
                raise ValueError("Mandatory field 'autorestart' is missing in the program configuration")

            if not isinstance(program["numprocs"], int) or not (1 <= program["numprocs"] <= 10):
                raise ValueError("The 'numprocs' field must be an integer between 1 and 10")

            if not isinstance(program["autostart"], bool):
                raise ValueError("The 'autostart' field must be a boolean (true or false)")

            if not isinstance(program["startretries"], int) or program["startretries"] <= 0:
                raise ValueError("The 'startretries' field must be an integer greater than 0")

            if not isinstance(program["starttime"], int) or program["starttime"] <= 0:
                raise ValueError("The 'starttime' field must be an integer greater than 0")

        autorestart_values = ["never", "always", "unexpected"]
        if program["autorestart"] not in autorestart_values:
            raise ValueError(f"Invalid value for 'autorestart', allowed values are: {autorestart_values}")

        program.setdefault("stopsignal", "SIGTERM")
        program.setdefault("startretries", 3)
        program.setdefault("starttime", 3)
        program.setdefault("stdout", f"/tmp/{program_name}.stdout")
        program.setdefault("stderr", f"/tmp/{program_name}.stderr")

        program.setdefault("exitcodes", [0, 2, 143])
        program.setdefault("env", {})

    def load(self):
        with open(self.config_path, "r") as config_file:
            self.data = yaml.safe_load(config_file)
            self.validate_config()

    # Ajouter cette méthode pour rendre l'objet Config subscriptable
    def __getitem__(self, key):
        return self.data[key]

    def __repr__(self):
        return f"Config({self.config_path})"
