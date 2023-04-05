.PHONY: run test lint format install-deps

run:
	python main.py

test:
	python -m unittest discover tests

lint:
	flake8 .

format:
	black .
	isort .

install-deps:
	pip install -r requirements.txt