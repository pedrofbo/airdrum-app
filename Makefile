.DEFAULT_GOAL := all
SOURCE_ROOT := airdrum_app

all: check

check:
	black --check --line-length 120 ${SOURCE_ROOT}
	mypy -m ${SOURCE_ROOT}

format:
	isort ${SOURCE_ROOT}
	black --line-length 120 ${SOURCE_ROOT}

start:
	xhost local:
	docker compose up