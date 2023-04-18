import os
import subprocess
import signal
import time
import shlex

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
            os.close(0)  # Close stdin, for program like cat for example
        except Exception as e:
            self.logger.warning(f"Failed to set umask for process '{self.name}': {e}")

    def is_active(self):
        return self.process and self.process.poll() is None

    def attach(self):
        if not self.is_active():
                self.logger.warning(f"Process '{self.name}' is not running")
                return
        try:
            stdout_path = self.config['stdout']
            command = f"tail -f {stdout_path}"
            tail_process = subprocess.Popen(shlex.split(command))
            # Wait for the user to press Enter
            input("Press Enter to detach from the process...\n")

            # Terminate the tail -f process
            tail_process.terminate()
        except Exception as e:
            self.logger.error(f"Failed to attach to process '{self.name}': {e}")

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
                    self.config["cmd"],
                    shell=True,
                    cwd=self.config.get("workingdir", None),
                    env=env,
                    preexec_fn=self._initproc,
                    stdout=self.stdout,
                    stderr=self.stderr,
                )
                time.sleep(self.config.get("starttime", 5))  # TODO: Find better impl
                if (
                    self.process.poll() in self.config.get("exitcodes", [0])
                    or self.is_active()
                ):
                    self.logger.info(f"Process '{self.name}' started successfully")
                    self.monitor = True
                    break
                else:
                    self.logger.warning(
                        f"Failed to start process '{self.name}', attempt {attempt + 1}/{retries}"
                    )
            except Exception as e:
                self.logger.warning(
                    f"Failed to start process '{self.name}', attempt {attempt + 1}/{retries}: {e}"
                )
        if (
            self.process.poll() not in self.config.get("exitcodes", [0])
            and not self.is_active()
        ):
            self.logger.error(
                f"Failed to start process '{self.name}' after {retries} attempts"
            )

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

    def _get_output_stream(self, stream_type):
        output_path = self.config.get(stream_type, None)
        if output_path:
            if os.path.dirname(output_path) and not os.path.exists(
                os.path.dirname(output_path)
            ):
                os.makedirs(os.path.dirname(output_path))
            try:
                return open(output_path, "a")
            except Exception as e:
                self.logger.warning(
                    f"Failed to open {stream_type} file '{output_path}': {e}"
                )
                return subprocess.DEVNULL
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
