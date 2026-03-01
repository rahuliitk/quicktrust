# QuickTrust - Test Plan

## Overview

This document details every feature area that needs to be tested for the QuickTrust GRC platform, covering backend API endpoints, frontend UI, AI agents, integrations, and cross-cutting concerns.

---

## 1. Authentication & Authorization

### 1.1 Keycloak OIDC Login
- [ ] User can log in via Keycloak OIDC/PKCE flow
- [ ] Callback handler correctly exchanges code for tokens
- [ ] JWT token includes correct claims (sub, email, roles)
- [ ] Token auto-refresh every 60 seconds works
- [ ] Expired/invalid tokens return 401
- [ ] Logout clears session and redirects to login

### 1.2 Role-Based Access Control (RBAC)
- [ ] `super_admin` can access all endpoints across all orgs
- [ ] `admin` can access all endpoints within their org
- [ ] `compliance_manager` can manage frameworks, controls, policies, risks, audits
- [ ] `control_owner` can only manage assigned controls and their evidence
- [ ] `employee` can only view training assignments and complete them
- [ ] `executive` has read-only access to dashboards and reports
- [ ] `auditor_internal` can view all compliance data within org
- [ ] `auditor_external` can only access auditor portal with valid token
- [ ] Unauthenticated requests return 401
- [ ] Unauthorized role access returns 403
- [ ] RoleChecker dependency correctly enforces role requirements

### 1.3 Multi-Tenancy Isolation
- [ ] User from Org A cannot access Org B's data via API
- [ ] `verify_org_access()` blocks cross-org URL manipulation
- [ ] All query results are scoped to `org_id`
- [ ] Bulk operations (e.g., bulk approve controls) respect org boundaries
- [ ] Tenant provisioning creates org + admin user correctly

---

## 2. Organization Management

### 2.1 CRUD Operations
- [ ] `POST /api/v1/organizations` creates an organization with slug
- [ ] `GET /api/v1/organizations/{org_id}` returns org details
- [ ] `PATCH /api/v1/organizations/{org_id}` updates org settings
- [ ] Slug uniqueness is enforced
- [ ] JSON fields (cloud_providers, tech_stack, settings) serialize/deserialize correctly

---

## 3. User Management

### 3.1 CRUD Operations
- [ ] `POST /api/v1/organizations/{org_id}/users` creates a user linked to Keycloak
- [ ] `GET /api/v1/organizations/{org_id}/users` lists users for org
- [ ] `GET /api/v1/organizations/{org_id}/users/{id}` returns user details
- [ ] `PATCH /api/v1/organizations/{org_id}/users/{id}` updates user role/department
- [ ] `DELETE /api/v1/organizations/{org_id}/users/{id}` deactivates user
- [ ] Email uniqueness is enforced
- [ ] Keycloak ID uniqueness is enforced

---

## 4. Compliance Frameworks

### 4.1 Framework CRUD
- [ ] List all active frameworks
- [ ] Get framework details with nested domains and requirements
- [ ] Create custom framework with name, version, category
- [ ] Update framework details
- [ ] Deactivate framework (soft delete via `is_active`)

### 4.2 Framework Domains
- [ ] CRUD for domains within a framework
- [ ] Sort order is maintained
- [ ] Domain codes are unique within framework

### 4.3 Framework Requirements
- [ ] CRUD for requirements within a domain
- [ ] Requirements load with their parent domain
- [ ] Sort order is maintained

---

## 5. Controls

### 5.1 Control CRUD
- [ ] `POST` creates a control with title, description, owner
- [ ] `GET` list supports filtering by status, owner, framework
- [ ] `GET` detail includes framework mappings and evidence
- [ ] `PATCH` updates control status, effectiveness, implementation details
- [ ] `DELETE` removes control and cascades to mappings

### 5.2 Control Status Lifecycle
- [ ] Status transitions: `draft` -> `not_implemented` -> `in_progress` -> `implemented`
- [ ] Effectiveness can be set once status is `implemented`: `effective`, `partially_effective`, `not_effective`
- [ ] Automation level tracks as: `manual`, `semi_automated`, `automated`

### 5.3 Control Statistics
- [ ] `/stats` endpoint returns correct counts by status
- [ ] Compliance percentage calculation is accurate
- [ ] Stats respect org_id scope

