import json
import daemon
import sys
import os

from daemon import pidfile
from server.process_manager import ProcessManager
from server.control_shell import ControlShell
from server.logger import Logger
from server.utils import parse_args, drop_privileges


def main():
    process_manager = None
    try:
        args = parse_args()

        # Convert the configuration file path to an absolute path
        args.config = os.path.abspath(args.config)

        smtp_config = None
        if args.smtp_config:
            with open(args.smtp_config, "r") as f:
                smtp_config = json.load(f)

        syslog_config = None
        if args.syslog_config:
            with open(args.syslog_config, "r") as f:
                syslog_config = json.load(f)

        logger = Logger(
            "TaskMaster",
            log_file=args.logfile,
            log_level=args.log_level,
            smtp_config=smtp_config,
            syslog_config=syslog_config,
        )
        logger.info("Starting TaskMaster")

        if args.user and args.group:
            drop_privileges(args.user, args.group, logger)

        if args.daemon:
            logger.info("Starting TaskMaster as a daemon")
            log_path = "/var/log/taskmaster/taskmaster.log"  # Change this path to a suitable location
            if os.path.dirname(log_path) and not os.path.exists(
                os.path.dirname(log_path)
            ):
                os.makedirs(os.path.dirname(log_path))
            with open(log_path, "a") as log_file:
                logger.info(f"Redirecting stdout and stderr to log file 'taskmaster.log' in {log_path}")
                # Close all handlers before entering daemon context
                for handler in logger.logger.handlers:
                    handler.close()
                    logger.logger.removeHandler(handler)

                context = daemon.DaemonContext(
                    pidfile=pidfile.TimeoutPIDLockFile(args.pidfile),
                    stdout=log_file,
                    stderr=log_file
                )

                with context:
                    # Re-initialize the logger with the new log file
                    logger = Logger(
                        "TaskMaster",
                        log_file=log_path,
                        log_level=args.log_level,
                        smtp_config=smtp_config,
                        syslog_config=syslog_config,
                    )
                    logger.info("Starting server")
                    process_manager = ProcessManager(args.config, logger)
                    control_shell = ControlShell(process_manager, logger)
                    logger.display_cli_prompt_method = control_shell.display_cli_prompt
                    control_shell.cmdloop()
        else:
            logger.info("Starting TaskMaster in the foreground")
            process_manager = ProcessManager(args.config, logger)
            control_shell = ControlShell(process_manager, logger)
            logger.display_cli_prompt_method = control_shell.display_cli_prompt
            control_shell.cmdloop()
    except KeyboardInterrupt:
        print("Exiting TaskMaster")
        if process_manager:
            process_manager.stop_all()
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
