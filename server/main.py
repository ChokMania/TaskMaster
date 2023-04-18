import json
import daemon
import sys
import os

from daemon import pidfile

from server.process_manager import ProcessManager
from server.control_shell import ControlShell
from server.logger import Logger
from server.utils import parse_args, drop_privileges
from server.server import TaskMasterServer


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

        # Create the log file directory if it doesn't exist
        if os.path.dirname(args.logfile) and not os.path.exists(
            os.path.dirname(args.logfile)
        ):
            os.makedirs(os.path.dirname(args.logfile))

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

        if args.server:
            logger.info("Starting TaskMaster as a server")
            with open(args.logfile, "a") as log_file:
                logger.info(
                    f"Redirecting stdout and stderr to log file 'taskmaster.log' in {args.logfile}"
                )
                # Close all handlers before entering server context
                for handler in logger.logger.handlers:
                    handler.close()
                    logger.logger.removeHandler(handler)

                context = daemon.DaemonContext(
                    pidfile=pidfile.TimeoutPIDLockFile(args.pidfile),
                    stdout=log_file,
                    stderr=log_file,
                )

                with context:
                    # Re-initialize the logger with the new log file
                    logger.info("Starting server")
                    process_manager = ProcessManager(args.config, logger)
                    server = TaskMasterServer(
                        process_manager=process_manager,
                        logger=logger,
                        host=args.server_addr,
                        port=args.server_port,
                    )
                    server.start()

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
