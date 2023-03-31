import subprocess

from utils.logger import TaskmasterLogger

__all__ = [
    "Program",
]


class Program:
    def __init__(
        self,
        name,
        cmd,
        numprocs=1,
        autostart=False,
        autorestart="unexpected",
        exitcodes=[0],
        startretries=3,
        starttime=5,
        stopsignal="TERM",
        stoptime=10,
        workingdir=None,
        umask=None,
        stdout=None,
        stderr=None,
        env=None,
    ):
        self.name = name
        self.cmd = cmd
        self.numprocs = numprocs
        self.autostart = autostart
        self.autorestart = autorestart
        self.exitcodes = exitcodes
        self.startretries = startretries
        self.starttime = starttime
        self.stopsignal = stopsignal
        self.stoptime = stoptime
        self.workingdir = workingdir
        self.umask = umask
        self.stdout = stdout
        self.stderr = stderr
        self.env = env
        self.processes = []
        self.logger = TaskmasterLogger()

    def start(self):
        self.logger.log_event(
            f"Starting program {self.name} with command '{self.cmd}'..."
        )
        self.process = subprocess.Popen(
            self.cmd,
            cwd=self.workingdir,
            env=self.env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        self.logger.log_event(
            f"Program {self.name} started with PID {self.process.pid}"
        )
        return self.process.pid

    def stop(self):
        # Stop the program processes
        for process in self.processes:
            process.terminate()

    def get_status(self):
        # Check the status of the program processes
        for process in self.processes:
            if process.poll() is None:
                # At least one process is still running
                return "running"
        # All processes have exited
        return "stopped"