### 5.4 Bulk Operations
- [ ] Bulk approve controls changes status correctly
- [ ] Bulk operations are transactional (all-or-nothing)

### 5.5 Control-Framework Mappings
- [ ] Controls can be mapped to framework requirements
- [ ] A control can map to multiple requirements
- [ ] Mappings are returned in control detail response

---

## 6. Evidence Management

### 6.1 Evidence CRUD
- [ ] Create evidence linked to a control
- [ ] List evidence filtered by control, status
- [ ] Update evidence status: `pending` -> `collected` -> `stale`
- [ ] Evidence `data` field stores JSON correctly

### 6.2 File Upload
- [ ] Upload file via multipart form data
- [ ] SHA-256 hash is computed and stored
- [ ] File stored in MinIO and URL returned
- [ ] File download via `file_url` works

### 6.3 Evidence Staleness
- [ ] Evidence older than threshold is flagged as `stale`
- [ ] Monitoring rule correctly identifies stale evidence
- [ ] Alerts fire for stale evidence

### 6.4 Automated Evidence Collection
- [ ] Trigger collection via integration endpoint
- [ ] Collection job status updates: `pending` -> `running` -> `completed`/`failed`
- [ ] Result data is stored in collection job
- [ ] Evidence record is created from collection result
- [ ] Failed collections store error message

---

## 7. Policy Management

### 7.1 Policy CRUD
- [ ] Create policy with title, content, owner
- [ ] List policies with status filter
- [ ] Get policy detail with linked frameworks and controls
- [ ] Update policy content, version

### 7.2 Policy Approval Workflow
- [ ] `draft` -> `pending_review`: Submit for approval
- [ ] `pending_review` -> `approved`: Admin approves, records `approved_by_id` and `approved_at`
- [ ] `pending_review` -> `draft`: Rejection returns to draft
- [ ] `approved` -> `published`: Publish sets `published_at`
- [ ] `published` -> `archived`: Archive end-of-life policies
- [ ] Only authorized roles can approve policies

### 7.3 Policy Review Tracking
- [ ] `next_review_date` is set on publish
- [ ] Monitoring rule fires when review date approaches/passes
- [ ] Notification sent for upcoming review

---

## 8. Risk Management

### 8.1 Risk CRUD
- [ ] Create risk with title, category, likelihood, impact
- [ ] Risk score is auto-calculated as `likelihood * impact`
- [ ] Risk level is derived: low (1-4), medium (5-9), high (10-15), critical (16-25)
- [ ] Update risk details, scoring, treatment plan

### 8.2 Risk Matrix
- [ ] `/matrix` endpoint returns 5x5 risk distribution
- [ ] Risks are correctly plotted by likelihood and impact
- [ ] Filtering by category works

### 8.3 Treatment Plans
- [ ] Treatment types: `mitigate`, `transfer`, `accept`, `avoid`
- [ ] Treatment status: `not_started` -> `in_progress` -> `completed`
- [ ] Treatment due date tracking

### 8.4 Residual Risk
- [ ] Residual likelihood/impact/score can be set post-treatment
- [ ] Residual values are independent of inherent values

### 8.5 Risk-Control Mappings
- [ ] Map risks to controls
- [ ] Multiple controls can mitigate one risk
- [ ] Risk detail includes linked controls

---

## 9. Incident Management

### 9.1 Incident CRUD
- [ ] Create incident with title, severity (P1-P4), category
- [ ] List incidents with status/severity filtering
- [ ] Update incident status, assigned_to, severity
- [ ] Incident detail includes timeline events

### 9.2 Incident Status Workflow
- [ ] `open` -> `investigating` -> `resolved` -> `closed`
- [ ] `resolved_at` timestamp set on resolution
- [ ] Post-mortem notes added before closing

### 9.3 Timeline Events
- [ ] Add timeline events: `status_change`, `note`, `assignment`
- [ ] Events include actor, timestamp, description
- [ ] Timeline displayed in chronological order

### 9.4 Related Controls
- [ ] Incidents can link to related control IDs
- [ ] Cross-reference visible in both incident and control views

---

## 10. Audit Management

