PWD = $(shell pwd)

MODULE = agi_rnd
IMAGE_TAG ?= $(MODULE)
GITHUB_SHA ?= $(MODULE)

test:
	@pytest

lint:
	@ruff --select=E9,F63,F7,F82 --ignore E501 --ignore F401 --target-version=py311 .

all: lint test

.PHONY: all fmt lint test install test-up test-down up down ps build generate build-workspace run-workspace
