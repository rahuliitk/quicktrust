# QuickTrust — Implemented Features

> **Version:** v0.3.0
> **Last Updated:** 2026-02-24
> **Tech Stack:** Next.js 15 + React 19 + Tailwind CSS v4 (Frontend) | FastAPI + SQLAlchemy 2.0 Async (Backend) | Keycloak 26 (Auth) | LangGraph + LiteLLM (AI Agents) | PostgreSQL / SQLite (Database)

---

## 1. Compliance Frameworks

- **6 frameworks fully seeded** with domains, requirements, and control objectives:
  - SOC 2 Type II (9 domains, 33 requirements)
  - ISO 27001:2022
  - HIPAA Security Rule
  - GDPR
  - PCI DSS v4.0
  - NIST CSF 2.0
- **REST API:** List frameworks, get framework detail, list domains, get domain detail, list requirements, get requirement detail
- **Frontend:** `/frameworks` list page with active/inactive badges; `/frameworks/[id]` detail page with domain drill-down

---

## 2. Controls Engine

- **Full CRUD API** with pagination, filtering by status/framework, stats, and bulk-approve operations
- **Control statuses:** draft, implemented, partially_implemented, not_implemented, not_applicable
- **Automation levels:** manual, partial, full
- **Framework mappings:** many-to-many relationship to framework requirements
- **Template library:** 25 base control templates + extended templates covering 8 domains (HR Security, phishing simulation, security champions, etc.)
- **Frontend:** `/controls` list page with status tabs/filters; `/controls/[id]` detail page with edit form, framework mapping display, evidence sub-list
- **Control Templates UI:** `/control-templates` page — browse templates with domain filter, pagination, detail view showing implementation guidance, test procedures, automation levels, and variables

---

## 3. Evidence Engine

- **CRUD API** with filtering by `control_id` and pagination
- **Evidence statuses:** collected, pending, expired, not_applicable
- **Collection methods:** manual, automated
- **20+ evidence templates** seeded (MFA reports, CloudTrail screenshots, access review logs, penetration test reports, etc.)
- **Frontend:** `/evidence` page — list with status filter, create form, upload metadata, links to source control

---

## 4. Policy Engine

- **Full CRUD API** with stats (draft, review, approved, published counts)
- **Policy lifecycle:** draft → review → approved → published
- **Policy template library:** Information Security Policy, Acceptable Use Policy, Access Control Policy, Data Classification, Incident Response Plan, and more
- **Policy Templates API:** `/api/v1/policy-templates/` — list (filterable by category), get by ID
- **Frontend:** `/policies` list page with status tabs, publish/approve workflow, rich content editor; `/policies/[id]` detail with content display and status change buttons

---

## 5. AI Agents

### Controls Generation Agent
- Multi-step LangGraph pipeline: load framework requirements → match templates → customize controls with LLM → deduplicate → suggest owners → finalize to DB
- Fallback: template substitution if no LLM API key (replaces `{cloud_provider}`, etc.)
- **Frontend:** `/agents/controls-generation` — framework selector, company context form, trigger button, live status polling with elapsed time counter, progress bar, generated controls review with bulk-approve checkboxes

### Policy Generation Agent
- Multi-step pipeline: identify required policies from controls → match policy templates → generate policy content with LLM → finalize to DB
- Keyword-domain mapping for policy category identification
- **Frontend:** `/agents/policy-generation` — similar UI pattern with framework selector, context, trigger, status poll, and generated policy review

### Evidence Generation Agent
- Pipeline: load controls → match evidence templates → generate evidence data → finalize to DB
- Uses deterministic placeholder data (no LLM, by design for speed)
- Creates evidence records linked to controls
- Triggered via onboarding pipeline only (no standalone UI)

### Agent Run Tracking
- All agent runs stored in `agent_runs` table with status, started_at, completed_at, input_data, output_data, error_message

---

## 6. Onboarding Wizard

