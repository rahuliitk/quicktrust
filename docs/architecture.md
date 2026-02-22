# OpenComply Architecture

## Overview

OpenComply is an open-source, agent-first GRC (Governance, Risk, and Compliance) platform. It uses AI agents to automate compliance workflows that traditionally require expensive tools like Vanta or Drata.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15, React 19, Tailwind CSS, shadcn/ui |
| Backend API | FastAPI, Python 3.12, SQLAlchemy 2.0 (async) |
| Database | PostgreSQL 16 + pgvector |
| Auth | Keycloak 26 (OIDC/PKCE) |
| Cache | Redis 7 |
| Object Storage | MinIO |
| AI Agent | LangGraph + LiteLLM |
| Reverse Proxy | Traefik v3 |
| Containerization | Docker Compose |

## Architecture Diagram

```
Browser ─── Next.js (3000) ─── FastAPI (8000) ─── PostgreSQL (5432)
                │                    │                    │
                │                    ├──── Redis (6379)   │
                │                    ├──── MinIO (9000)   │
                │                    └──── LangGraph      │
                │                           (AI Agent)    │
                └──── Keycloak (8080) ────────────────────┘
```

## Data Flow

### Controls Generation Agent Pipeline

```
START
  → load_framework_requirements (DB query)
  → match_templates_to_requirements (DB + scoring)
  → customize_controls (LLM: tailor to company context)
  → deduplicate_controls (pure logic)
  → suggest_owners (LLM: map to departments)
  → finalize_output (write to DB as draft)
END
```

### Key Design Decisions

1. **Async-first**: All DB access uses SQLAlchemy async sessions + asyncpg
2. **Agent background execution**: Agents run as `asyncio.create_task()` — simple for dev, can be upgraded to Celery for production
3. **LLM fallback**: Agent nodes gracefully degrade to template substitution if no LLM API key is configured
4. **PKCE auth**: Frontend uses Keycloak's PKCE flow (no client secret in browser)
5. **Org-scoped data**: Controls, evidence, and agent runs are scoped to organizations via `org_id` foreign keys

## Database Schema

15 core tables:

- `organizations` — multi-tenant root
- `users` — linked to Keycloak identities
- `frameworks` → `framework_domains` → `framework_requirements` → `control_objectives`
- `control_templates` → `control_template_framework_mappings`
- `evidence_templates` → `control_template_evidence_templates` (junction)
- `controls` → `control_framework_mappings`
- `evidence` — linked to controls
- `agent_runs` — tracks AI agent execution
- `audit_logs` — append-only audit trail

## Directory Structure

```
backend/
  app/
    api/v1/      — FastAPI routers
    core/        — Database, auth, dependencies
    models/      — SQLAlchemy models
    schemas/     — Pydantic schemas
    services/    — Business logic
    agents/      — LangGraph agent definitions
  seeds/         — Seed data scripts
  tests/         — Pytest suite

frontend/
  src/
    app/         — Next.js App Router pages
    components/  — UI components
    hooks/       — React Query hooks
    lib/         — API client, auth, types
    providers/   — Context providers
```
