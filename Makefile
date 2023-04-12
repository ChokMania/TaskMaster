run:
	taskmaster -c config.yaml

test:
	python -m unittest discover tests

lint:
	flake8 .

format:
	black .
	isort .

lint-format: lint format

install-deps:
	pip install -e .

install-deps-dev:
	pip install -e ."[dev]"

kill-usr1:
	@kill -USR1 `ps -x | grep "taskmaster" | grep -v "grep" | awk '{print $$1}'`

kill:
	@kill `ps -x | grep "taskmaster" | grep -v "grep" | awk '{print $$1}'`

kill-usr2:
	@kill -USR2 `ps -x | grep "taskmaster" | grep -v "grep" | awk '{print $$1}'`

kill-hup:
	@kill -HUP `ps -x | grep "taskmaster" | grep -v "grep" | awk '{print $$1}'`

kill-nginx:
	kill `ps -x | grep "nginx" | grep -v "grep" | grep "master process" | awk '{print $$1}'`

kill-nginx-sigterm:
	@kill -15 `ps -x | grep "nginx" | grep -v "grep" | grep "master process" | awk '{print $$1}'`

kill-nginx-sigstop:
	@kill -17 `ps -x | grep "nginx" | grep -v "grep" | grep "master process" | awk '{print $$1}'`

kill-nginx-sigint:
	@kill -2 `ps -x | grep "nginx" | grep -v "grep" | grep "master process" | awk '{print $$1}'`

kill-nginx-sigabrt:
	@kill -6 `ps -x | grep "nginx" | grep -v "grep" | grep "master process" | awk '{print $$1}'`

kill-nginx-sigkill:
	@kill -9 `ps -x | grep "nginx" | grep -v "grep" | grep "master process" | awk '{print $$1}'`

.PHONY: run test lint format install-deps install-deps-dev lint-format kill-hup  kill-usr1 kill-usr2 kill kill-nginx kill-nginx-sigterm kill-nginx-sigstop
