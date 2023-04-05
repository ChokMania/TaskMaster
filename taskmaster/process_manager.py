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
        new_config = Config(self.config_path)

        new_program_names = set(new_config['programs'].keys())
        old_program_names = set(self.processes.keys())

        self.remove_old_processes(old_program_names, new_program_names)
        self.add_new_processes(new_config, new_program_names, old_program_names)
        self.update_existing_processes(new_config, old_program_names, new_program_names)

        self.logger.info("Configuration reloaded.")

    def remove_old_processes(self, old_program_names, new_program_names):
        for program_name in old_program_names - new_program_names:
            self.stop_process(program_name)
            del self.processes[program_name]

    def add_new_processes(self, new_config, new_program_names, old_program_names):
        for program_name in new_program_names - old_program_names:
            program_config = new_config['programs'][program_name]
            process_controller = ProcessController(program_name, program_config, self.logger)
            self.processes[program_name] = [process_controller]
            process_controller.start()

    def update_existing_processes(self, new_config, old_program_names, new_program_names):
        for program_name in old_program_names & new_program_names:
            old_program_config = self.processes[program_name][0].config
            new_program_config = new_config['programs'][program_name]

            if self.is_config_different(old_program_config, new_program_config):
                self.logger.debug(f"Configuration changed for program: {program_name}")
                self.restart_process(program_name)
                for process_controller in self.processes[program_name]:
                    process_controller.config = new_program_config

    def is_config_different(self, old_config, new_config):
        return old_config != new_config

    def status(self):
        for process_name, process_list in self.processes.items():
            self.logger.info(f"Process '{process_name}':")
            for idx, process_controller in enumerate(process_list):
                status = process_controller.status()
                self.logger.info(f"  Instance {idx}: {status}")

    def attach_process(self, process_name):
        if process_name in self.processes:
            for process_controller in self.processes[process_name]:
                process_controller.attach()
        else:
            self.logger.warning(f"Process '{process_name}' not found in configuration")