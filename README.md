# Taskmaster

Taskmaster is a process control system that provides an interface for managing and monitoring processes. It is built in Python and allows you to easily manage multiple processes using a configuration file. Taskmaster can be used in both client-server mode or standalone mode.

## Getting Started

To get started with Taskmaster, you'll need to first clone the repository:

```bash
git clone https://github.com/ChokMania/taskmaster.git
```

Once you have the repository cloned, navigate to the project directory and install the package using `pip`:

```bash
cd taskmaster
pip install ."[dev]"
```

Now, you can run the Taskmaster using the entry points.

run standalone taskmaster:

```bash
taskmaster_server -c path/to/config
```

run in server mode:

```bash
taskmaster_server -c path/to/config --server
```

run the client:

```bash
taskmaster_client
```

You can check the Makefile for a lot of usefull commands.

## Configuration

Taskmaster uses a YAML configuration file to define the processes that you want to manage. The configuration file is located at config.yml by default, but you can specify a different file using the --config command line argument.

Here is an example configuration file:

```yaml
processes:
  web:
    cmd: python app.py
    workingdir: /path/to/working/dir
    stdout: /path/to/log/file
    stderr: /path/to/log/file
    startretries: 3
    starttime: 5
    exitcodes: [0, 2]
  worker:
    cmd: python worker.py
    workingdir: /path/to/working/dir
    stdout: /path/to/log/file
    stderr: /path/to/log/file
    startretries: 3
    starttime: 5
    exitcodes: [0, 2]
```

This configuration file defines two processes: web and worker. Each process is defined by a dictionary that contains the following keys:

- cmd: The command that should be run to start the process.
- workingdir: The working directory that the process should be run in.
- stdout: The file that the process's standard output should be written to.
- stderr: The file that the process's standard error should be written to.
- startretries: The number of times that Taskmaster should attempt to start the process if it fails to start.
- starttime: The amount of time that Taskmaster should wait between attempts to start the process.
- exitcodes: The exit codes that are considered successful for the process.

## Usage

Once you have your configuration file set up, you can use Taskmaster to manage your processes. Here are some of the commands that you can use:

- start <process>: Start a process.
- stop <process>: Stop a process.
- restart <process>: Restart a process.
- reload <path_to_new_config>: Reload the configuration file.
- status: Display the status of all processes.
- attach <process>: Attach to a running process.
- detach <process>: Detach from a running process.
- config: Display the configuration of all processes.
- quit: Quit Taskmaster.

You can also send signals to Taskmaster to perform certain actions:

- SIGINT, SIGTERM, SIGABRT: Stop all processes and exit Taskmaster.
- SIGHUP: Reload the configuration file and restart all processes.
- SIGUSR1: Display the current status of all processes.
- SIGUSR2: Toggle the logging level between INFO and DEBUG.

## Author

Created by Sithi5 and ChokMania.

## Contributing

Feel free to contribute ! Simply fork the repository, create a new branch, and submit a pull request when you're ready.

If you have any suggestions or issues, please submit an issue on the GitHub repository.
