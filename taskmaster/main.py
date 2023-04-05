import json

from taskmaster.process_manager import ProcessManager
from taskmaster.control_shell import ControlShell
from taskmaster.logger import Logger
from taskmaster.utils import parse_args, drop_privileges

def main():
    args = parse_args()

    smtp_config = None
    if args.smtp_config:
        with open(args.smtp_config, "r") as f:
            smtp_config = json.load(f)

    syslog_config = None
    if args.syslog_config:
        with open(args.syslog_config, "r") as f:
            syslog_config = json.load(f)

    logger = Logger("TaskMaster", log_file=args.logfile, log_level=args.log_level, smtp_config=smtp_config, syslog_config=syslog_config)
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
        if args.user and args.group:
            drop_privileges(args.user, args.group)
        process_manager = ProcessManager(args.config, logger)
        process_manager.start_all()
        control_shell = ControlShell(process_manager, logger)
        control_shell.cmdloop()

if __name__ == "__main__":
    main()
