import argparse
import os
import sys
import pwd
import grp


def drop_privileges(user, group, logger):
    if os.getuid() != 0:
        logger.error("Ce programme doit être exécuté en tant que root.")
    try:
        uid = pwd.getpwnam(user).pw_uid
        gid = grp.getgrnam(group).gr_gid
        os.setgid(gid)
        os.setuid(uid)
    except Exception as e:
        logger.error(f"Erreur lors de la désescalade des privilèges : {e}")


def parse_args():
    parser = argparse.ArgumentParser(description="Taskmaster - A job control daemon")
    parser.add_argument(
        "-c", "--config", required=True, help="Path to the configuration file"
    )
    parser.add_argument(
        "-l", "--logfile", default="./taskmaster.log", help="Path to the log file"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    parser.add_argument(
        "-u", "--user", help="User to run Taskmaster as (requires root)"
    )
    parser.add_argument(
        "-g", "--group", help="Group to run Taskmaster as (requires root)"
    )
    parser.add_argument(
        "--smtp-config",
        default="./config/smtp.json",
        help="Path to the SMTP configuration file (JSON format)",
    )
    parser.add_argument(
        "--syslog-config",
        default="./config/syslog.json",
        help="Path to the Syslog configuration file (JSON format)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    print("This module is not meant to be run directly.")
    print("Please run main.py instead.")
