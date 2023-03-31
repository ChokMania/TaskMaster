import yaml

from program.program import Program

__all__ = [
    "Configuration",
]


class Configuration:
    def __init__(self, filepath):
        self.filepath = filepath
        self.programs = self.load()

    def load(self):
        with open(self.filepath) as f:
            data = yaml.safe_load(f)
            if not data:
                raise ValueError("Empty configuration file")
            programs = data.get("programs", {})
            if not programs:
                raise ValueError("No programs specified in configuration file")

            # Load all programs from configuration file
            programs_dict = {}
            for name, program in programs.items():
                programs_dict[name] = Program(name=name, **program)

            # Start all programs with 'autostart' set to True
            for program in programs_dict.values():
                if program.autostart:
                    program.start()

            return programs_dict


    def get_program_names(self):
        return list(self.programs.keys())

    def get_program(self, name):
        return self.programs.get(name)
