PY := python3
VENV := .venv
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn
STREAMLIT := $(VENV)/bin/streamlit

.PHONY: help install env backend frontend start stop clean freeze

help:
	@echo "Targets:"
	@echo "  install  - create venv and install deps"
	@echo "  env      - create local .env if missing"
	@echo "  start    - run backend (8000) + UI (8501)"
	@echo "  backend  - run backend only"
	@echo "  frontend - run UI only"
	@echo "  stop     - stop background processes"
	@echo "  clean    - remove venv/cache"
	@echo "  freeze   - update requirements.txt"

install:
	$(PY) -m venv $(VENV)
	$(PIP) install -U pip
	$(PIP) install -r requirements.txt

env:
	@[ -f .env ] || cp .env.example .env

backend:
	$(UVICORN) backend.main:app --host 127.0.0.1 --port 8000 --reload

frontend:
	cd frontend && API_URL=http://127.0.0.1:8000 $(STREAMLIT) run app.py --server.address 127.0.0.1 --server.port 8501

start: install env
	@echo "Starting backend on :8000"
	$(UVICORN) backend.main:app --host 127.0.0.1 --port 8000 --reload &
	echo $$! > .backend.pid
	@echo "Starting UI on :8501"
	cd frontend && API_URL=http://127.0.0.1:8000 $(STREAMLIT) run app.py --server.address 127.0.0.1 --server.port 8501

stop:
	@[ -f .backend.pid ] && kill `cat .backend.pid` 2>/dev/null || true
	@rm -f .backend.pid
	@pkill -f "streamlit run frontend/app.py" 2>/dev/null || true

clean: stop
	rm -rf .chroma .streamlit $(VENV) **/__pycache__ .pytest_cache

freeze:
	$(PIP) freeze > requirements.txt
