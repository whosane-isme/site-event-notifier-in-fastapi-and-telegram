ifeq ($(OS),Windows_NT)
PYTHON ?= py -3
VENV_PYTHON = .venv/Scripts/python.exe
else
PYTHON ?= python3
VENV_PYTHON = .venv/bin/python
endif

.PHONY: setup venv run uvicorn

setup:
	$(PYTHON) -m venv .venv
	$(VENV_PYTHON) -m pip install -r requirements.txt

venv: setup

run:
	$(VENV_PYTHON) -m uvicorn main:app --reload

uvicorn: run
