import argparse
import os
import sys
import pwd
import grp

def drop_privileges(user, group):
    if os.getuid() != 0:
        print("Ce programme doit être exécuté en tant que root.")
        sys.exit(1)
    try:
        # Obtenez l'UID et le GID de l'utilisateur et du groupe spécifiés
        uid = pwd.getpwnam(user).pw_uid
        gid = grp.getgrnam(group).gr_gid
        # Changez le GID du processus pour celui du groupe spécifié
        os.setgid(gid)
        # Changez l'UID du processus pour celui de l'utilisateur spécifié
        os.setuid(uid)
    except Exception as e:
        print(f"Erreur lors de la désescalade des privilèges : {e}")
        sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(description="Taskmaster - A job control daemon")
    parser.add_argument("-c", "--config", required=True, help="Path to the configuration file")
    parser.add_argument("-l", "--logfile", default="./taskmaster.log", help="Path to the log file")
    parser.add_argument("--log-level", default="INFO", help="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    parser.add_argument("-d", "--daemonize", action="store_true", help="Run Taskmaster in daemon mode")
    parser.add_argument("-u", "--user", help="User to run Taskmaster as (requires root)")
    parser.add_argument("-g", "--group", help="Group to run Taskmaster as (requires root)")
    parser.add_argument("--smtp-config", default="./taskmaster/config/smtp.json", help="Path to the SMTP configuration file (JSON format)")
    parser.add_argument("--syslog-config", default="./taskmaster/config/syslog.json", help="Path to the Syslog configuration file (JSON format)")
    return parser.parse_args()