### 10.1 Audit CRUD
- [ ] Create audit with title, type (internal/external), framework, dates
- [ ] List audits with status filter
- [ ] Update audit details, status, readiness score

### 10.2 Audit Status Workflow
- [ ] `planning` -> `fieldwork` -> `review` -> `completed` -> `closed`

### 10.3 Audit Findings
- [ ] Create finding linked to audit
- [ ] Finding severity levels work correctly
- [ ] Finding status: `open` -> `remediation_in_progress` -> `closed`
- [ ] Remediation plan and due date tracking

### 10.4 Audit Readiness Score
- [ ] Calculation: Controls (40%) + Evidence (30%) + Policies (20%) + Risks (10%)
- [ ] Score updates reflect current data state

### 10.5 Auditor Portal (External)
- [ ] Generate time-limited access token for an audit
- [ ] Token grants read-only access to audit's controls, evidence, policies
- [ ] Token validated via `X-Auditor-Token` header
- [ ] Expired tokens return 401
- [ ] External auditor cannot modify any data
- [ ] Portal UI displays correct data scope

---

## 11. Vendor Risk Management

### 11.1 Vendor CRUD
- [ ] Create vendor with name, category, risk_tier, contact info
- [ ] List vendors with status/risk_tier filter
- [ ] Update vendor details and contract dates
- [ ] Vendor status: `active`, `under_review`, `terminated`

### 11.2 Vendor Assessments
- [ ] Create assessment for a vendor with score and questionnaire data
- [ ] Assessment updates vendor's `assessment_score` and `risk_tier`
- [ ] Assessment history maintained per vendor

### 11.3 Contract Tracking
- [ ] Contract start/end dates tracked
- [ ] `next_assessment_date` triggers reminder notifications

---

## 12. Training & Awareness

### 12.1 Training Courses
- [ ] CRUD for training courses
- [ ] Course types: `video`, `document`, `quiz`
- [ ] `required_roles` field correctly scopes assignments
- [ ] `is_required` flag marks mandatory courses

### 12.2 Training Assignments
- [ ] Assign course to user with due date
- [ ] Assignment status: `assigned` -> `in_progress` -> `completed` / `overdue`
- [ ] Completion records score and `completed_at`
- [ ] Overdue detection based on `due_date`
- [ ] Attempts counter increments

### 12.3 Training Reports
- [ ] Completion rate per course
- [ ] Overdue assignments per user
- [ ] Training completion report generation

---

## 13. Access Reviews

### 13.1 Campaign Management
- [ ] Create access review campaign with title, reviewer, due_date
- [ ] Campaign status: `draft` -> `active` -> `completed` / `cancelled`
- [ ] List campaigns with status filter

### 13.2 Review Entries
- [ ] Add entries: user_name, system, resource, current_access
- [ ] Entry decisions: `approved`, `revoked`, `modified`
- [ ] Decision records `decided_by_id` and `decided_at`
- [ ] Undecided entries are flagged

### 13.3 Campaign Completion
- [ ] Campaign auto-completes when all entries have decisions
- [ ] `completed_at` timestamp set

---

## 14. Monitoring & Alerting

### 14.1 Monitor Rules
- [ ] CRUD for monitoring rules
- [ ] Check types: `evidence_staleness`, `control_status`, `policy_expiry`, `manual`
- [ ] Schedule options: `hourly`, `daily`, `weekly`
- [ ] Rule activation/deactivation via `is_active`

### 14.2 Rule Execution
- [ ] Rules execute on schedule via APScheduler
- [ ] `evidence_staleness` checks evidence age against threshold
- [ ] `control_status` detects controls stuck in draft/not_implemented
- [ ] `policy_expiry` detects policies past review date
- [ ] `last_checked_at` and `last_result` update after execution

### 14.3 Monitor Alerts
- [ ] Alerts created when rule check fails
- [ ] Alert severity: `critical`, `high`, `medium`, `low`
- [ ] Alert status: `open` -> `acknowledged` -> `resolved`
- [ ] Acknowledge records user and timestamp
- [ ] Resolved alerts record `resolved_at`

---

## 15. Integrations & Evidence Collectors

