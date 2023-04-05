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

.PHONY: run test lint format install-deps install-deps-dev lint-format
