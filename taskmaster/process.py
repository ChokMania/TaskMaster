import os
import subprocess
import signal
import time
import stat
import logging

class ProcessController:
    def __init__(self, name, config, logger):
        self.name = name
        self.config = config
        self.logger = logger
        self.umask = None
        self.process = None
        self.stdout = None
        self.stderr = None
        self.monitor = False

    def _initproc(self):
        try:
            os.umask(self.umask)
        except Exception as e:
            self.logger.warning(f"Failed to set umask for process '{self.name}': {e}")

    def is_active(self):
        return self.process and self.process.poll() is None

    def start(self):
        retries = self.config.get("startretries", 3)
        for attempt in range(retries):
            try:
                if self.is_active():
                    self.logger.warning(f"Process '{self.name}' is already running")
                    return

                env = os.environ.copy()
                env.update(self.config.get("env", {}))

                self.stdout = self._get_output_stream("stdout")
                self.stderr = self._get_output_stream("stderr")
                self.umask = self.config.get("umask", "022")
                self.process = subprocess.Popen(
                    self.config['cmd'],
                    shell=True,
                    cwd=self.config.get("workingdir", None),
                    env=env,
                    preexec_fn=self._initproc,
                    stdout=self.stdout,
                    stderr=self.stderr,
                )
                time.sleep(self.config.get("starttime", 5)) # TODO: Find better impl
                if self.is_active():
                    self.logger.info(f"Process '{self.name}' started successfully")
                    self.monitor = True
                    break
                else:
                    self.logger.warning(f"Failed to start process '{self.name}', attempt {attempt + 1}/{retries}")
            except Exception as e:
                self.logger.warning(f"Failed to start process '{self.name}', attempt {attempt + 1}/{retries}: {e}")
        if self.process.poll() is not None:
            self.logger.error(f"Failed to start process '{self.name}' after {retries} attempts")

    def terminate_process(self):
        self.monitor = False
        self.process.terminate()
        self._close_output_streams()
        self.logger.info(f"Process '{self.name}' terminated successfully")

    def stop(self):
        stop_signal = getattr(
            signal, self.config.get("stopsignal", "SIGTERM"), signal.SIGTERM
        )
        time.sleep(self.config.get("stoptime", 10))
        self.process.send_signal(stop_signal)

        self.terminate_process()

    def restart(self):
        self.stop()
        self.start()

    def status(self):
        if self.process:
            return_code = self.process.poll()
            if return_code is None:
                return "running"
            elif return_code == 0:
                return "completed"
            else:
                return f"stopped (return code: {return_code})"
        else:
            return "stopped"

    def attach(self):
        if not self.process or self.process.poll() is not None:
            self.logger.warning(f"Process '{self.name}' is not running")
            return
        self.logger.info(f"Attaching to process '{self.name}'")
        try:
            env = os.environ.copy()
            env.update(self.config.get("env", {}))

            child = subprocess.Popen(
                self.config["cmd"],
                shell=True,
                cwd=self.config.get("workingdir", None),
                env=env,
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


if __name__ == "__main__":
    print("This module is not meant to be run directly.")
    print("Please run main.py instead.")