- **4-step wizard** at `/onboarding`:
  - Step 1: Company Info (name, industry, size)
  - Step 2: Tech Stack (cloud providers, tech stack multi-select, departments)
  - Step 3: Frameworks (checkboxes, multi-framework selection)
  - Step 4: Review & Launch (summary, notes)
- **Backend pipeline:** 4 sequential background steps — update org, run controls generation, run policy generation, run evidence generation
- **Progress tracking:** `/onboarding/progress` polls status and shows step completion

---

## 7. Risk Register

- **Full CRUD API** with stats, risk matrix, and control mapping
- **Risk scoring:** 5x5 likelihood × impact matrix with computed risk levels (critical/high/medium/low)
- **Risk lifecycle:** identified → assessing → treated → accepted → closed
- **Treatment management:** treatment_plan, treatment_type, treatment_status, treatment_due_date
- **Residual risk tracking:** residual_likelihood, residual_impact, residual_score
- **Frontend:** `/risks` list page with risk level badges; `/risks/[id]` detail with treatment plan and control mapping; `/risks/matrix` — visual 5×5 heat map

---

## 8. Incident Management

- **Full CRUD API** with stats, timeline events, and automatic timeline creation on status change
- **Severity levels:** P1, P2, P3, P4
- **Incident lifecycle:** open → investigating → resolved → closed
- **Timeline events:** status_change, note, assignment
- **Post-mortem notes** support
- **Frontend:** `/incidents` list with severity badges and filters; `/incidents/[id]` detail with status workflow, post-mortem section, timeline feed with add-note form

---

## 9. Vendor Risk Management

- **Full CRUD API** with stats and vendor assessments
- **Risk tiers:** critical, high, medium, low
- **Vendor lifecycle:** active, under_review, terminated
- **Assessment tracking:** score, risk_tier_assigned, notes, questionnaire_data
- **Frontend:** `/vendors` list with risk tier badges; `/vendors/[id]` detail with contract info, assessment history, and add assessment form

---

## 10. Training & Awareness

- **CRUD API** for courses and assignments with stats
- **Course types:** security_awareness, compliance, role_specific
- **Assignment lifecycle:** pending → in_progress → completed → overdue
- **Tracking:** completion rates, scores, mandatory course flagging
- **Frontend:** `/training` list with course cards and stats; `/training/[id]` detail with assignments list and completion management

---

## 11. Access Reviews

- **CRUD API** for campaigns and entries with stats
- **Campaign types:** quarterly, annual, ad_hoc
- **Campaign lifecycle:** draft → active → completed → cancelled
- **Entry decisions:** pending → approved / revoked / skipped (with justification)
- **Frontend:** `/access-reviews` list with stats cards (pending, approved, revoked); `/access-reviews/[id]` detail with per-entry approve/revoke/skip buttons

---

## 12. Continuous Monitoring

- **Rules + alerts API** with stats and on-demand execution
- **Check types implemented:**
  - `evidence_staleness` — finds evidence older than configured threshold
  - `control_status` — finds controls in not_implemented/draft status
  - `policy_expiry` — finds policies past review date
  - `manual` — user-created rules for workflow
- **Alert management:** open → acknowledged → resolved
- **Frontend:** `/monitoring` list with stats and rule cards; `/monitoring/[id]` rule detail with alert history and acknowledge/resolve buttons

---

## 13. Security Questionnaire Automation

- **CRUD API** with auto-fill, stats, and per-response management
- **Auto-fill:** keyword matching against controls/policies with confidence scoring
- **Response tracking:** per-question answers with confidence, source linkage, and approval workflow
- **Frontend:** `/questionnaires` list with status filter and stats; `/questionnaires/[id]` detail with question-by-question answer form, auto-fill button, approve/reject per response

---

## 14. Trust Center

