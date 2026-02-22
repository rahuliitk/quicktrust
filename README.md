# QuickTrust

**Open-source, agent-first GRC platform that makes compliance fast, affordable, and automated.**

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

## Why QuickTrust?

Compliance tools like Vanta and Drata charge $20,000–$100,000+/year, putting SOC 2, ISO 27001, and other certifications out of reach for startups and SMBs. QuickTrust changes that.

QuickTrust uses **AI agents** to automate the most time-consuming parts of compliance — generating controls, mapping them to framework requirements, customizing them to your tech stack, and suggesting owners — reducing weeks of manual work to minutes.

### Goals

- **Democratize compliance**: Make enterprise-grade GRC tooling accessible to every company, regardless of budget
- **Agent-first architecture**: Use LLM-powered agents to automate control generation, evidence collection, and gap analysis — not just dashboards and checklists
- **Open-source transparency**: Compliance is about trust. Your compliance tooling should be auditable, extensible, and community-driven
- **Framework-agnostic**: Support SOC 2, ISO 27001, HIPAA, PCI DSS, and any custom framework through a pluggable framework engine

## Features

- **SOC 2 Type II** framework with 9 domains, 33 requirements, and control objectives — fully seeded and ready to use
- **25 control templates** across 8 security domains (Access Control, Network Security, Data Protection, Change Management, Logging & Monitoring, Incident Response, Endpoint Security, HR Security)
- **20 evidence templates** for structured evidence collection
- **AI controls generation agent** — give it your company context and framework, get tailored draft controls in minutes (LangGraph + LiteLLM)
- **Multi-tenant architecture** with Keycloak SSO (OIDC/PKCE)
- **Compliance dashboard** with scoring, status tracking, and framework progress
- **Full REST API** with Swagger documentation

## Quick Start

### Local Development (no Docker required)

```bash
# Clone
git clone https://github.com/rahuliitk/quicktrust.git
cd quicktrust

# Backend
cd backend
pip install -e ".[dev]"
python seeds/run_seeds.py        # Seed SOC 2 framework + templates
uvicorn app.main:app --reload    # API at http://localhost:8000

# Frontend (new terminal)
cd frontend
pnpm install
pnpm dev                         # UI at http://localhost:3000
```

### Docker Compose (full stack)

```bash
cp .env.example .env
docker compose up -d
docker compose exec api python -m seeds.run_seeds
# App at http://localhost:3000, API at http://localhost:8000, Swagger at http://localhost:8000/docs
```

See [docs/setup.md](docs/setup.md) for detailed setup instructions.

## Architecture

| Component | Technology |
|-----------|-----------|
| Frontend | Next.js 15, React 19, shadcn/ui, TanStack Query |
| Backend | FastAPI, Python 3.12, SQLAlchemy 2.0 (async) |
| Database | PostgreSQL 16 + pgvector (SQLite for local dev) |
| Auth | Keycloak 26 (OIDC/PKCE) |
| AI Agent | LangGraph + LiteLLM (any LLM provider) |
| Infrastructure | Docker Compose, Traefik, Redis, MinIO |

See [docs/architecture.md](docs/architecture.md) for the full architecture overview.

## Project Structure

```
quicktrust/
  backend/          # FastAPI API, models, services, agents, seeds
  frontend/         # Next.js UI with shadcn/ui components
  infra/            # Keycloak realm, PostgreSQL init, Traefik config
  docs/             # Setup guide, architecture docs
  docker-compose.yml
```

## Roadmap

- [ ] ISO 27001 framework support
- [ ] HIPAA framework support
- [ ] Evidence auto-collection via integrations (AWS, GitHub, Okta, etc.)
- [ ] Risk register and risk assessment workflows
- [ ] Audit preparation and auditor portal
- [ ] Policy document management
- [ ] Continuous monitoring with real-time compliance scoring
- [ ] Self-hosted deployment guides (Kubernetes, single VM)

## Contributing

Contributions are welcome! Whether it's adding a new compliance framework, improving the AI agent, or fixing a bug — we'd love your help.

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/my-feature`)
3. Commit your changes
4. Push and open a PR

Please open an issue first for large changes to discuss the approach.

## License

[GNU Affero General Public License v3.0](LICENSE) — you can use, modify, and distribute QuickTrust freely. If you host it as a service, you must share your modifications. This ensures the project stays open and benefits the community.
