.PHONY: setup venv

setup:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

venv:
	@bash -c "source venv/bin/activate && exec bash"