- **Admin API:** config management, document CRUD
- **Public endpoint:** `GET /api/v1/trust/{slug}` — serves published trust center page (no auth required)
- **Config:** slug, headline, description, certifications, contact email, publish toggle
- **Documents:** policy, certification, report, other — with public/NDA/private visibility and sort ordering
- **Frontend:** `/trust-center` admin page — config form, publish toggle, document management, public URL preview

---

## 15. Audit Management & Auditor Portal

### Audit Management
- **Full CRUD** + findings, access tokens, evidence package, and readiness score
- **Readiness score formula:** controls (40%) + evidence (30%) + policies (20%) + risks (10%)
- **Audit lifecycle:** planning → fieldwork → review → completed
- **Findings management:** title, severity, status, recommendation, management response, due date
- **Access tokens:** generate time-limited, revocable tokens for external auditors
- **Frontend:** `/audits` list with status badges; `/audits/[id]` detail — findings, token generation, readiness score, evidence package view

### Auditor Portal (External)
- **Separate read-only API** authenticated via `X-Auditor-Token` header
- **Portal endpoints:** overview, controls, evidence, policies (approved/published only), risks, evidence package
- **Frontend:** `/portal` (standalone, no sidebar) — token input form, tabbed view for Overview/Controls/Evidence/Policies/Risks

---

## 16. Integrations & Evidence Collection

- **CRUD API** + providers catalog, trigger collection, job tracking
- **6 collectors defined** (mock implementations):
  - AWS: IAM MFA report, CloudTrail status, Encryption at rest
  - GitHub: Branch protection, Dependabot alerts
  - Okta: MFA enrollment
- **Collection jobs:** status tracking (running/completed/failed), result data, evidence linking
- **Frontend:** `/integrations` list with provider catalog cards; `/integrations/[id]` detail — trigger collection by type, job history

---

## 17. Reports

- **CRUD API** with stats and report data generation
- **Report types with data aggregation:**
  - `compliance_summary` — control stats + risk stats + policy counts + evidence counts
  - `risk_report` — risk stats
  - `evidence_audit` — control stats + evidence counts
  - `training_completion` — assignment completion rates
- **Frontend:** `/reports` page with type/status filters, stats cards, create form, list with status badges

---

## 18. Settings & Organization Management

- **Organization CRUD API:** create, get, update
- **Frontend:** `/settings` page — edit organization name, industry, company size, cloud providers, tech stack
- **Comma-separated input → array conversion** for multi-value fields

---

## 19. Authentication (Keycloak OIDC/PKCE)

- **Frontend:** Keycloak OIDC/PKCE flow via `keycloak-js`, `check-sso` on load, S256 PKCE, token auto-refresh every 60 seconds
- **Auth context:** provides authenticated status, token, userInfo (name, email, roles, org_id)
- **Backend:** JWT RS256 verification against Keycloak JWKS endpoint, JWKS in-memory cache
- **Auth routes:** `/auth/token` (password grant for testing), `/auth/me`, `/auth/logout`
- **Login/callback pages:** `/login` and `/callback` for Keycloak redirect handling
- **Dev fallback:** Demo org ID when Keycloak is not configured

---

## 20. Dashboard

- **Compliance score** (computed from controls implementation percentage)
- **Framework count** with framework cards
- **Policy count** with status breakdown
- **Risk count** with risk level distribution
- **Agent runs** count and history
- **Quick action links** to key modules

---

## 21. Infrastructure & DevOps

- **Docker Compose** setup with all services (FastAPI, Next.js, PostgreSQL, Keycloak, MinIO, Redis, Traefik)
- **Traefik reverse proxy** configuration
- **Keycloak realm config** for OIDC
- **Alembic** database migrations
- **Database seeding** scripts for frameworks, templates, and demo data
- **Health check** endpoint at `/health`

---

## 22. Testing

- **Backend tests** implemented for:
  - Frameworks API
  - Controls API
  - Control Templates API
  - Organizations API
  - Health check endpoint