### 15.1 Integration Management
- [ ] CRUD for integrations (AWS, GitHub, Okta, Prowler)
- [ ] Integration status: `connected`, `disconnected`, `error`
- [ ] Config JSON stores provider-specific settings
- [ ] Credentials stored securely (reference only in DB)

### 15.2 AWS Collectors
- [ ] `aws_iam_mfa`: Returns IAM MFA enrollment report
- [ ] `aws_cloudtrail`: Returns CloudTrail status
- [ ] `aws_encryption_check`: Returns encryption at rest status
- [ ] Mock fallback works when credentials unavailable

### 15.3 GitHub Collectors
- [ ] `github_branch_protection`: Returns branch protection status
- [ ] `github_dependabot`: Returns Dependabot alert summary
- [ ] Mock fallback works when token unavailable

### 15.4 Okta Collectors
- [ ] `okta_mfa_enrollment`: Returns MFA enrollment report
- [ ] Mock fallback works when API key unavailable

### 15.5 Prowler Collectors
- [ ] `prowler_full_scan`: Full AWS security scan
- [ ] `prowler_service_scan`: Service-specific scan
- [ ] `prowler_compliance_scan`: Compliance framework scan
- [ ] Results include findings with severity and status
- [ ] Mock fallback for testing

### 15.6 Collection Job Tracking
- [ ] Job status transitions: `pending` -> `running` -> `completed`/`failed`
- [ ] `result_data` stored on completion
- [ ] `error_message` stored on failure
- [ ] Evidence record created from successful collection

---

## 16. AI Agents

### 16.1 Controls Generation Agent
- [ ] Loads framework requirements for selected frameworks
- [ ] Matches requirements to control templates
- [ ] LLM customizes control descriptions (or fallback to template substitution)
- [ ] Deduplication removes similar controls
- [ ] Owner suggestion assigns controls to users
- [ ] Created controls stored in DB with `agent_run_id`
- [ ] Agent run status tracked: `pending` -> `running` -> `completed`/`failed`

### 16.2 Policy Generation Agent
- [ ] Identifies required policies from framework domains
- [ ] Matches to policy templates
- [ ] LLM generates policy content with org context
- [ ] Created policies stored in DB

### 16.3 Evidence Generation Agent
- [ ] Loads controls for org
- [ ] Matches to evidence templates
- [ ] Generates placeholder evidence data (deterministic)
- [ ] Created evidence stored in DB

### 16.4 Risk Assessment Agent
- [ ] Evaluates org risks using LLM with company context
- [ ] Suggests risk scores and treatment plans
- [ ] Output stored in agent run

### 16.5 Vendor Risk Assessment Agent
- [ ] Processes vendor questionnaire data
- [ ] Assigns risk tier based on assessment
- [ ] Output stored in agent run

### 16.6 Remediation Agent
- [ ] Suggests remediation for failed controls
- [ ] Maps to evidence collection activities

### 16.7 Audit Preparation Agent
- [ ] Prepares evidence packages for auditor review
- [ ] Generates readiness reports

### 16.8 Pentest Orchestrator Agent
- [ ] Coordinates security testing workflows
- [ ] Integrates with external tools

### 16.9 Agent Run Tracking
- [ ] `input_data` and `output_data` recorded
- [ ] `tokens_used` tracked
- [ ] `error_message` captured on failure
- [ ] Duration tracked via `started_at` / `completed_at`

---

## 17. Security Questionnaires

### 17.1 Questionnaire CRUD
- [ ] Create questionnaire with title, source, questions JSON
- [ ] List questionnaires with status filter
- [ ] Status: `draft` -> `in_progress` -> `completed` -> `submitted`
- [ ] `total_questions` and `answered_count` maintained

### 17.2 Auto-Fill (Two-Pass)
- [ ] Pass 1: Keyword matching finds relevant controls/policies
- [ ] Pass 2: LLM refinement generates accurate answers
- [ ] Confidence scores returned per answer
- [ ] Source type tracked: `control`, `policy`, `manual`
- [ ] Source ID links to the originating entity

### 17.3 Response Approval
- [ ] Responses flagged for review
- [ ] Approval sets `is_approved` and `approved_by_id`
- [ ] Only authorized users can approve responses

---

## 18. Trust Center

