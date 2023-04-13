
from srcs.shell import TaskmasterShell
from srcs.signals import SignalHandler


def register_signal_handlers():
    signal_handler = SignalHandler()
    signal_handler.register_signals()


if __name__ == "__main__":
    shell = TaskmasterShell("./config/config.yaml")
    register_signal_handlers()
    shell.cmdloop()
