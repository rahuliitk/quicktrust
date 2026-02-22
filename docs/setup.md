# OpenComply — Local Development Setup

## Prerequisites

- Docker & Docker Compose
- Node.js 20+ and pnpm 9+
- Python 3.12+ (for local backend development)
- Git

## Quick Start

### 1. Clone and configure

```bash
git clone <repo-url> grcplatfrom
cd grcplatfrom
cp .env.example .env
```

### 2. Start all services

```bash
docker compose up -d
```

This starts 7 services:
- **PostgreSQL** (pgvector) — port 5432
- **Redis** — port 6379
- **MinIO** — ports 9000 (API), 9001 (console)
- **Keycloak** — port 8080
- **API** (FastAPI) — port 8000
- **Web** (Next.js) — port 3000
- **Traefik** — ports 80, 8081

### 3. Run database migrations

```bash
docker compose exec api alembic upgrade head
```

### 4. Seed data

```bash
docker compose exec api python -m seeds.run_seeds
```

This loads:
- SOC 2 Type II framework (9 domains, 33 requirements)
- 25 control templates
- 20 evidence templates

### 5. Verify

- API health: http://localhost:8000/health
- API docs: http://localhost:8000/docs
- Keycloak admin: http://localhost:8080 (admin/admin)
- Frontend: http://localhost:3000
- MinIO console: http://localhost:9001

### 6. Dev users

| Email | Password | Role |
|-------|----------|------|
| admin@opencomply.dev | admin123 | super_admin |
| manager@opencomply.dev | manager123 | compliance_manager |

## Local Development (without Docker)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

## Running Tests

```bash
cd backend
pip install aiosqlite  # for test database
pytest -v
```

## Environment Variables

See `.env.example` for all available configuration options.

## AI Agent Configuration

To use the controls generation agent with a real LLM:

1. Set `OPENAI_API_KEY` in `.env`
2. Optionally change `LITELLM_MODEL` (default: `gpt-4o-mini`)
3. The agent falls back to template-based generation if no API key is configured