### 18.1 Admin Configuration
- [ ] Create/update trust center config: slug, headline, description, branding
- [ ] Slug uniqueness enforced
- [ ] `is_published` toggle controls visibility

### 18.2 Document Management
- [ ] CRUD for trust center documents
- [ ] Document types: `policy`, `certification`, `soc2`, `pentest`, `report`
- [ ] `is_public` controls visibility without NDA
- [ ] `requires_nda` flag for restricted documents
- [ ] Sort order maintained

### 18.3 Public Endpoint
- [ ] `GET /api/v1/trust/{slug}` returns published trust center
- [ ] No authentication required for public endpoint
- [ ] Only published config is accessible
- [ ] Only public documents returned (NDA documents excluded from response)

---

## 19. Reports

### 19.1 Report Generation
- [ ] `compliance_summary`: Control + risk + policy + evidence stats
- [ ] `risk_report`: Risk register data
- [ ] `evidence_audit`: Evidence collection status
- [ ] `training_completion`: Course completion rates

### 19.2 Report Formats
- [ ] PDF generation via ReportLab
- [ ] CSV export with correct headers and data
- [ ] JSON format for programmatic access

### 19.3 Report Lifecycle
- [ ] Status: `pending` -> `generating` -> `completed` / `failed`
- [ ] File stored in MinIO on completion
- [ ] `file_url` returned for download
- [ ] Error message captured on failure

---

## 20. Notifications

### 20.1 In-App Notifications
- [ ] Notifications created for relevant events
- [ ] List notifications for current user
- [ ] Mark individual notification as read
- [ ] Mark all notifications as read
- [ ] Unread count returned correctly

### 20.2 Notification Categories
- [ ] `policy_expiry`: Triggered when policy review is due
- [ ] `evidence_stale`: Triggered when evidence ages out
- [ ] `incident`: Triggered on incident assignment
- [ ] `monitoring_alert`: Triggered by monitor rule failure
- [ ] `access_review`: Triggered for pending review decisions
- [ ] `training`: Triggered for overdue training

### 20.3 Email Notifications
- [ ] SMTP integration sends emails correctly
- [ ] Email template formatting correct
- [ ] Fallback when SMTP not configured

### 20.4 Slack Notifications
- [ ] Webhook integration sends Slack messages
- [ ] Correct formatting for Slack blocks
- [ ] Category filtering per webhook config

### 20.5 Notification Preferences
- [ ] User can configure per-category/per-channel preferences
- [ ] Disabled categories don't generate notifications

---

## 21. Audit Logging

### 21.1 Audit Trail
- [ ] All CRUD operations logged with actor, action, entity type/id
- [ ] Changes stored as JSON diff (old/new values)
- [ ] IP address captured from request
- [ ] Timestamps accurate
- [ ] Append-only: no updates or deletes to audit_logs table

### 21.2 Query Interface
- [ ] Filter by org_id, actor, action, entity_type, date range
- [ ] Pagination works correctly
- [ ] Results ordered by timestamp descending

---

## 22. Gap Analysis

### 22.1 Per-Framework Analysis
- [ ] Returns coverage percentage for each framework domain
- [ ] Shows requirements mapped vs unmapped to controls
- [ ] Identifies controls not mapped to any requirement

### 22.2 Cross-Framework Matrix
- [ ] Shows overlap between frameworks
- [ ] Highlights shared controls across frameworks
- [ ] Identifies unique requirements per framework

---

## 23. Prowler Integration

### 23.1 Scan Management
- [ ] Trigger full AWS security scan
- [ ] Trigger service-specific scan
- [ ] Trigger compliance framework scan (CIS, SOC 2, PCI, HIPAA)
- [ ] Scan results stored with severity and resource details

### 23.2 Compliance Posture
- [ ] Aggregate pass/fail rate by compliance framework
- [ ] Service-level breakdown of findings
- [ ] Severity distribution (critical, high, medium, low)

### 23.3 Evidence Linking
- [ ] Scan results auto-linked to relevant controls
- [ ] Evidence records created from scan findings

---

## 24. Semantic Search (Embeddings)

### 24.1 Embedding Generation
- [ ] Embeddings generated for controls, policies, evidence descriptions
- [ ] Model: all-MiniLM-L6-v2 (384-dimensional vectors)
- [ ] Vectors stored correctly (JSON or pgvector)

