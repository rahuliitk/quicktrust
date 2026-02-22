# OpenComply

Open-source, agent-first GRC (Governance, Risk, and Compliance) platform.

## What is OpenComply?

OpenComply automates compliance workflows using AI agents. Instead of manually mapping controls, collecting evidence, and tracking compliance status, OpenComply uses LLM-powered agents to:

- **Generate controls** from compliance frameworks (SOC 2, ISO 27001, etc.)
- **Customize controls** to your specific tech stack and company context
- **Map controls** to framework requirements automatically
- **Suggest owners** based on your organizational structure

## Features

- Full SOC 2 Type II framework with 9 domains and 33 requirements
- 25 pre-built control templates across 8 security domains
- 20 evidence templates for automated evidence collection
- AI-powered controls generation agent (LangGraph + LiteLLM)
- Multi-tenant architecture with Keycloak SSO
- Modern dashboard with compliance scoring
- RESTful API with full Swagger documentation

## Quick Start

```bash
# Clone the repository
git clone <repo-url> opencomply
cd opencomply

# Copy environment configuration
cp .env.example .env

# Start all services
docker compose up -d

# Run database migrations
docker compose exec api alembic upgrade head

# Seed compliance data
docker compose exec api python -m seeds.run_seeds

# Open the app
open http://localhost:3000
```

See [docs/setup.md](docs/setup.md) for detailed setup instructions.

## Architecture

| Component | Technology |
|-----------|-----------|
| Frontend | Next.js 15, React 19, shadcn/ui |
| Backend | FastAPI, Python 3.12, SQLAlchemy 2.0 |
| Database | PostgreSQL 16 + pgvector |
| Auth | Keycloak 26 (OIDC/PKCE) |
| AI Agent | LangGraph + LiteLLM |
| Infrastructure | Docker Compose, Traefik, Redis, MinIO |

See [docs/architecture.md](docs/architecture.md) for the full architecture overview.

## Project Structure

```
opencomply/
  backend/          # FastAPI backend (Python)
  frontend/         # Next.js frontend (TypeScript)
  infra/            # Keycloak, PostgreSQL, Traefik configs
  docs/             # Documentation
  docker-compose.yml
```

## Development

### Backend

```bash
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

### Tests

```bash
cd backend
pytest -v
```

## Contributing

Contributions are welcome. Please open an issue first to discuss what you would like to change.

## License

[AGPLv3](LICENSE)
