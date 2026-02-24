.PHONY: help dev dev-backend dev-frontend build lint test test-backend test-frontend format migrate seed clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# === Development ===

dev: ## Start all services via Docker Compose
	docker compose up

dev-backend: ## Start only the API service
	docker compose up api

dev-frontend: ## Start the frontend dev server locally
	cd frontend && pnpm dev

# === Build ===

build: ## Build frontend for production
	cd frontend && pnpm build

docker-build: ## Build Docker images for backend and frontend
	docker build -t quicktrust-api --target production backend/
	docker build -t quicktrust-web --target production frontend/

# === Quality ===

lint: ## Run linters (backend + frontend)
	cd backend && ruff check . && ruff format --check .
	cd frontend && pnpm lint

format: ## Auto-format code
	cd backend && ruff format .
	cd frontend && pnpm lint --fix

test: test-backend test-frontend ## Run all tests

test-backend: ## Run backend tests
	cd backend && pytest --tb=short -q

test-frontend: ## Run frontend type check
	cd frontend && pnpm exec tsc --noEmit

# === Database ===

migrate: ## Run database migrations
	cd backend && alembic upgrade head

migrate-new: ## Create a new migration (usage: make migrate-new MSG="description")
	cd backend && alembic revision --autogenerate -m "$(MSG)"

seed: ## Seed the database with sample data
	docker compose exec api python -m seeds.run_seeds

# === Utilities ===

clean: ## Clean up Docker volumes and build artifacts
	docker compose down -v
	rm -rf frontend/.next frontend/node_modules/.cache
	rm -f backend/quicktrust.db

logs: ## Tail all service logs
	docker compose logs -f

shell-api: ## Open a shell in the API container
	docker compose exec api bash

shell-db: ## Open a psql shell
	docker compose exec postgres psql -U quicktrust -d quicktrust
