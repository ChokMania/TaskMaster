import time
import pytest

from srcs.shell import TaskmasterShell
from srcs.program import Program


def test_program_autorestart():
    # create a new program with autorestart enabled
    program = Program(name="test_program", cmd="sleep 10", autorestart="unexpected")
    # start the program
    pid = program.start()
    assert pid is not None
    # kill the program
    program.stop()
    time.sleep(1)  # wait a bit for the program to restart
    # check that the program has been restarted
    assert program.get_status() == "running"


def test_program_startretries():
    # create a new program with startretries set to 2
    program = Program(name="test_program", cmd="exit 1", startretries=2)
    # try to start the program, should fail
    with pytest.raises(SystemExit):
        program.start()
    # check that the program has been stopped
    assert program.get_status() == "stopped"


def test_shell_load_config_error():
    # create a new shell with an invalid configuration file
    with pytest.raises(SystemExit):
        shell = TaskmasterShell("invalid_config.yaml")
