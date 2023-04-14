import threading
import time

from taskmaster.config import Config
from taskmaster.process import ProcessController

import json

class ProcessManager:
    def __init__(self, config_path, logger):
        self.config_path = config_path
        self.logger = logger
        self.processes = {}
        self._monitoring = False
        self._load_configuration()
        self._start_monitoring()

    def _load_configuration(self):
        try:
            config = Config(self.config_path)
        except Exception as e:
            self.logger.error(f"Error while loading configuration: {e}")
            return

        if not config["programs"]:
            self.logger.error("No program found in configuration file")
            return
        for program_name, program_config in config["programs"].items():
            self.logger.info(f"Loading configuration for program '{program_name}'")
            if program_name not in self.processes:
                self.processes[program_name] = []

            numprocs = program_config.get("numprocs", 1)
            if numprocs < 1 or numprocs > 10:
                self.logger.error(
                    f"Invalid number of processes for program '{program_name}'"
                )
                continue
            for i in range(numprocs):
                process_name = f"{program_name}_{i}" if numprocs > 1 else program_name
                process_controller = ProcessController(
                    name=process_name, config=program_config, logger=self.logger
                )
                if process_controller.config.get("autostart", False):
                    process_controller.start()
                self.processes[program_name].append(process_controller)



    def _start_monitoring(self):
        """Start monitoring all active processes"""
        self._monitoring = True
        self.logger.info(f"Starting monitoring all actives processes")
        self.monitor_thread = threading.Thread(target=self._monitor)
        self.monitor_thread.start()

    def _monitor(self):
        while self._monitoring is True:
            for process_list in self.processes.values():
                for process_controller in process_list:
                    if process_controller.monitor is False:
                        continue
                    return_code = process_controller.process.poll()
                    if return_code is not None:
                        autorestart = process_controller.config.get(
                            "autorestart", "unexpected"
                        )
                        exitcodes = process_controller.config.get("exitcodes", [0])
                        process_name = process_controller.name
                        if autorestart == "always" or (
                            autorestart == "unexpected" and return_code not in exitcodes
                        ):
                            self.logger.info(
                                f"\nProcess '{process_name}' exited with code {return_code}. Restarting...",
                            )
                            process_controller.restart()
                            self.logger.redisplay_cli_prompt()
                        else:
                            self.logger.info(
                                f"\nProcess '{process_name}' exited with code {return_code}. stopping.",
                            )
                            process_controller.monitor = False
                            process_controller.terminate_process()
                            self.logger.redisplay_cli_prompt()
            time.sleep(1)


    def display_process_config(self, arg):
        if arg in self.processes:
            for process_controller in self.processes[arg]:
                self.logger.info(f"Process '{arg}':")
                self.logger.info(json.dumps(process_controller.config, indent=4))
        else:
            self.logger.warning(f"Process '{arg}' not found in configuration")

    def start_all(self):
        self._monitoring = True
        for process_list in self.processes.values():
            for process_controller in process_list:
                process_controller.start()

    def stop_all(self):
        self._monitoring = False
        for process_list in self.processes.values():
            for process_controller in process_list:
                if process_controller.is_active():
                    process_controller.stop()

    def restart_all(self):
        self._monitoring = False
        for process_list in self.processes.values():
            for process_controller in process_list:
                process_controller.restart()
        self._monitoring = True

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
        try:
            new_config = Config(self.config_path)
        except Exception as e:
            self.logger.error(f"Error while reloading configuration: {e}")
            return

        if not new_config["programs"]:
            self.logger.error("No program found in configuration file")
            new_program_names = set()
        else:
            new_program_names = set(new_config["programs"].keys())
        old_program_names = set(self.processes.keys())

        self.remove_old_config_programs(old_program_names, new_program_names)
        self.add_new_config_programs(new_config, new_program_names, old_program_names)
        self.update_existing_programs(new_config, old_program_names, new_program_names)

        self.logger.info("Configuration reloaded.")

    def remove_old_config_programs(self, old_program_names, new_program_names):
        for program_name in old_program_names - new_program_names:
            self.stop_process(program_name)
            del self.processes[program_name]

    def add_new_config_programs(self, new_config, new_program_names, old_program_names):
        for program_name in new_program_names - old_program_names:
            program_config = new_config["programs"][program_name]
            self.processes[program_name] = []
            for i in range(program_config["numprocs"]):
                process_name = f"{program_name}_{i}" if program_config["numprocs"] > 1 else program_name
                process_controller = ProcessController(
                    name=process_name, config=program_config, logger=self.logger
                )
                self.processes[program_name].append(process_controller)
                process_controller.start()

    def update_existing_programs(
        self, new_config, old_program_names, new_program_names
    ):
        for program_name in old_program_names & new_program_names:
            old_program_config = self.processes[program_name][0].config
            new_program_config = new_config["programs"][program_name]
            if self.is_config_different(old_program_config, new_program_config):
                self.logger.debug(f"Configuration changed for program: {program_name}")
                old_program_numprocs = old_program_config["numprocs"]
                new_program_numprocs = new_program_config["numprocs"]
                if new_program_numprocs > old_program_numprocs:
                    # update config for existing processes
                    for process_controller in self.processes[program_name]:
                        process_controller.config = new_program_config
                    self.restart_process(program_name)
                    # add new processes
                    for i in range(old_program_numprocs, new_program_numprocs):
                        process_name = f"{program_name}_{i}"
                        process_controller = ProcessController(
                            name=process_name, config=new_program_config, logger=self.logger
                        )
                        self.processes[program_name].append(process_controller)
                        process_controller.start()
                elif new_program_numprocs < old_program_numprocs:
                    # stop and remove processes
                    for i in range(old_program_numprocs, new_program_numprocs, -1):
                        process_controller = self.processes[program_name][i -1]
                        process_controller.stop()
                        del self.processes[program_name][i-1]
                    # update config for existing processes
                    for i in range(new_program_numprocs):
                        process_controller = self.processes[program_name][i]
                        process_controller.config = new_program_config
                    self.restart_process(program_name)
                else:
                    for process_controller in self.processes[program_name]:
                        process_controller.config = new_program_config
                    self.restart_process(program_name)

    def is_config_different(self, old_config, new_config):
        return old_config != new_config

    def status(self):
        if not self.processes.items():
            self.logger.info("No process configured")
            return
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

    def detach_process(self, process_name):
        raise NotImplementedError


if __name__ == "__main__":
    print("This module is not meant to be run directly.")
    print("Please run main.py instead.")
