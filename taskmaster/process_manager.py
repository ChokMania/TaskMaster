from taskmaster.config import Config
from taskmaster.process import ProcessController

from taskmaster.config import Config
from taskmaster.process import ProcessController


class ProcessManager:
    def __init__(self, config_path, logger):
        self.config_path = config_path
        self.logger = logger
        self.processes = {}

        self.load_configuration()

    def load_configuration(self):
        config = Config(self.config_path)

        for program_name, program_config in config['programs'].items():
            self.logger.debug(f"Loading configuration for program: {program_name}")
            if program_name not in self.processes:
                self.processes[program_name] = []

            process_controller = ProcessController(program_name, program_config, self.logger)
            self.processes[program_name].append(process_controller)

    def start_all(self):
        for process_list in self.processes.values():
            for process_controller in process_list:
                process_controller.start()

    def stop_all(self):
        for process_list in self.processes.values():
            for process_controller in process_list:
                process_controller.stop()

    def restart_all(self):
        for process_list in self.processes.values():
            for process_controller in process_list:
                process_controller.restart()

    def start_process(self, process_name):
        if process_name in self.processes:
            for process_controller in self.processes[process_name]:
                process_controller.start()
        else:
            self.logger.warning(f"Process '{process_name}' not found in configuration")

    def stop_process(self, process_name):
        if process_name in self.processes:
            for process_controller in self.processes[process_name]:
                process_controller.stop()
        else:
            self.logger.warning(f"Process '{process_name}' not found in configuration")

    def restart_process(self, process_name):
        if process_name in self.processes:
            for process_controller in self.processes[process_name]:
                process_controller.restart()
        else:
            self.logger.warning(f"Process '{process_name}' not found in configuration")

    def reload_configuration(self):
        self.logger.info("Reloading configuration")
        self.stop_all()
        self.load_configuration()
        self.start_all()

    def status(self):
        for process_name, process_list in self.processes.items():
            self.logger.info(f"Process '{process_name}':")
            for idx, process_controller in enumerate(process_list):
                status = process_controller.status()
                self.logger.info(f"  Instance {idx}: {status}")

