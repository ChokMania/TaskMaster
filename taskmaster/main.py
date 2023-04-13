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
    process_manager = ProcessManager(args.config, logger)
    control_shell = ControlShell(process_manager, logger)
    logger.display_cli_prompt_method = control_shell.display_cli_prompt
    control_shell.cmdloop()


if __name__ == "__main__":
    main()
