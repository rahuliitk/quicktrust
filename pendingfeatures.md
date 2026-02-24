# QuickTrust — Pending / Incomplete Features

> **Version:** v0.3.0
> **Last Updated:** 2026-02-24

---

## High Priority

### 1. Role-Based Access Control (RBAC) — Not Enforced

- **Status:** Defined but not wired
- **Details:** The `require_role()` decorator exists in `core/dependencies.py` and user `role` field is stored in the DB, but `require_role` is **not applied to any API route**. Every authenticated endpoint accepts any valid JWT regardless of role.
- **Planned roles:** Super Admin, Compliance Manager, Control Owner, Employee, Executive, Auditor (Internal/External), API/Service Account
- **Impact:** Any authenticated user can access all data and perform all actions

### 2. Role-Based UI Segregation

- **Status:** Not implemented
- **Details:** The sidebar shows all 22 nav items to every authenticated user. No role-gated routing exists.
- **Expected behavior:**
  - Control Owners should only see their assigned controls
  - Employees should only see training and access reviews
  - Executives should see read-only dashboards
  - Auditors should be restricted to the portal

### 3. Real Integration Connectors (Currently Mock Only)

- **Status:** Stubbed with hardcoded data
- **Details:** All 6 collectors (AWS IAM MFA, CloudTrail, Encryption; GitHub Branch Protection, Dependabot; Okta MFA) return hardcoded synthetic data. Integration credentials are stored but never used for real API calls.
- **Required work:**
  - AWS SDK (boto3) integration for real IAM/CloudTrail/KMS data
  - GitHub API integration for real repo scanning
  - Okta SDK integration for real MFA enrollment data
  - Error handling, rate limiting, credential validation

---

## Medium Priority

### 4. AI Agents (Agents 4–8 from Requirements Spec)

The following agents are planned but **not implemented**:

| Agent | Description |
|---|---|
| **Agent 04: Risk Assessment Agent** | Automated risk identification from scan results, vulnerability feeds, and configuration drift |
| **Agent 05: Remediation Agent** | Auto-remediation with PR generation, IaC patching, and rollback capabilities |
| **Agent 06: Audit Preparation Agent** | Automated workpapers, evidence gap analysis, narrative generation |
| **Agent 07: Vendor Risk Assessment Agent** | SOC 2 report parsing, automated vendor scoring, contract analysis |
| **Agent 08: Penetration Testing Orchestrator** | Full open-source pen test tool orchestration (Nmap, OWASP ZAP, etc.) |
| **Agent 10: Continuous Monitoring Agent (Daemon)** | Real-time drift detection, CloudTrail event stream processing |

### 5. Report File Generation (PDF/CSV)

- **Status:** Only JSON data payload generated
- **Details:** The Reports module accepts `format: "pdf" | "csv" | "json"` but only generates JSON. No PDF rendering library (WeasyPrint, reportlab) or CSV serialization is implemented. The `file_url` field in the model is never populated.
- **Required work:** PDF template rendering, CSV export, file storage to MinIO, download endpoints

### 6. Scheduled / Automated Monitoring

- **Status:** Manual trigger only
- **Details:** Monitoring rules have a `schedule` field (hourly/daily/weekly) but there is no scheduler (cron, Celery beat, APScheduler). Rules only execute when manually triggered via `POST /monitoring/rules/{rule_id}/run`.
- **Required work:** Background scheduler (APScheduler or Celery beat), automatic periodic rule execution, alert notification system

### 7. File Upload / Object Storage (MinIO)

- **Status:** Configured but not wired
- **Details:** MinIO is configured (URL, credentials, bucket name in `config.py`) and the MinIO SDK is a declared dependency, but MinIO client is **not instantiated or used anywhere**. No file upload endpoint exists. Evidence `data` is stored as JSON. `file_url` fields on Report and TrustCenterDocument are never populated.
- **Required work:** MinIO client initialization, file upload endpoints, evidence attachment support, report file storage

### 8. Evidence File Upload / Attachment

- **Status:** Not implemented
- **Details:** Evidence records store `data` as a JSON blob only. No multipart file upload endpoint for attaching screenshots, reports, or binary artifacts to evidence items.
- **Required work:** Upload API, file validation, storage integration (MinIO), evidence model `file_url` field

### 9. Additional Compliance Frameworks (9 Missing)

- **Status:** Not seeded
- **Implemented:** SOC 2, ISO 27001, HIPAA, GDPR, PCI DSS v4.0, NIST CSF 2.0 (6 frameworks)
- **Missing from requirements:**
  - ISO 27701
  - NIST 800-53 Rev 5
  - NIST 800-171 Rev 3
  - FedRAMP
  - CCPA/CPRA
  - SOX IT Controls
  - CIS Controls v8
  - CSA STAR/CCM
  - CMMC 2.0

### 10. Policy Approval Workflow (Formal)

- **Status:** Partially implemented
- **Details:** Policies have `status: draft → review → approved → published` and `approved_by_id` / `approved_at` fields, but the API only exposes a generic PATCH. No dedicated `/approve` or `/publish` endpoint enforcing role checks or setting approval timestamps automatically.
- **Required work:** Dedicated approval endpoints, role-based approval gates, audit trail for approvals

