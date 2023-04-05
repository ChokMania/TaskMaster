import argparse
from taskmaster.process_manager import ProcessManager
from taskmaster.control_shell import ControlShell
from taskmaster.logger import Logger


def parse_args():
    parser = argparse.ArgumentParser(description="Taskmaster - A job control daemon")
    parser.add_argument("-c", "--config", required=True, help="Path to the configuration file")
    parser.add_argument("-l", "--logfile", default="taskmaster.log", help="Path to the log file")
    parser.add_argument("--log-level", default="INFO", help="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    parser.add_argument("-d", "--daemonize", action="store_true", help="Run Taskmaster in daemon mode")
    parser.add_argument("-u", "--user", help="User to run Taskmaster as (requires root)")
    parser.add_argument("-g", "--group", help="Group to run Taskmaster as (requires root)")
    return parser.parse_args()

def main():
    args = parse_args()
    logger = Logger("TaskMaster", log_level=args.log_level, log_file=args.logfile)
    logger.info("Starting TaskMaster")

    if args.daemonize:
        if not args.user or not args.group:
            logger.error("Both user and group must be specified when running in daemon mode.")
            return

        try:
            import daemon
            from daemon import pidfile
            from pwd import getpwnam
            from grp import getgrnam
        except ImportError:
            logger.error("Python 'daemon' package is required to run Taskmaster in daemon mode.")
            return

        context = daemon.DaemonContext(
            uid=getpwnam(args.user).pw_uid,
            gid=getgrnam(args.group).gr_gid,
            pidfile=pidfile.TimeoutPIDLockFile("taskmaster.pid"),
            stdout=open(args.logfile, "w+"),
            stderr=open(args.logfile, "w+"),
        )

        with context:
            process_manager = ProcessManager(args.config, logger)
            process_manager.start_all()
            control_shell = ControlShell(process_manager, logger)
            control_shell.cmdloop()

    else:
        process_manager = ProcessManager(args.config, logger)
        process_manager.start_all()
        control_shell = ControlShell(process_manager, logger)
        control_shell.cmdloop()

if __name__ == "__main__":
    main()
