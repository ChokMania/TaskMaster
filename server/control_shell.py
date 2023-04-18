import cmd
import signal
import logging
from server.logger import Logger
import readline
import atexit
import sys
import io

class ControlShell(cmd.Cmd):
    intro = "\nTaskmaster Control Shell. Type help or ? to list commands.\n"
    prompt = "(taskmaster) "

    def __init__(self, process_manager, logger: Logger, daemonised=False):
        super(ControlShell, self).__init__()
        self.logger = logger
        self.daemonised = daemonised
        self.process_manager = process_manager
        self.setup_signal_handlers()
        self.setup_history()

    def onecmd(self, line):
        if self.daemonised:
            # Redirect stdout to a StringIO object
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()

            # Call the superclass method
            super().onecmd(line)

            # Get the output from StringIO and restore stdout
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout

            return output
        else:
            return super().onecmd(line)

    def setup_history(self):
        history_file = ".taskmaster_history"
        try:
            readline.read_history_file(history_file)
        except FileNotFoundError:
            pass
        atexit.register(self.save_history, history_file)

    def save_history(self, history_file):
        readline.write_history_file(history_file)

    def display_cli_prompt(self):
        self.stdout.write(self.prompt)
        self.stdout.flush()

    def do_history(self, arg):
        "Display the command history"
        num_commands = readline.get_current_history_length()
        if num_commands == 0:
            print("No command history available.")
        else:
            print("Command history:")
            for i in range(num_commands):
                print(f"{i + 1}: {readline.get_history_item(i + 1)}")

    def do_attach(self, arg):
        "Attach to a process: ATTACH <process name> [instance_number]"
        args = arg.split()
        if len(args) == 0:
            self.logger.error("No process name provided.")
            return

        process_name = args[0]
        instance_number = None
        if len(args) > 1:
            try:
                instance_number = int(args[1])
            except ValueError:
                self.logger.error("Invalid instance number provided.")
                return

        self.process_manager.attach_instance(process_name, instance_number)

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

    def do_startall(self, arg):
        "Start all processes"
        self.process_manager.start_all()

    def do_stop(self, arg):
        "Stop a process: STOP <process name>"
        self.logger.error("Stopping process..")
        self.process_manager.stop_process(arg)

    def do_stopall(self, arg):
        "Stop all processes"
        self.process_manager.stop_all()

    def do_restart(self, arg):
        "Restart a process: RESTART <process name>"
        self.process_manager.restart_process(arg)

    def do_reload(self, arg):
        "Reload the configuration file"
        self.process_manager.reload_configuration(arg)

    def do_quit(self, arg):
        "Exit the Taskmaster Control Shell"
        self.process_manager.stop_all()
        self.logger.info("Exiting Taskmaster Control Shell")
        return True

    def do_exit(self, arg):
        "Exit the Taskmaster Control Shell"
        return self.do_quit(arg)

    def do_EOF(self, arg):
        "Exit the Taskmaster Control Shell using Ctrl-D"
        self.logger.warning(f"Received signal EOF. Stopping all processes.")
        return self.do_quit(arg)

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
            self.logger.warning(f"\nReceived signal {signum}.")
            if signum in (signal.SIGINT, signal.SIGTERM, signal.SIGABRT):
                self.logger.warning(f"Stopping all processes.")
                self.process_manager.stop_all()
                self.logger.info("All processes stopped. Exiting.")
                exit(0)
            elif signum == signal.SIGHUP:
                self.logger.warning(
                    f"Reloading configuration and restarting processes."
                )
                self.process_manager.reload_configuration()
            elif signum == signal.SIGUSR1:
                self.logger.warning(f"Displaying current process status.")
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
