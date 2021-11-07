.DEFAULT_GOAL := all
SOURCE_ROOT := airdrum_app

all: check

check:
	black --check ${SOURCE_ROOT}
	flake8 ${SOURCE_ROOT}
    # mypy ${SOURCE_ROOT} # mypy hangs for some reason

format:
	isort ${SOURCE_ROOT}
	black ${SOURCE_ROOT}

build:
	docker compose build

start:
	xhost local:
	python ${SOURCE_ROOT}/airdrum.py

docker-start:
	xhost local:
	docker compose up
