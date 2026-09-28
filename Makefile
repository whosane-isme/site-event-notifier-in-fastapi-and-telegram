.PHONY: all venv reload

all:
	source venv/bin/activate && uvicorn main:app --reload

venv:
	bash -c 'source venv/bin/activate && exec bash'

reload:
	venv/bin/uvicorn main:app --reload
