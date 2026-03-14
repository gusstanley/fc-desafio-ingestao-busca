.PHONY: setup venv ingest chat

setup:
	python3.13 -m venv venv
	venv/bin/pip install -r requirements.txt

venv:
	@bash -c "source venv/bin/activate && exec bash"

ingest:
	venv/bin/python src/ingest.py

chat:
	venv/bin/python src/chat.py
