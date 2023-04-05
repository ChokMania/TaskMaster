import os
import subprocess
import signal
import time


class ProcessController:
    def __init__(self, name, config, logger):
        self.name = name
        self.config = config
        self.logger = logger
        self.process = None
        self.stdout = None
        self.stderr = None

    def start(self):
        if self.process and self.process.poll() is None:
            self.logger.warning(f"Process '{self.name}' is already running")
            return

        env = os.environ.copy()
        env.update(self.config.get("env", {}))

        self.stdout = self._get_output_stream("stdout")
        self.stderr = self._get_output_stream("stderr")

        self.process = subprocess.Popen(
            self.config["cmd"],
            shell=True,
            cwd=self.config.get("workingdir", None),
            # env=env,
            stdout=self.stdout,
            stderr=self.stderr,
        )
        self.logger.info(f"Started process '{self.name}' with PID {self.process.pid}")

    def stop(self):
        if not self.process or self.process.poll() is not None:
            self.logger.warning(f"Process '{self.name}' is not running")
            return

        stop_signal = getattr(signal, self.config.get("stopsignal", "TERM"))
        self.process.send_signal(stop_signal)
        time.sleep(self.config.get("stoptime", 10))

        if self.process.poll() is None:
            self.process.terminate()

        self._close_output_streams()
        self.logger.info(f"Stopped process '{self.name}'")

    def restart(self):
        self.stop()
        self.start()

    def status(self):
        if self.process and self.process.poll() is None:
            return "running"
        else:
            return "stopped"

    def attach(self):
        if not self.process or self.process.poll() is not None:
            self.logger.warning(f"Process '{self.name}' is not running")
            return
        self.logger.info(f"Attaching to process '{self.name}'")
        try:
            child = subprocess.Popen(
                self.config["cmd"],
                shell=True,
                cwd=self.config.get("workingdir", None),
                # env=env,
            )
            child.communicate()
        except Exception as e:
            self.logger.warning(f"Error attaching to process '{{self.name}}': {e}")

    def _get_output_stream(self, stream_type):
        output_path = self.config.get(stream_type, None)
        if output_path:
            return open(output_path, "a")
        else:
            return subprocess.DEVNULL

    def _close_output_streams(self):
        if self.stdout:
            self.stdout.close()
        if self.stderr:
            self.stderr.close()
