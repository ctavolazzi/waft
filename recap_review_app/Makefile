.PHONY: help build up down logs restart clean test health

help: ## Show this help message
	@echo "Recap and Review - Docker Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

build: ## Build Docker images
	docker-compose build backend

build-dev: ## Build development Docker image
	docker-compose build backend-dev

up: ## Start backend service
	docker-compose up -d backend

up-dev: ## Start development backend with hot reload
	docker-compose --profile dev up -d backend-dev

down: ## Stop all services
	docker-compose down

logs: ## View backend logs
	docker-compose logs -f backend

logs-dev: ## View development backend logs
	docker-compose logs -f backend-dev

restart: ## Restart backend service
	docker-compose restart backend

clean: ## Stop and remove containers, networks
	docker-compose down -v

clean-all: ## Remove containers, networks, and images
	docker-compose down --rmi all -v

test: ## Test backend health
	curl http://localhost:8000/api/health

health: ## Check backend health
	@docker-compose exec backend curl -s http://localhost:8000/api/health || echo "Backend not running"

ps: ## Show running containers
	docker-compose ps

shell: ## Open shell in backend container
	docker-compose exec backend /bin/bash

rebuild: ## Rebuild and restart backend
	docker-compose up -d --build backend

rebuild-dev: ## Rebuild and restart development backend
	docker-compose --profile dev up -d --build backend-dev
