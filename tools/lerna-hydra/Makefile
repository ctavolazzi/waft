# Lerna Hydra — Makefile
# Fork the repo, run `make setup && make dev`, browser pops up.
# Full stack: llama-server (Gemma-4) + PocketBase + FastAPI nerve center + browser dashboard

LLAMA_PORT   ?= 8080
NERVE_PORT   ?= 3000
PB_PORT      ?= 8090
LLAMA_BIN    ?= $(HOME)/Code/llama.cpp/build/bin/llama-server
MODEL_PATH   ?= $(HOME)/google_gemma-4-E4B-it-Q4_K_M.gguf

.PHONY: help setup dev dev-no-llama dev-minimal test clean browse

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

setup: ## Install Python dependencies
	pip install fastapi uvicorn httpx pytest

dev: ## Start everything: PocketBase + llama-server + nerve center + browser
	python3 launch.py --port $(NERVE_PORT) --llama-port $(LLAMA_PORT) \
		--pb-port $(PB_PORT) --model-path $(MODEL_PATH)

dev-no-llama: ## Start without llama-server (already running on :8080)
	python3 launch.py --port $(NERVE_PORT) --llama-port $(LLAMA_PORT) \
		--pb-port $(PB_PORT) --no-llama

dev-minimal: ## Start nerve center only (no llama, no PocketBase)
	python3 launch.py --port $(NERVE_PORT) --no-llama --no-pocketbase --no-copilotkit

test: ## Run all tests
	python3 -m pytest tests/ -v

browse: ## Open dashboard + PocketBase admin
	open http://localhost:$(NERVE_PORT)
	open http://localhost:$(PB_PORT)/_/

clean: ## Remove sandbox temp dirs and PocketBase data
	@echo "Removing sandbox temp directories..."
	rm -rf /tmp/lerna-hydra-*
	rm -rf .data/pb_data
	@echo "Done."
