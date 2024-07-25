.PHONY: compile install venv

compile:
	uv pip compile requirements.in -o requirements.txt

venv:
	python -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip && pip install uv

install: venv
	. .venv/bin/activate && uv pip install -r requirements.txt
