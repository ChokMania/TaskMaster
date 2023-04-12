import os
import subprocess
import signal
import time
import threading

class ProcessController:
    def __init__(self, name, config, logger):
        self.name = name
        self.config = config
        self.logger = logger
        self.process = None
        self.stdout = None
        self.stderr = None
        self.monitoring = False
        self.monitor_thread = None

    def _start_monitoring(self):
        self.logger.info("Starting monitoring")
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor)
        self.monitor_thread.start()

    def start(self):
        try:
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
                env=env,
                stdout=self.stdout,
                stderr=self.stderr,
            )
            time.sleep(self.config.get("starttime", 5))
            if self.process and self.process.poll() is None:
                self._start_monitoring()
            else:
                self.logger.warning(f"Failed to start process '{self.name}'")
        except Exception as e:
            self.logger.info(f"Failed to start process '{self.name}': {e}")

    def monitor(self):
        while self.monitoring is True:
            return_code = self.process.poll()
            if return_code is not None:
                self.handle_exit(return_code)
                break
            time.sleep(1)

    def handle_exit(self, return_code):
        autorestart = self.config.get("autorestart", "unexpected")
        exitcodes = self.config.get("exitcodes", [0])

        if autorestart == "always" or (autorestart == "unexpected" and return_code not in exitcodes):
            self.logger.warning(f"Process '{self.name}' exited with code {return_code}. Restarting...")
            self.start()
        else:
            self.logger.info(f"Process '{self.name}' exited with code {return_code}. Not restarting.")

    def stop(self):
        if not self.process or self.process.poll() is not None:
            self.logger.warning(f"Process '{self.name}' is not running")
            return

        self.monitoring = False
        stop_signal = getattr(signal, self.config.get('stopsignal', 'SIGTERM') , signal.SIGTERM)
        time.sleep(self.config.get("stoptime", 10))
        self.process.send_signal(stop_signal)

        if self.process.poll() is None:
            self.process.terminate()

        self._close_output_streams()
        self.logger.info(f"Stopped process '{self.name}'")

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