### 24.2 Similarity Search
- [ ] Search returns semantically similar entities
- [ ] Results ranked by cosine similarity
- [ ] Cross-entity search works (find policies related to a control)

---

## 25. Onboarding Wizard

### 25.1 Step Progression
- [ ] Step 1: Org setup (name, industry, size, cloud providers)
- [ ] Step 2: Framework selection (multi-select)
- [ ] Step 3: AI agent generation (controls, policies, evidence)
- [ ] Step 4: Review and dashboard redirect

### 25.2 Session Tracking
- [ ] Onboarding session created on start
- [ ] `current_step` and `steps_completed` updated correctly
- [ ] `metadata` stores selections and generation results
- [ ] Status: `pending` -> `in_progress` -> `completed`

---

## 26. Auditor Marketplace

### 26.1 Auditor Profiles
- [ ] Register auditor profile with certifications, specialties
- [ ] Verification workflow for auditor credentials
- [ ] Search auditors by specialty, certification, location

### 26.2 Auditor Matching
- [ ] Filter by framework expertise
- [ ] Filter by industry experience
- [ ] Contact/request flow

---

## 27. Frontend UI Testing

### 27.1 Layout & Navigation
- [ ] Sidebar renders with correct menu items per role
- [ ] Top bar shows user info and notifications
- [ ] Responsive design works on mobile/tablet
- [ ] Dark/light mode (if applicable)

### 27.2 Dashboard
- [ ] Compliance score widget shows correct percentage
- [ ] Control status breakdown chart renders
- [ ] Recent incidents list populates
- [ ] Quick action buttons navigate correctly
- [ ] Risk overview widget shows risk level distribution

### 27.3 Data Tables
- [ ] TanStack Table renders data correctly
- [ ] Pagination controls work
- [ ] Sorting by columns works
- [ ] Filtering/search works
- [ ] Empty state renders when no data

### 27.4 Forms
- [ ] Create/edit forms validate required fields
- [ ] Error messages display correctly
- [ ] Form submission triggers API call
- [ ] Success/error toast notifications display

### 27.5 Charts & Visualizations
- [ ] Risk matrix heatmap renders correctly
- [ ] Compliance trend line chart renders
- [ ] Training completion bar chart renders
- [ ] Prowler findings pie chart renders

---

## 28. API Edge Cases & Error Handling

### 28.1 Input Validation
- [ ] Required fields return 422 when missing
- [ ] Invalid UUID formats rejected
- [ ] String length limits enforced
- [ ] Enum values validated (status, severity, role)

### 28.2 Error Responses
- [ ] 400: Bad request with descriptive message
- [ ] 401: Unauthorized (no/invalid token)
- [ ] 403: Forbidden (insufficient role)
- [ ] 404: Not found for missing resources
- [ ] 422: Validation error with field details
- [ ] 500: Internal server error with safe message

### 28.3 Concurrency
- [ ] Concurrent updates to same resource don't corrupt data
- [ ] `updated_at` optimistic locking works (if implemented)

### 28.4 Pagination
- [ ] Default page size applied
- [ ] Custom page size respected
- [ ] Total count returned
- [ ] Out-of-range page returns empty list (not error)

---

## 29. Infrastructure & DevOps

### 29.1 Docker Compose
- [ ] All services start successfully: PostgreSQL, Redis, MinIO, Keycloak, FastAPI, Next.js, Traefik
- [ ] Services can communicate with each other
- [ ] Volume persistence works across restarts
- [ ] Health checks pass for all services

### 29.2 Database Migrations
- [ ] All Alembic migrations run without errors
- [ ] Upgrade from scratch creates correct schema
- [ ] Downgrade migrations work correctly

### 29.3 Redis Caching
- [ ] Cache hit returns cached data
- [ ] Cache miss queries database and populates cache
- [ ] Cache invalidation on data update
- [ ] Graceful degradation when Redis unavailable

### 29.4 MinIO Storage
- [ ] File upload to MinIO succeeds
- [ ] File download from MinIO succeeds
- [ ] File deletion from MinIO succeeds
- [ ] Bucket auto-creation on first use

---

## 30. Performance & Scalability

