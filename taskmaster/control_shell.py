import cmd
import signal
import logging
from taskmaster.logger import Logger
from taskmaster.process_manager import ProcessManager


class ControlShell(cmd.Cmd):
    intro = "\nTaskmaster Control Shell. Type help or ? to list commands.\n"
    prompt = "(taskmaster) "

    def __init__(self, process_manager, logger: Logger):
        super(ControlShell, self).__init__()
        self.logger = logger
        self.process_manager = process_manager
        self.setup_signal_handlers()

    def display_cli_prompt(self):
        self.stdout.write(self.prompt)
        self.stdout.flush()

    def do_config(self, arg):
        "Display the config of all processes"
        if not arg:
            arg = " ".join(self.process_manager.processes.keys())
        for process in arg.split():
            self.process_manager.display_process_config(process)

    def do_status(self, arg):
        "Display the status of all processes"
        self.process_manager.status()

    def do_start(self, arg):
        "Start a process: START <process name>"
        self.process_manager.start_process(arg)

    def do_stop(self, arg):
        "Stop a process: STOP <process name>"
        self.logger.error("Stopping process..")
        self.process_manager.stop_process(arg)

    def do_restart(self, arg):
        "Restart a process: RESTART <process name>"
        self.process_manager.restart_process(arg)

    def do_reload(self, arg):
        "Reload the configuration file"
        self.process_manager.reload_configuration(arg)

    def do_quit(self, arg):
        "Exit the Taskmaster Control Shell"
        self.process_manager.stop_all()
        print("Exiting Taskmaster Control Shell")
        return True

    def do_EOF(self, arg):
        "Exit the Taskmaster Control Shell using Ctrl-D"
        self.logger.warning(f"Received signal EOF. Stopping all processes.")
        return self.do_quit(arg)

    def do_attach(self, arg):
        "Attach to a running process: ATTACH <process name>"
        self.process_manager.attach_process(arg)

    def do_detach(self, arg):
        "Detach from a running process: DETACH <process name>"
        self.process_manager.detach_process(arg)

    def setup_signal_handlers(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGABRT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGQUIT, self.signal_handler)
        signal.signal(signal.SIGHUP, self.signal_handler)
        signal.signal(signal.SIGUSR1, self.signal_handler)
        signal.signal(signal.SIGUSR2, self.signal_handler)

    def signal_handler(self, signum, frame):
        try:
            self.logger.warning(
                    f"\nReceived signal {signum}."
                )
            if signum in (signal.SIGINT, signal.SIGTERM, signal.SIGABRT):
                self.logger.warning(
                    f"Stopping all processes."
                )
                self.process_manager.stop_all()
                self.logger.info("All processes stopped. Exiting.")
                exit(0)
            elif signum == signal.SIGHUP:
                self.logger.warning(
                    f"Reloading configuration and restarting processes."
                )
                self.process_manager.reload_configuration()
            elif signum == signal.SIGUSR1:
                self.logger.warning(
                    f"Displaying current process status."
                )
                self.process_manager.status()
            elif signum == signal.SIGUSR2:
                self.toggle_logging_level()
            self.display_cli_prompt()
        except Exception as e:
            self.logger.error(f"Error while handling signal {signum}: {e}")

    def toggle_logging_level(self):
        current_level = self.logger.logger.getEffectiveLevel()
        if current_level == logging.INFO:
            self.logger.logger.setLevel(logging.DEBUG)
            self.logger.info("Switched logging level to DEBUG.")
        else:
            self.logger.logger.setLevel(logging.INFO)
            self.logger.info("Switched logging level to INFO.")



if __name__ == "__main__":
    print("This module is not meant to be run directly.")
    print("Please run main.py instead.")
