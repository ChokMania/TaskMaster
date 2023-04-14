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

docker-build:
	docker build -t taskmaster-image-v1.0 ./docker/.

docker-run:
	docker run -it --name taskmaster-container-1 -v `pwd`:/shared -p 81:81 -p 80:80 taskmaster-image-v1.0

docker-exec:
	docker exec -it taskmaster-container-1 bash

docker-start:
	docker start taskmaster-container-1

docker-all: docker-build docker-run

kill-usr1:
	@kill -USR1 `ps -x | grep "taskmaster" | grep -v "grep" | awk '{print $$1}'`

kill:
	@kill `ps -x | grep "taskmaster" | grep -v "grep" | awk '{print $$1}'`

kill-usr2:
	@kill -USR2 `ps -x | grep "taskmaster" | grep -v "grep" | awk '{print $$1}'`

kill-hup:
	@kill -HUP `ps -x | grep "taskmaster" | grep -v "grep" | awk '{print $$1}'`

kill-ping:
	@kill `ps -x | grep " ping " | grep -v "grep" | grep -v "/bin/sh" | awk '{print $$1}'`

kill-ping-sigterm:
	@kill -15 `ps -x | grep " ping " | grep -v "grep" | grep -v "/bin/sh" | awk '{print $$1}'`

kill-ping-sigtop:
	@kill -17 `ps -x | grep " ping " | grep -v "grep" | grep -v "/bin/sh" | awk '{print $$1}'`

kill-ping-sigint:
	@kill -2 `ps -x | grep " ping " | grep -v "grep" | grep -v "/bin/sh" | awk '{print $$1}'`

kill-ping-sigabrt:
	@kill -6 `ps -x | grep " ping " | grep -v "grep" | grep -v "/bin/sh" | awk '{print $$1}'`

kill-ping-sigkill:
	@kill -9 `ps -x | grep " ping " | grep -v "grep" | grep -v "/bin/sh" | awk '{print $$1}'`

get-ping-umask:
	@grep '^Umask:' "/proc/`ps -x | grep " ping " | grep -v "grep" | grep -v "/bin/sh" | awk '{print $$1}'`/status"

.PHONY: run test lint format install-deps install-deps-dev lint-format kill-hup  kill-usr1 kill-usr2 kill kill-nginx kill-nginx-sigterm kill-nginx-sigstop