### 30.1 API Response Times
- [ ] List endpoints respond under 500ms for 100+ records
- [ ] Detail endpoints respond under 200ms
- [ ] Report generation completes within 30 seconds

### 30.2 Database Queries
- [ ] No N+1 queries in list endpoints
- [ ] Indexes exist for frequently filtered columns (org_id, status)
- [ ] Large result sets use pagination

### 30.3 Background Tasks
- [ ] Agent runs execute without blocking API responses
- [ ] Collection jobs run asynchronously
- [ ] Report generation is non-blocking

---

## Test Data Summary

The `samplesql.sql` file provides the following test data:

| Entity                  | Count | Notes                              |
|-------------------------|-------|------------------------------------|
| Organizations           | 3     | Acme Corp, HealthFirst, FinSecure  |
| Users                   | 10    | Across 3 orgs, 6 roles            |
| Frameworks              | 6     | SOC 2, ISO 27001, HIPAA, PCI, GDPR, NIST |
| Framework Domains       | 14    | Across SOC 2, ISO 27001, HIPAA    |
| Framework Requirements  | 13    | Across SOC 2, ISO 27001, HIPAA    |
| Controls                | 15    | 12 Acme + 3 HealthFirst           |
| Evidence                | 11    | Various statuses and collectors    |
| Policies                | 7     | All lifecycle statuses             |
| Risks                   | 7     | All risk levels and treatment types|
| Incidents               | 4     | All severity levels and statuses   |
| Timeline Events         | 7     | For incident tracking              |
| Audits                  | 3     | Various statuses                   |
| Audit Findings          | 3     | Various severities                 |
| Vendors                 | 6     | Various risk tiers and statuses    |
| Vendor Assessments      | 2     | With questionnaire data            |
| Training Courses        | 4     | Various course types               |
| Training Assignments    | 6     | All assignment statuses            |
| Access Review Campaigns | 2     | Active and completed               |
| Access Review Entries   | 5     | Various decisions                  |
| Monitor Rules           | 4     | All check types                    |
| Monitor Alerts          | 3     | All alert statuses                 |
| Integrations            | 5     | AWS, GitHub, Okta, Prowler         |
| Collection Jobs         | 5     | Completed and failed               |
| Questionnaires          | 3     | Various statuses                   |
| Questionnaire Responses | 3     | With confidence scores             |
| Trust Center Config     | 1     | Published                          |
| Trust Center Documents  | 3     | Public and NDA-required            |
| Reports                 | 4     | Various types and formats          |
| Notifications           | 5     | Various categories                 |
| Audit Logs              | 8     | Various actions                    |
| Onboarding Sessions     | 3     | Various completion states          |
| Agent Runs              | 5     | Various agent types and statuses   |

---

## Existing Test Files

The repository has pytest test files in `backend/tests/` covering:

| Test File                          | Coverage Area                    |
|------------------------------------|----------------------------------|
| `test_health.py`                   | Health check endpoint            |
| `test_frameworks.py`               | Framework CRUD API               |
| `test_controls.py`                 | Controls CRUD API                |
| `test_control_templates.py`        | Control template management      |
| `test_organizations.py`            | Organization CRUD API            |
| `test_risks.py`                    | Risk management API              |
| `test_training.py`                 | Training courses & assignments   |
| `test_access_reviews.py`           | Access review campaigns          |
| `test_incidents.py`                | Incident management API          |
| `test_vendors.py`                  | Vendor management API            |
| `test_questionnaires.py`           | Questionnaire API                |
| `test_notifications.py`           | Notification system              |
| `test_gap_analysis.py`             | Gap analysis API                 |
| `test_auditor_marketplace.py`      | Auditor marketplace              |
| `test_audit_logs.py`               | Audit logging                    |
| `test_rbac.py`                     | RBAC enforcement                 |
| `test_tenants.py`                  | Multi-tenancy isolation          |
| `test_prowler.py`                  | Prowler integration              |
| `test_trust_center.py`             | Trust center                     |

### Running Tests
```bash
# Run all tests
cd backend && pytest

# Run with verbose output
cd backend && pytest -v

# Run specific test file
cd backend && pytest tests/test_controls.py

# Run with coverage report
cd backend && pytest --cov=app --cov-report=html
```