---

## Lower Priority

### 11. Redis Cache Integration

- **Status:** Configured but unused
- **Details:** Redis is configured (`REDIS_URL`) and the `redis` package is a dependency, but Redis is **not used anywhere**. No session storage, no pub/sub messaging, no cache layer.
- **Potential uses:** API response caching, session storage, rate limiting, real-time notifications

### 12. pgvector / Embeddings for Agent Memory

- **Status:** Not implemented
- **Details:** pgvector is mentioned in architecture docs as a planned component for agent memory. No vector columns exist in any model, no embedding generation, no similarity search.
- **Required work:** pgvector extension setup, embedding model integration, vector columns, similarity search for policy/control matching

### 13. Evidence Generation Agent — Standalone UI

- **Status:** Agent works, but no standalone trigger
- **Details:** The evidence generation agent runs as part of the onboarding pipeline but has no dedicated UI page under `/agents/` and no standalone API endpoint for independent triggering.
- **Required work:** `/agents/evidence-generation` page, standalone API endpoint

### 14. Questionnaire Auto-Fill — LLM-Powered

- **Status:** Keyword matching only
- **Details:** The `auto_fill` service uses basic keyword substring matching rather than LLM-powered semantic matching. Functional but lower quality than the full agent-based approach described in the requirements.
- **Required work:** LLM integration for semantic question-answer matching, confidence scoring, source citation

### 15. Custom Framework Builder

- **Status:** Not implemented
- **Details:** Requirements describe a custom framework creation UI (define custom domains, requirements, control objectives). The framework model supports this, but **no POST/PATCH endpoints exist** — the framework API is read-only. Frameworks can only be added via seed scripts.
- **Required work:** Framework CRUD API, UI for creating/editing frameworks, domain/requirement management

### 16. Auditor Registration / Marketplace

- **Status:** Not implemented
- **Details:** Requirements describe auditor registration and marketplace (credentials, CPA/CISA verification, public profiles, auditor discovery). Only the internal auditor portal (token-based read access) is built.
- **Required work:** Auditor user registration, credential verification workflow, public profiles, marketplace search/discovery

### 17. Cross-Framework Control Mapping & Gap Analysis

- **Status:** Partially implemented
- **Details:** `ControlFrameworkMapping` model supports multi-framework mapping and the controls generation agent handles `requirement_codes` across frameworks. However, there is no dedicated cross-framework deduplication report, gap analysis UI, or framework version diff/migration tooling.
- **Required work:** Gap analysis dashboard, cross-framework mapping matrix UI, framework version migration tool

### 18. Dashboard — Missing Metrics

- **Status:** Partially complete
- **Details:** Dashboard shows compliance score, framework count, policy count, risk count, and agent runs. Missing:
  - Incident count / open incidents
  - Vendor risk summary
  - Training completion rate
  - Open monitoring alerts count
  - Access review pending count
- These modules have stats APIs but are not surfaced on the main dashboard.

### 19. Test Coverage — Major Gaps

- **Status:** Minimal test coverage
- **Tests exist for:** Frameworks, Controls, Control Templates, Organizations, Health check
- **No tests for:**
  - Policies API
  - Risks API
  - Incidents API
  - Vendors API
  - Training API
  - Access Reviews API
  - Monitoring API
  - Questionnaires API
  - Trust Center API
  - Reports API
  - Integrations API
  - Onboarding API
  - Audit Portal API
  - AI Agent logic (controls gen, policy gen, evidence gen)

### 20. Notification System

- **Status:** Not implemented
- **Details:** No email, Slack, or in-app notification system exists. Events like policy expiry, evidence staleness, incident creation, access review assignments, and monitoring alerts do not trigger notifications.
- **Required work:** Notification service, email templates, Slack webhook integration, in-app notification center

### 21. Audit Logging / Activity Feed

- **Status:** Not implemented
- **Details:** No system-wide audit log tracking who changed what and when. Individual models have `created_at` / `updated_at` but there is no centralized activity/change log.
- **Required work:** Audit log model, middleware to capture changes, activity feed UI

### 22. Multi-Tenancy Hardening

- **Status:** Basic org scoping implemented
- **Details:** All data is scoped by `org_id`, but there is no org-level isolation testing, no cross-tenant access prevention verification, and no tenant provisioning workflow.
- **Required work:** Tenant isolation tests, org provisioning API, tenant admin management

---

## Summary

| Priority | Count | Categories |
|---|---|---|
| **High** | 3 | RBAC enforcement, UI segregation, real integrations |
| **Medium** | 7 | AI agents (5 missing), PDF/CSV reports, scheduled monitoring, file upload/MinIO, evidence attachments, additional frameworks, policy approval workflow |
| **Lower** | 11 | Redis, pgvector, evidence agent UI, LLM auto-fill, custom frameworks, auditor marketplace, cross-framework analysis, dashboard metrics, test coverage, notifications, audit logging, multi-tenancy |
| **Total** | **21** | |
