# OpenComply — Open-Source Agentic GRC Platform

## Requirements Specification v1.0

> **Mission**: Build an open-source, agent-first GRC platform that automates end-to-end compliance with minimal-to-zero client intervention. Replace $20k+/yr platforms (Vanta, Drata, Sprinto, Secureframe) with a transparent, community-driven alternative.

---

## Table of Contents

1. [Platform Overview](#1-platform-overview)
2. [User Personas & Roles](#2-user-personas--roles)
3. [Compliance Framework Engine](#3-compliance-framework-engine)
4. [AI Agent Architecture](#4-ai-agent-architecture)
5. [Controls Engine](#5-controls-engine)
6. [Policy Engine](#6-policy-engine)
7. [Evidence Engine](#7-evidence-engine)
8. [Cloud Security Monitoring (Open Source Stack)](#8-cloud-security-monitoring)
9. [Penetration Testing Agents](#9-penetration-testing-agents)
10. [Integration Hub (Open Source Connectors)](#10-integration-hub)
11. [Risk Management](#11-risk-management)
12. [Audit Management & Auditor Portal](#12-audit-management--auditor-portal)
13. [Continuous Monitoring & Alerting](#13-continuous-monitoring--alerting)
14. [Access Review Automation](#14-access-review-automation)
15. [Incident Management](#15-incident-management)
16. [Vendor Risk Management](#16-vendor-risk-management)
17. [Training & Awareness](#17-training--awareness)
18. [Security Questionnaire Automation](#18-security-questionnaire-automation)
19. [Trust Center](#19-trust-center)
20. [Reporting & Dashboards](#20-reporting--dashboards)
21. [SaaS Platform Features](#21-saas-platform-features)
22. [Technical Architecture](#22-technical-architecture)
23. [Open Source Tool Registry](#23-open-source-tool-registry)
24. [Data Model](#24-data-model)
25. [Deployment](#25-deployment)
26. [Roadmap & Phasing](#26-roadmap--phasing)

---

## 1. Platform Overview

### 1.1 Core Philosophy

The platform operates on a **"connect and forget"** principle:

1. Client connects their infrastructure and tools (one-time setup, ~30 minutes)
2. AI agents take over — generating controls, writing policies, collecting evidence, monitoring continuously
3. Client only intervenes for: approval of generated artifacts, risk acceptance decisions, auditor meetings
4. Auditors get a self-service portal to review everything independently

### 1.2 Delivery Modes

| Mode | Description |
|---|---|
| **Self-hosted (Open Source)** | Docker Compose / Kubernetes. Full platform, no restrictions. AGPLv3 license. |
| **SaaS (Managed)** | Multi-tenant hosted version. Free tier + paid tiers. Handles infra, updates, backups. |
| **Hybrid** | Self-hosted platform with SaaS agent orchestration (for orgs that want data on-prem but AI in cloud) |

### 1.3 What We Automate vs. What Requires Humans

| Fully Automated (Zero Touch) | Human-in-the-Loop (Approval Only) | Requires Human |
|---|---|---|
| Evidence collection | Policy approval & publishing | Risk acceptance decisions |
| Control test execution | Remediation execution | Business context for risk assessments |
| Compliance score calculation | Vendor risk tier assignment | Auditor meetings |
| Drift detection & alerting | Exception approvals | Board-level risk discussions |
| Access review data gathering | Pen test scope approval | Legal/regulatory interpretation |
| Vulnerability scanning | Custom control creation | |
| Training assignment | | |

---

## 2. User Personas & Roles

### 2.1 Platform Roles

| Role | Permissions | Description |
|---|---|---|
| **Super Admin** | Full platform access | Platform owner, manages billing, tenant settings |
| **Compliance Manager** | Manage frameworks, controls, policies, evidence, risks, audits | Day-to-day compliance operations |
| **Control Owner** | View/update assigned controls, upload evidence | Department leads responsible for specific controls |
| **Employee** | Complete training, acknowledge policies, respond to access reviews | General staff |
| **Executive / Board** | View dashboards, reports | Read-only executive view |
| **Auditor (External)** | Read-only access to audit workspace | Registered external auditors |
| **Auditor (Internal)** | Read-only access + finding creation | Internal audit team |
| **API / Service Account** | Programmatic access | For CI/CD and automation integrations |

### 2.2 Auditor Registration & Marketplace

Auditors can register independently on the platform:

- **Registration flow**: Name, firm, credentials (CPA, CISA, CISSP, ISO LA), areas of practice, geography
- **Verification**: Platform verifies credentials (manual initially, automated later)
- **Profile**: Public auditor profile with specializations, certifications, reviews
- **Engagement**: Clients can discover and engage auditors directly through the platform
- **Audit workspace**: Dedicated workspace per engagement with evidence access, finding tracking, communication
- **Auditor tools**: Sampling calculator, workpaper templates, control testing checklists

---

## 3. Compliance Framework Engine

### 3.1 Supported Frameworks (Built-in)

| Framework | Version | Category |
|---|---|---|
| SOC 2 Type I & II | 2017 Trust Services Criteria | Service Organization |
| ISO 27001 | 2022 | Information Security |
| ISO 27701 | 2019 | Privacy |
| HIPAA | Current | Healthcare |
| GDPR | Current | Privacy (EU) |
| PCI DSS | v4.0 | Payment Card |
| NIST 800-53 | Rev 5 | Federal/Government |
| NIST CSF | 2.0 | Cybersecurity Framework |
| NIST 800-171 | Rev 3 | CUI Protection |
| FedRAMP | Current | Federal Cloud |
| CCPA/CPRA | Current | Privacy (California) |
| SOX IT Controls | Current | Financial |
| CIS Controls | v8 | Security Best Practices |
| CSA STAR / CCM | v4 | Cloud Security |
| CMMC | 2.0 | Defense Contractors |

### 3.2 Framework Engine Features

| Feature | Description |
|---|---|
| **Cross-framework mapping** | One control satisfies multiple frameworks. E.g., "MFA enforcement" maps to SOC 2 CC6.1 + ISO A.8.5 + NIST IA-2 + PCI 8.4. Pre-built mapping matrix. |
| **Custom framework builder** | Define custom frameworks with custom control domains, objectives, and requirements. For internal policies or regional regulations. |
| **Framework versioning** | Track framework version changes. When a framework updates (e.g., PCI DSS 3.2.1 → 4.0), show diff and migration path. |
| **Compliance scoring** | Per-framework compliance percentage. Weighted by control criticality. |
| **Gap analysis** | AI agent analyzes connected infrastructure against selected framework, shows: met / partially met / not met / not applicable. |

### 3.3 Control-to-Framework Mapping Data Model

```
Framework
  └── Domain (e.g., "Access Control")
       └── Requirement (e.g., "CC6.1 - Logical Access Security")
            └── Control Objective (e.g., "Restrict access to authorized users")
                 └── Control Activity (mapped from template library)
                      ├── Evidence Template (what proves this control works)
                      ├── Test Procedure (how to verify)
                      └── Cross-framework references (other frameworks this satisfies)
```

---

## 4. AI Agent Architecture

### 4.1 Agent Orchestration Layer

**Primary Framework**: LangGraph (MIT) — for complex, stateful agent workflows with branching logic
**Secondary Framework**: CrewAI (MIT) — for multi-agent collaboration patterns
**LLM Gateway**: LiteLLM (MIT) — unified API to route to any LLM (Claude, GPT, Llama, Mistral, local models)

### 4.2 Agent Registry

#### Agent 01: Controls Generation Agent

```
Trigger:     Framework selected + company context provided
Inputs:      - Selected frameworks
             - Company context (size, industry, tech stack, cloud providers)
             - Connected integrations list
             - Control template library
Process:     1. Load framework requirements
             2. Match requirements to control templates from library
             3. Customize controls for company context (e.g., "AWS S3" not "cloud storage")
             4. Map controls across frameworks (dedup)
             5. Assign suggested owners based on control domain
             6. Set test procedures and evidence requirements
Output:      Complete control set with ownership, evidence mapping, test procedures
Human Step:  Review & approve generated controls (bulk approve with exceptions)
```

#### Agent 02: Policy Generation Agent

```
Trigger:     Controls approved OR manual request
Inputs:      - Approved controls
             - Company context (name, industry, size, tech stack)
             - Policy template library
             - Existing policies (if any, for gap analysis)
Process:     1. Identify required policies from control set
             2. Select matching policy templates
             3. Customize with company-specific details
             4. Cross-reference controls to ensure full coverage
             5. Generate version 1.0 of each policy
             6. Create policy distribution plan
Output:      Complete policy documents (Markdown + PDF export)
Policies:    Information Security Policy, Acceptable Use Policy, Access Control Policy,
             Data Classification Policy, Incident Response Plan, Business Continuity Plan,
             Disaster Recovery Plan, Change Management Policy, Vendor Management Policy,
             Data Retention Policy, Encryption Policy, Password Policy, Remote Work Policy,
             Physical Security Policy, Risk Management Policy, SDLC Policy
Human Step:  Review, edit, approve policies
```

#### Agent 03: Evidence Collection Agent

```
Trigger:     Scheduled (hourly/daily/weekly per control) OR manual
Inputs:      - Control requirements
             - Evidence templates (what format, what data)
             - Connected integration credentials
Process:     1. For each control requiring evidence:
                a. Query connected integrations via API
                b. Extract relevant configuration/data
                c. Take automated screenshots where needed (Playwright)
                d. Format evidence per template
                e. Validate evidence completeness
             2. Map evidence to controls
             3. Flag controls with missing/stale evidence
Output:      Evidence artifacts stored and linked to controls
Human Step:  None (fully automated). Alerts on failures.
```

#### Agent 04: Risk Assessment Agent

```
Trigger:     Quarterly schedule OR new scan results OR manual
Inputs:      - Company context
             - Scan results (cloud security, vulnerability, pen test)
             - Control status (passing/failing)
             - Asset inventory
             - Industry threat intelligence
Process:     1. Identify risks from scan results and control gaps
             2. Categorize risks (confidentiality, integrity, availability)
             3. Score likelihood and impact (1-5 scale)
             4. Calculate inherent and residual risk scores
             5. Suggest risk treatment (mitigate, accept, transfer, avoid)
             6. Map risks to controls and assets
Output:      Risk register entries with scores and treatment recommendations
Human Step:  Review risk scores, approve treatment decisions
```

#### Agent 05: Remediation Agent

```
Trigger:     Failed control detected OR vulnerability found
Inputs:      - Failed control details
             - Current misconfiguration
             - Connected cloud/tool access
Process:     1. Analyze root cause of failure
             2. Generate remediation plan (step-by-step)
             3. If auto-remediable:
                a. Generate fix (IaC patch, API call, config change)
                b. Create PR or change request
                c. Wait for approval
                d. Apply fix
                e. Re-test control
             4. If manual remediation needed:
                a. Create task with detailed instructions
                b. Assign to control owner
                c. Track completion
Output:      Remediation actions (automated or manual tasks)
Human Step:  Approve auto-remediation actions before execution
```

#### Agent 06: Audit Preparation Agent

```
Trigger:     Audit engagement created OR 30 days before audit start
Inputs:      - Framework being audited
             - Control status and evidence
             - Previous audit findings (if any)
             - Auditor requirements
Process:     1. Review all controls for selected framework
             2. Identify evidence gaps
             3. Simulate auditor walkthroughs (question/answer pairs)
             4. Generate audit workpapers (pre-populated)
             5. Create evidence packages organized by control domain
             6. Identify high-risk areas likely to receive scrutiny
             7. Generate management responses for any known gaps
Output:      Audit readiness report, pre-populated workpapers, evidence packages
Human Step:  Review readiness report, address identified gaps
```

#### Agent 07: Vendor Risk Assessment Agent

```
Trigger:     New vendor added OR annual vendor review
Inputs:      - Vendor name, category, data access level
             - Vendor's SOC 2 report (PDF parsed)
             - Vendor's security page / trust center
             - Questionnaire responses
Process:     1. Classify vendor risk tier (critical, high, medium, low)
             2. Parse and analyze SOC 2 report
             3. Identify control gaps or qualified opinions
             4. Score vendor risk
             5. Generate vendor risk assessment report
             6. Flag vendors requiring additional due diligence
Output:      Vendor risk assessment with score and recommendations
Human Step:  Approve vendor risk tier, decide on vendor engagement
```

#### Agent 08: Penetration Testing Orchestrator Agent

```
Trigger:     Manual (scheduled pen test) OR pre-audit
Inputs:      - Target scope (IPs, domains, applications)
             - Test type (network, web app, API, cloud)
             - Rules of engagement
Process:     1. Plan test methodology based on scope
             2. Orchestrate open-source pen test tools (see Section 9)
             3. Aggregate and deduplicate findings
             4. Classify severity (Critical, High, Medium, Low, Info)
             5. Generate detailed findings with reproduction steps
             6. Suggest remediation for each finding
             7. Generate executive summary and technical report
Output:      Penetration test report (executive + technical)
Human Step:  Approve scope before execution, review findings
```

#### Agent 09: Security Questionnaire Agent

```
Trigger:     Questionnaire received from customer/prospect
Inputs:      - Questionnaire document (Excel, PDF, web form)
             - Existing controls, policies, evidence
             - Previous questionnaire responses
Process:     1. Parse questionnaire into structured Q&A
             2. Match each question to relevant controls/policies/evidence
             3. Generate response based on actual compliance posture
             4. Flag questions requiring human input
             5. Export in original format
Output:      Completed questionnaire with AI-generated responses
Human Step:  Review and approve responses, fill human-required answers
```

#### Agent 10: Continuous Monitoring Agent

```
Trigger:     Always running (daemon)
Inputs:      - All connected integrations
             - Control test definitions
             - Alert rules
Process:     1. Run control tests on schedule (configurable per control)
             2. Compare results to previous state (drift detection)
             3. If drift detected:
                a. Create alert
                b. Trigger remediation agent (if auto-remediation enabled)
                c. Update compliance score
             4. Log all test results for audit trail
Output:      Real-time compliance status, drift alerts
Human Step:  None (fully automated)
```

### 4.3 Agent Communication & Memory

| Component | Tool | Purpose |
|---|---|---|
| **Agent memory** | PostgreSQL + pgvector | Store agent context, decisions, learnings across runs |
| **Agent messaging** | Redis Pub/Sub | Inter-agent communication (e.g., evidence agent notifies audit prep agent) |
| **Workflow state** | Temporal (Apache 2.0) | Durable workflow execution with retry, timeout, compensation |
| **Audit trail** | Append-only PostgreSQL table | Every agent action logged immutably |

### 4.4 Template Libraries

#### Controls Template Library

```
Structure per template:
{
  "template_id": "ctrl-access-mfa-001",
  "title": "Multi-Factor Authentication Enforcement",
  "domain": "Access Control",
  "description": "All user accounts must use MFA for authentication",
  "implementation_guidance": "Enable MFA in identity provider for all users...",
  "test_procedure": "Query IdP API for MFA enrollment status per user...",
  "evidence_template_id": "evd-mfa-enrollment-001",
  "automation_level": "full",        // full | partial | manual
  "applicable_frameworks": [
    { "framework": "SOC2", "requirement": "CC6.1" },
    { "framework": "ISO27001", "requirement": "A.8.5" },
    { "framework": "NIST800-53", "requirement": "IA-2" },
    { "framework": "PCIDSS", "requirement": "8.4" },
    { "framework": "HIPAA", "requirement": "164.312(d)" }
  ],
  "integration_tests": [
    { "integration": "okta", "test": "check_mfa_enrollment" },
    { "integration": "azure_ad", "test": "check_mfa_policy" },
    { "integration": "google_workspace", "test": "check_2sv_enforcement" }
  ],
  "variables": [
    { "key": "mfa_methods_allowed", "default": ["authenticator_app", "hardware_key"] },
    { "key": "grace_period_days", "default": 7 }
  ]
}
```

Library covers 200+ control templates across all domains:
- Access Control (25+ templates)
- Change Management (15+ templates)
- Data Protection & Encryption (20+ templates)
- Network Security (15+ templates)
- Endpoint Security (15+ templates)
- Logging & Monitoring (20+ templates)
- Incident Response (10+ templates)
- Business Continuity (10+ templates)
- Human Resources Security (15+ templates)
- Physical Security (10+ templates)
- Vendor Management (10+ templates)
- Software Development (20+ templates)
- Risk Management (10+ templates)
- Compliance & Governance (10+ templates)

#### Evidence Template Library

```
Structure per template:
{
  "template_id": "evd-mfa-enrollment-001",
  "title": "MFA Enrollment Evidence",
  "description": "Screenshot or export showing MFA enrollment status for all users",
  "evidence_type": "automated",     // automated | manual_upload | screenshot
  "format": "json_export",          // json_export | screenshot | pdf | csv
  "collection_method": "api_query", // api_query | screenshot | manual
  "refresh_frequency": "daily",
  "retention_period": "13_months",  // for SOC 2 Type II observation period
  "fields": [
    { "field": "total_users", "type": "number" },
    { "field": "mfa_enrolled_users", "type": "number" },
    { "field": "mfa_enrollment_percentage", "type": "percentage" },
    { "field": "non_enrolled_users", "type": "array", "detail": "username, email, last_login" },
    { "field": "mfa_methods_distribution", "type": "object" },
    { "field": "collection_timestamp", "type": "datetime" }
  ],
  "pass_criteria": {
    "mfa_enrollment_percentage": { "operator": ">=", "value": 100 }
  },
  "integrations": ["okta", "azure_ad", "google_workspace", "jumpcloud"]
}
```

#### Policy Template Library

```
Structure per template:
{
  "template_id": "pol-infosec-001",
  "title": "Information Security Policy",
  "required_by_frameworks": ["SOC2", "ISO27001", "HIPAA", "PCIDSS"],
  "sections": [
    "Purpose", "Scope", "Roles and Responsibilities",
    "Policy Statements", "Enforcement", "Review Schedule"
  ],
  "variables": [
    { "key": "company_name", "source": "org_context" },
    { "key": "review_frequency", "default": "annual" },
    { "key": "policy_owner", "source": "role:compliance_manager" },
    { "key": "classification_levels", "default": ["Public", "Internal", "Confidential", "Restricted"] }
  ],
  "review_frequency": "annual",
  "template_content": "markdown_template_with_variables"
}
```

---

## 5. Controls Engine

### 5.1 Control Lifecycle

```
Template Selection → Customization → Review/Approve → Implementation → Testing → Monitoring → Audit
      (AI)              (AI)          (Human)          (AI/Human)      (AI)      (AI)       (Auditor)
```

### 5.2 Features

| Feature | Description |
|---|---|
| **Auto-generation from templates** | AI selects relevant controls from template library based on framework + company context |
| **Cross-framework deduplication** | One implemented control satisfies multiple frameworks. Single control view shows all mapped frameworks. |
| **Control ownership assignment** | AI suggests owners based on control domain. E.g., "Network Security" controls → IT/Infrastructure team lead. |
| **Control testing** | Automated tests run on schedule. Tests defined per control template. Results: Pass/Fail/Error/Not Tested. |
| **Control effectiveness rating** | Based on test history: Effective / Needs Improvement / Ineffective |
| **Control exceptions** | Request, approve, track exceptions with expiry dates and compensating controls |
| **Control versioning** | Track changes to control implementation over time |
| **Bulk operations** | Approve, assign, update multiple controls at once |
| **Control dependencies** | Some controls depend on others (e.g., "Log Review" depends on "Centralized Logging") |

### 5.3 User Input → Controls Mapping

The system uses structured user inputs to determine which controls to generate:

```
User Input Fields:
├── Company Profile
│   ├── Industry (SaaS, Healthcare, Fintech, E-commerce, etc.)
│   ├── Company size (1-50, 51-200, 201-1000, 1000+)
│   ├── Data types handled (PII, PHI, PCI, IP, none)
│   └── Geographic regions (US, EU, APAC, etc.)
├── Technical Environment
│   ├── Cloud providers (AWS, GCP, Azure, multi-cloud)
│   ├── Identity provider (Okta, Azure AD, Google Workspace, JumpCloud)
│   ├── Source control (GitHub, GitLab, Bitbucket)
│   ├── CI/CD (GitHub Actions, Jenkins, CircleCI, GitLab CI)
│   ├── Infrastructure approach (IaC, manual, hybrid)
│   ├── Container usage (Kubernetes, ECS, Docker, none)
│   └── Database types (PostgreSQL, MySQL, MongoDB, DynamoDB, etc.)
├── Selected Frameworks
│   └── [SOC2, ISO27001, HIPAA, etc.]
└── Current Maturity
    ├── Existing policies (yes/no, upload if yes)
    ├── Previous audits (yes/no, upload findings if yes)
    └── Known gaps (free text)
```

Mapping Engine:
```
User Input → Framework Requirements → Template Library → Filtered & Customized Controls
             (what's needed)          (how to implement)   (tailored to this company)
```

---

## 6. Policy Engine

### 6.1 Features

| Feature | Description |
|---|---|
| **AI generation from templates** | Policies generated from template library, customized with company context and control requirements |
| **Variable interpolation** | Company name, specific tool names, team names, dates auto-inserted |
| **Version control** | Full version history with diff view. Major/minor versioning. |
| **Approval workflow** | Draft → Review → Approve → Published. Multi-level approval chains. |
| **Employee acknowledgment** | Track who has read and acknowledged each policy. Reminder automation. |
| **Distribution** | Auto-distribute via Slack, email, or in-platform notification when policies update |
| **Annual review automation** | Auto-create review tasks on policy anniversary. Assign to policy owner. |
| **Policy gap analysis** | AI identifies controls not covered by any policy |
| **Export formats** | Markdown (source), PDF, DOCX |
| **Policy portal** | Internal-facing portal where employees can browse all active policies |

### 6.2 Policy Documents Generated

| Policy | Frameworks | AI Generation Level |
|---|---|---|
| Information Security Policy | All | Full — template + company context |
| Acceptable Use Policy | All | Full |
| Access Control Policy | All | Full — customized per identity provider |
| Data Classification Policy | All | Full |
| Data Retention & Disposal Policy | GDPR, HIPAA, SOC 2 | Full |
| Encryption Policy | All | Full — customized per cloud provider |
| Incident Response Plan | All | Full — includes escalation contacts |
| Business Continuity Plan | SOC 2, ISO 27001 | Partial — requires business input |
| Disaster Recovery Plan | SOC 2, ISO 27001 | Full — customized per infrastructure |
| Change Management Policy | All | Full — customized per CI/CD tools |
| Vendor Management Policy | All | Full |
| Password / Authentication Policy | All | Full — reflects actual IdP settings |
| Remote Work / BYOD Policy | SOC 2, ISO 27001 | Full |
| Physical Security Policy | ISO 27001, SOC 2 | Partial — requires physical location details |
| Risk Management Policy | All | Full |
| SDLC / Secure Development Policy | SOC 2, ISO 27001, PCI DSS | Full — customized per dev tools |
| Privacy Policy | GDPR, CCPA, HIPAA | Partial — requires legal review |
| Vulnerability Management Policy | All | Full |
| Logging & Monitoring Policy | All | Full — customized per SIEM/logging tools |
| Network Security Policy | PCI DSS, ISO 27001 | Full — customized per cloud networking |

---

## 7. Evidence Engine

### 7.1 Evidence Collection Methods

| Method | Description | Example |
|---|---|---|
| **API query** | Direct API calls to integrated tools | Pull MFA enrollment from Okta API |
| **Automated screenshot** | Playwright-based screenshots of tool dashboards | Screenshot of AWS GuardDuty settings |
| **Configuration export** | Export JSON/YAML configs from cloud APIs | AWS S3 bucket policy export |
| **Log extract** | Pull relevant log entries for a time period | CloudTrail logs showing access review |
| **Report generation** | Generate reports from scan results | Prowler compliance report |
| **Manual upload** | User uploads evidence (last resort) | Physical security photos |

### 7.2 Evidence Management Features

| Feature | Description |
|---|---|
| **Auto-collection on schedule** | Configurable per control: hourly, daily, weekly, monthly |
| **Evidence versioning** | Every collection creates a new version. Full history retained. |
| **Freshness tracking** | Show how old each evidence artifact is. Alert on stale evidence. |
| **Evidence-to-control mapping** | One evidence artifact can satisfy multiple controls |
| **Pass/fail evaluation** | Automated evaluation against pass criteria defined in evidence template |
| **Evidence packaging** | Bundle evidence by control domain for auditor consumption |
| **Tamper-proof storage** | SHA-256 hash of each evidence artifact at collection time. Stored in append-only log. |
| **Retention management** | Auto-retain evidence per retention policy. Alert before deletion. |
| **Storage backend** | MinIO (AGPLv3) — self-hosted S3-compatible object storage |

### 7.3 Evidence Storage

| Component | Tool | License |
|---|---|---|
| Object storage | **MinIO** | AGPLv3 |
| Metadata store | PostgreSQL | PostgreSQL License |
| Full-text search | **Meilisearch** | MIT |
| PDF parsing | **Apache Tika** | Apache 2.0 |

---

## 8. Cloud Security Monitoring

### 8.1 Open Source Security Scanning Stack

#### Cloud Security Posture Management (CSPM)

| Tool | License | Purpose | Cloud Support |
|---|---|---|---|
| **Prowler** | Apache 2.0 | Cloud security assessment. 300+ checks for AWS, 60+ for Azure, 70+ for GCP. Maps to CIS, NIST, PCI, HIPAA, SOC 2, GDPR. | AWS, Azure, GCP |
| **ScoutSuite** | GPL 2.0 | Multi-cloud security auditing. Collects configuration data via APIs. | AWS, Azure, GCP, Oracle, Alibaba |
| **CloudSploit** | GPL 2.0 | Cloud security configuration monitoring. 500+ checks. | AWS, Azure, GCP, Oracle |
| **Steampipe** | AGPLv3 | Query cloud APIs using SQL. 140+ plugins. Real-time querying. | AWS, Azure, GCP, Kubernetes, + 100 more |

#### Infrastructure as Code (IaC) Security

| Tool | License | Purpose |
|---|---|---|
| **Checkov** | Apache 2.0 | Static analysis for IaC. Supports Terraform, CloudFormation, Kubernetes, Helm, ARM templates. 1000+ built-in checks. |
| **tfsec** | MIT | Terraform-specific security scanner. Fast, focused. |
| **KICS** | Apache 2.0 | IaC security scanner. Supports Terraform, Docker, Kubernetes, Ansible, CloudFormation. |
| **Terrascan** | Apache 2.0 | Compliance-as-code for IaC. 500+ policies for CIS, NIST. |

#### Container & Image Security

| Tool | License | Purpose |
|---|---|---|
| **Trivy** | Apache 2.0 | Comprehensive vulnerability scanner. Containers, filesystems, repos, IaC. SBOM generation. |
| **Grype** | Apache 2.0 | Container image vulnerability scanner. Works with Syft SBOMs. |
| **Syft** | Apache 2.0 | SBOM generator. Catalogs packages in container images and filesystems. |
| **Clair** | Apache 2.0 | Container vulnerability analysis. Indexes and matches vulnerabilities. |
| **Falco** | Apache 2.0 | Runtime security. Detects anomalous activity in containers/hosts using system call monitoring. |

#### Secret Detection

| Tool | License | Purpose |
|---|---|---|
| **TruffleHog** | AGPLv3 | Find leaked secrets in git repos, S3 buckets, filesystems. Verification of live secrets. |
| **Gitleaks** | MIT | Git secret scanning. Pre-commit hook support. CI/CD integration. |
| **detect-secrets** | Apache 2.0 | Yelp's secret detection. Baseline approach — track known secrets, alert on new ones. |

#### Static Application Security Testing (SAST)

| Tool | License | Purpose |
|---|---|---|
| **Semgrep** | LGPL 2.1 | Lightweight static analysis. Custom rules. Supports 30+ languages. |
| **Bandit** | Apache 2.0 | Python-specific security linter. |
| **Brakeman** | MIT | Ruby on Rails security scanner. |
| **ESLint Security Plugin** | MIT | JavaScript/TypeScript security rules. |
| **SonarQube Community** | LGPL 3.0 | Code quality + security analysis. 27 languages. |

#### Software Composition Analysis (SCA)

| Tool | License | Purpose |
|---|---|---|
| **OSV-Scanner** | Apache 2.0 | Google's vulnerability scanner using OSV database. |
| **Dependency-Check** | Apache 2.0 | OWASP tool. Checks dependencies for known vulnerabilities (NVD). |
| **npm audit / pip audit** | Built-in | Package manager native vulnerability checks. |

#### SIEM & Log Management

| Tool | License | Purpose |
|---|---|---|
| **Wazuh** | GPL 2.0 | Full SIEM. Host-based intrusion detection, log analysis, file integrity monitoring, vulnerability detection. |
| **OSSEC** | GPL 2.0 | Host-based intrusion detection. Log analysis, rootkit detection. |
| **Suricata** | GPL 2.0 | Network threat detection. IDS/IPS. Protocol analysis. |
| **GrayLog** | SSPL (open edition) | Log management and analysis. |

### 8.2 How Scanning Integrates with the Platform

```
Scheduled Trigger
    │
    ▼
┌─────────────────────┐
│  Scanner Orchestrator│  (Temporal workflow)
│                      │
│  1. Prowler scan     │──→ Cloud misconfigurations
│  2. Trivy scan       │──→ Container vulnerabilities
│  3. Checkov scan     │──→ IaC issues
│  4. Semgrep scan     │──→ Code security issues
│  5. TruffleHog scan  │──→ Leaked secrets
│  6. OSV-Scanner      │──→ Dependency vulnerabilities
│  7. Wazuh alerts     │──→ Runtime security events
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Results Normalizer  │  (Unified finding format)
└─────────┬───────────┘
          │
          ├──→ Evidence Engine (map findings to controls)
          ├──→ Risk Assessment Agent (new risks identified)
          ├──→ Remediation Agent (auto-fix where possible)
          └──→ Dashboard (real-time compliance impact)
```

---

## 9. Penetration Testing Agents

### 9.1 Open Source Penetration Testing Tools

#### Reconnaissance

| Tool | License | Purpose |
|---|---|---|
| **Nmap** | Custom OSS | Network discovery, port scanning, service detection, OS fingerprinting |
| **Masscan** | AGPLv3 | High-speed port scanner. Scans entire internet in 6 minutes. |
| **RustScan** | GPL 3.0 | Fast port scanner. Pipes results to Nmap for service detection. |
| **Subfinder** | MIT | Subdomain discovery. Passive reconnaissance using multiple sources. |
| **Amass** | Apache 2.0 | Attack surface mapping. DNS enumeration, subdomain discovery. |
| **httpx** | MIT | HTTP toolkit. Probe URLs for status, title, tech stack. |
| **Katana** | MIT | Web crawler. Discovers endpoints, JavaScript parsing, form detection. |
| **Shodan CLI** | MIT (client) | Internet-connected device search (requires API key). |

#### Web Application Testing

| Tool | License | Purpose |
|---|---|---|
| **OWASP ZAP** | Apache 2.0 | Web application security scanner. Active/passive scanning. API scanning. |
| **Nuclei** | MIT | Template-based vulnerability scanner. 7000+ community templates. Fast. |
| **Nikto** | GPL | Web server vulnerability scanner. 6700+ checks. |
| **Wapiti** | GPL 2.0 | Web vulnerability scanner. Injection, XSS, SSRF, XXE detection. |
| **ffuf** | MIT | Web fuzzer. Directory discovery, parameter fuzzing, virtual host discovery. |
| **Gobuster** | Apache 2.0 | Directory/DNS brute-forcing. Fast. |
| **SQLMap** | GPL 2.0 | Automated SQL injection detection and exploitation. |
| **XSStrike** | GPL 3.0 | XSS detection suite. |

#### API Testing

| Tool | License | Purpose |
|---|---|---|
| **Arjun** | GPL 3.0 | HTTP parameter discovery. |
| **Kiterunner** | Apache 2.0 | API endpoint discovery and content discovery. |
| **Postman/Newman** | MIT (Newman) | API testing automation. |

#### Network / Infrastructure Testing

| Tool | License | Purpose |
|---|---|---|
| **Metasploit Framework** | BSD | Exploitation framework. Module-based. Verify vulnerabilities. |
| **CrackMapExec / NetExec** | BSD | Network pentesting. SMB, WinRM, LDAP, MSSQL. |
| **Impacket** | Apache 2.0 | Python library for network protocols. SMB, MSRPC, Kerberos. |
| **Responder** | GPL 3.0 | LLMNR/NBT-NS/MDNS poisoner. |
| **Certipy** | MIT | Active Directory Certificate Services enumeration and abuse. |

#### Cloud-Specific Testing

| Tool | License | Purpose |
|---|---|---|
| **Pacu** | BSD | AWS exploitation framework. Post-exploitation, privilege escalation. |
| **ScoutSuite** | GPL 2.0 | Multi-cloud security auditing. |
| **CloudFox** | MIT | Cloud penetration testing. Find exploitable paths in cloud infrastructure. |
| **Prowler** | Apache 2.0 | (Also used for CSPM — security findings feed into pen test scoping) |

#### Credential Testing

| Tool | License | Purpose |
|---|---|---|
| **Hydra** | GPL 3.0 | Online password brute-forcing. HTTP, SSH, FTP, SMB, etc. |
| **John the Ripper** | GPL 2.0 | Offline password cracking. Hash identification. |
| **Hashcat** | MIT | GPU-based password recovery. |

### 9.2 Penetration Test Agent Orchestration

```
Pen Test Request (with approved scope)
    │
    ▼
┌─────────────────────────────────┐
│  Pen Test Orchestrator Agent    │
│                                 │
│  Phase 1: Reconnaissance        │
│  ├── Nmap / RustScan           │──→ Open ports, services
│  ├── Subfinder / Amass         │──→ Subdomains
│  ├── httpx                     │──→ Live hosts, tech stack
│  └── Katana                    │──→ URLs, endpoints
│                                 │
│  Phase 2: Vulnerability Scan    │
│  ├── Nuclei                    │──→ Known CVEs, misconfigs
│  ├── OWASP ZAP                 │──→ Web app vulns (OWASP Top 10)
│  ├── SQLMap (targeted)         │──→ SQL injection
│  ├── ffuf                      │──→ Hidden endpoints
│  └── Trivy                    │──→ Container/dependency vulns
│                                 │
│  Phase 3: Exploitation (opt-in) │
│  ├── Metasploit                │──→ Exploit verification
│  ├── Pacu (AWS)                │──→ Cloud privilege escalation
│  └── CrackMapExec              │──→ Network lateral movement
│                                 │
│  Phase 4: Reporting             │
│  ├── Normalize findings        │
│  ├── Deduplicate               │
│  ├── CVSS scoring              │
│  ├── Evidence collection       │
│  └── Report generation         │
└─────────────────────────────────┘
    │
    ▼
  Output:
  ├── Executive Summary (1-2 pages)
  ├── Technical Findings (detailed, per finding)
  ├── Risk Matrix
  ├── Remediation Recommendations
  └── Re-test Verification Plan
```

### 9.3 Safety Controls for Pen Testing

| Control | Description |
|---|---|
| **Scope lock** | Agent can ONLY test explicitly approved targets. Hard-coded scope validation before every tool execution. |
| **Rate limiting** | Configurable scan intensity. Default: "polite" mode. |
| **Kill switch** | Manual stop button. Auto-stop on scope violation. |
| **Exploitation opt-in** | Phase 3 (exploitation) requires separate explicit approval. Default: scan-only. |
| **Audit trail** | Every command executed by pen test agent is logged with timestamp, target, output. |
| **Credential handling** | Test credentials stored encrypted. Cleared after engagement. |
| **Network isolation** | Pen test agents run in isolated containers with controlled egress. |

---

## 10. Integration Hub

### 10.1 Integration Architecture

```
┌──────────────────────────────────────────────┐
│  Integration Hub                             │
│                                              │
│  ┌─────────────┐   ┌──────────────────────┐ │
│  │  Connector   │   │  Credential Vault    │ │
│  │  Plugin API  │   │  (HashiCorp Vault /  │ │
│  │              │   │   Infisical)         │ │
│  └──────┬──────┘   └──────────┬───────────┘ │
│         │                     │              │
│  ┌──────▼─────────────────────▼───────────┐ │
│  │  Connector Registry                     │ │
│  │                                         │ │
│  │  Each connector implements:             │ │
│  │  - authenticate()                       │ │
│  │  - list_resources()                     │ │
│  │  - collect_evidence(control_id)         │ │
│  │  - test_control(control_id)             │ │
│  │  - get_configuration()                  │ │
│  │  - remediate(finding_id)   [optional]   │ │
│  └─────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘
```

### 10.2 Credential Management

| Tool | License | Purpose |
|---|---|---|
| **Infisical** | MIT (core) | Open-source secret management. API-first. Integrates with cloud providers. |
| **HashiCorp Vault** | BUSL 1.1 (was MPL) | Secret management, encryption as a service. *Note: license changed — evaluate Infisical first.* |
| **SOPS** | MPL 2.0 | Encrypted file secrets. Good for IaC. |

### 10.3 Integration Categories & Connectors

#### Cloud Providers

| Integration | Auth Method | Evidence Collected |
|---|---|---|
| **AWS** | IAM Role / Access Key | IAM policies, S3 configs, SecurityHub findings, CloudTrail, GuardDuty, VPC configs, encryption settings, KMS keys, RDS configs, ECS/EKS settings |
| **Google Cloud** | Service Account | IAM, Cloud Audit Logs, Security Command Center, VPC, GKE, Cloud KMS, BigQuery access |
| **Azure** | Service Principal | Azure AD, Defender for Cloud, Activity Logs, NSGs, Key Vault, AKS, Storage accounts |
| **DigitalOcean** | API Token | Droplet configs, firewall rules, database settings |

#### Identity Providers

| Integration | Auth Method | Evidence Collected |
|---|---|---|
| **Okta** | API Token | MFA enrollment, SSO configs, user lifecycle, password policies, admin roles, application access |
| **Azure AD / Entra ID** | OAuth | Conditional access policies, MFA status, user provisioning, group memberships, sign-in logs |
| **Google Workspace** | Service Account | 2SV enforcement, admin roles, OAuth app access, Drive sharing settings, mobile device management |
| **JumpCloud** | API Key | MFA, SSO, device management, user groups, policies |
| **OneLogin** | API Credentials | MFA, SSO, user provisioning, app access |

#### Source Code & CI/CD

| Integration | Auth Method | Evidence Collected |
|---|---|---|
| **GitHub** | GitHub App | Branch protection, PR review requirements, secret scanning, Dependabot, Actions configs, CODEOWNERS, commit signing |
| **GitLab** | OAuth / Token | Protected branches, MR approvals, SAST/DAST, container scanning, dependency scanning |
| **Bitbucket** | OAuth | Branch permissions, PR requirements, pipeline configs |
| **GitHub Actions** | (via GitHub) | Deployment approvals, environment protection, workflow permissions |
| **Jenkins** | API Token | Job configs, security settings, plugin versions |
| **CircleCI** | API Token | Pipeline configs, environment variables management |

#### Project Management & Ticketing

| Integration | Auth Method | Evidence Collected |
|---|---|---|
| **Jira** | OAuth / API Token | Change management tickets, incident tracking, SLA compliance, workflow configs |
| **Linear** | API Key | Issue tracking, cycle analytics, triage workflows |
| **Asana** | OAuth | Task management, approval workflows |
| **GitHub Issues** | (via GitHub) | Issue tracking, labeling, project boards |

#### Communication

| Integration | Auth Method | Evidence Collected |
|---|---|---|
| **Slack** | OAuth Bot | Security alert channels, policy acknowledgment messages, DLP settings, retention settings, SSO config |
| **Microsoft Teams** | OAuth | Channel configs, compliance settings, guest access policies |
| **Email (Google/M365)** | (via IdP) | Email security settings (DMARC, SPF, DKIM), DLP policies, retention |

#### HR Systems

| Integration | Auth Method | Evidence Collected |
|---|---|---|
| **BambooHR** | API Key | Employee directory, onboarding/offboarding status, org chart |
| **Gusto** | OAuth | Employee data, onboarding checklists |
| **Rippling** | API Key | Employee lifecycle, device management, app access |
| **Workday** | OAuth | Employee data, org structure |

#### Endpoint / MDM

| Integration | Auth Method | Evidence Collected |
|---|---|---|
| **CrowdStrike** | API Key | Endpoint protection status, detection events, sensor coverage |
| **SentinelOne** | API Token | Endpoint status, threat detection, device compliance |
| **Jamf** | API Credentials | macOS management, disk encryption (FileVault), OS updates, screen lock |
| **Microsoft Intune** | OAuth | Device compliance, BitLocker, OS updates, security baselines |
| **Kolide** | API Key | Device health checks, compliance queries |
| **osquery** | Direct | Cross-platform endpoint visibility via SQL queries |

#### Vulnerability Management

| Integration | Auth Method | Evidence Collected |
|---|---|---|
| **Snyk** | API Token | Code vulnerabilities, container vulns, IaC issues, license compliance |
| **Dependabot** | (via GitHub) | Dependency vulnerabilities, auto-update PRs |
| **Qualys** | API Credentials | Network vulnerability scans, web app scans |
| **OpenVAS (Greenbone)** | API | Network vulnerability assessment (open source Nessus alternative) |

#### Monitoring & Observability

| Integration | Auth Method | Evidence Collected |
|---|---|---|
| **Grafana** | API Key | Dashboard configs, alert rules, uptime monitoring |
| **Prometheus** | API | Alert rules, recording rules, target health |
| **PagerDuty** | API Token | Incident response, on-call schedules, escalation policies |
| **Opsgenie** | API Key | Alert routing, on-call, incident management |
| **Uptime Kuma** | API (self-hosted) | Uptime monitoring (open source) |

#### Databases

| Integration | Auth Method | Evidence Collected |
|---|---|---|
| **PostgreSQL** | Connection String | User roles, encryption settings, audit logging config, backup status |
| **MySQL** | Connection String | User privileges, SSL config, audit plugin status |
| **MongoDB** | Connection String | Authentication settings, encryption, audit logging |
| **Redis** | Connection String | AUTH config, TLS, ACL settings |

### 10.4 Workflow Automation

| Tool | License | Purpose |
|---|---|---|
| **Temporal** | Apache 2.0 | Workflow orchestration. Durable execution. Retries, timeouts, versioning. For long-running integration workflows. |
| **n8n** | Sustainable Use License | Visual workflow automation. Good for custom integration flows. *Note: evaluate license compatibility.* |
| **BullMQ** | MIT | Redis-based job queue. For simple scheduled tasks and background processing. |

---

## 11. Risk Management

### 11.1 Features

| Feature | Description |
|---|---|
| **Risk register** | Centralized catalog of all identified risks. Auto-populated from scan results + AI analysis. |
| **Risk scoring** | Quantitative: Likelihood (1-5) x Impact (1-5) = Risk Score (1-25). Qualitative labels: Critical, High, Medium, Low. |
| **Inherent vs. residual risk** | Inherent = risk without controls. Residual = risk with controls in place. |
| **Risk treatment** | Four options per risk: Mitigate, Accept, Transfer, Avoid. Track treatment status. |
| **Risk heatmap** | Visual matrix showing risk distribution by likelihood and impact. |
| **Risk appetite / tolerance** | Define organizational risk appetite. Flag risks exceeding tolerance. |
| **Risk ownership** | Assign risk owners. Track accountability. |
| **Risk-to-control mapping** | Each risk linked to controls that mitigate it. |
| **Auto-risk identification** | AI agent scans infrastructure and scan results to surface new risks. |
| **Risk trending** | Historical risk score over time. Show improvement or degradation. |
| **Risk reporting** | Board-ready risk reports. Top risks, treatment progress, risk appetite alignment. |

### 11.2 Third-Party Risk (See Section 16)

---

## 12. Audit Management & Auditor Portal

### 12.1 Auditor Registration System

```
Auditor Registration Flow:
1. Auditor signs up (email, firm name, credentials)
2. Selects specializations (SOC 2, ISO 27001, HIPAA, etc.)
3. Uploads certifications (CPA, CISA, CISSP, ISO 27001 Lead Auditor)
4. Platform verifies credentials (manual review initially)
5. Auditor profile published in marketplace
6. Clients can discover, message, and engage auditors
```

### 12.2 Auditor Portal Features

| Feature | Description |
|---|---|
| **Read-only evidence view** | Auditor sees all evidence organized by control domain. Can filter, search, download. |
| **Control testing workspace** | Auditor can mark controls as: Tested/Effective, Tested/Exception, Not Tested. |
| **Sampling tools** | Statistical sampling calculator. Random sample generation from populations. |
| **Finding management** | Create findings with severity, description, recommendation. Track management response. |
| **Workpaper templates** | Pre-built workpaper templates for each framework. AI pre-populated. |
| **Communication** | In-platform messaging between auditor and client. Threaded discussions per control. |
| **Evidence request system** | Auditor can request additional evidence. Client gets notified. |
| **Report generation** | Generate audit report drafts from findings and evidence. |
| **Multi-engagement support** | Auditor can manage multiple client engagements simultaneously. |
| **Audit timeline** | Gantt-style view of audit phases, milestones, deadlines. |

### 12.3 Audit Lifecycle

```
1. Engagement Setup
   ├── Client creates audit engagement
   ├── Selects framework(s) and audit period
   ├── Invites auditor (from marketplace or by email)
   └── Defines scope and timeline

2. Pre-Audit Preparation (AI Agent handles)
   ├── Evidence packaging by control domain
   ├── Workpaper pre-population
   ├── Gap analysis and readiness score
   └── Simulated audit walkthrough

3. Fieldwork
   ├── Auditor reviews evidence in portal
   ├── Auditor performs control testing
   ├── Auditor requests additional evidence
   ├── Client/AI agent provides evidence
   └── Auditor creates findings

4. Reporting
   ├── Auditor finalizes findings
   ├── Client provides management responses
   ├── Auditor generates audit report
   └── Report delivered through platform

5. Remediation Tracking
   ├── Findings converted to remediation tasks
   ├── Assigned to control owners
   ├── Tracked to completion
   └── Re-testing by auditor
```

---

## 13. Continuous Monitoring & Alerting

### 13.1 Features

| Feature | Description |
|---|---|
| **Scheduled control tests** | Every control with an automated test runs on schedule (configurable: 1h, 6h, 12h, 24h, 7d) |
| **Drift detection** | Compares current state to last known good state. Alerts on any change. |
| **Compliance score tracking** | Real-time compliance percentage per framework. Historical trending. |
| **Alert channels** | Slack, Microsoft Teams, email, PagerDuty, OpsGenie, webhooks |
| **Alert rules** | Configurable: alert on any failure, only critical, only for specific controls |
| **Auto-remediation triggers** | Optionally trigger remediation agent on specific control failures |
| **SLA tracking** | Time-to-fix tracking per severity. SLA breach alerts. |
| **Compliance regression alerts** | "Your SOC 2 compliance dropped from 97% to 91% in the last 24 hours" |
| **Change correlation** | Link compliance changes to infrastructure changes (via integration with CI/CD, cloud events) |

### 13.2 Monitoring Stack

| Component | Tool | License |
|---|---|---|
| Metric collection | **Prometheus** | Apache 2.0 |
| Visualization | **Grafana** | AGPLv3 |
| Uptime monitoring | **Uptime Kuma** | MIT |
| Alerting | **Alertmanager** (Prometheus) | Apache 2.0 |
| Log aggregation | **Wazuh** | GPL 2.0 |

---

## 14. Access Review Automation

### 14.1 Features

| Feature | Description |
|---|---|
| **User aggregation** | Pull all user accounts from all integrated systems. Unified view. |
| **Access matrix** | Show each user's access across all systems. Role, permissions, last login. |
| **Review campaigns** | Create periodic (quarterly) access review campaigns. Assign reviewers per department. |
| **Manager certification** | Route each user's access to their manager for approve/revoke decision. |
| **Over-provisioned access detection** | AI flags users with access they haven't used in 90+ days. |
| **Orphan account detection** | Cross-reference HR system with all tool accounts. Flag accounts for departed employees. |
| **Privilege escalation alerts** | Real-time alert when admin/elevated access is granted. |
| **Segregation of duties** | Define conflicting role combinations. Alert on violations. |
| **Review evidence generation** | Auto-generate evidence artifacts from completed access reviews. |
| **Automated deprovisioning** | With approval, auto-revoke access via integration APIs. |

---

## 15. Incident Management

### 15.1 Features

| Feature | Description |
|---|---|
| **Incident register** | Log, classify, and track security incidents. |
| **Severity classification** | P1 (Critical), P2 (High), P3 (Medium), P4 (Low). Auto-classify from source. |
| **Incident response playbooks** | Template-based workflows per incident type (data breach, malware, DDoS, insider threat, phishing). |
| **Auto-incident creation** | Create incidents from Wazuh alerts, cloud security findings, pen test findings. |
| **Timeline tracking** | Detailed timeline of incident events, actions taken, communications. |
| **Breach notification tracker** | GDPR 72-hour clock, HIPAA notification requirements, state breach notification laws. |
| **Post-mortem templates** | Structured root cause analysis. AI assists with drafting. |
| **Lessons learned** | Track improvements from incidents. Link to new/updated controls. |
| **Communication templates** | Pre-built templates for notifying affected parties, regulators, media. |
| **Metrics** | MTTD (mean time to detect), MTTR (mean time to respond), incident trending. |

---

## 16. Vendor Risk Management

### 16.1 Features

| Feature | Description |
|---|---|
| **Vendor inventory** | Central registry of all third-party vendors. |
| **Risk tiering** | Auto-classify: Critical (access to sensitive data), High, Medium, Low. Based on data access, business criticality. |
| **Due diligence automation** | AI agent collects vendor's SOC 2 report, security page, trust center, certifications. |
| **SOC 2 report analysis** | AI parses vendor SOC 2 PDFs, identifies exceptions, qualified opinions, gaps. |
| **Questionnaire management** | Send/receive security questionnaires (SIG, CAIQ, custom). AI auto-fills from vendor data. |
| **Vendor scoring** | Risk score based on security posture, certifications, questionnaire responses. |
| **Ongoing monitoring** | Track vendor security changes. Alert on vendor breaches (via news monitoring). |
| **Contract tracking** | Track vendor contracts, SLAs, DPAs, BAAs. Renewal reminders. |
| **Sub-processor management** | Track vendor's sub-processors (GDPR requirement). |
| **Vendor review scheduling** | Annual review for critical vendors, biennial for others. Auto-assignment. |

---

## 17. Training & Awareness

### 17.1 Features

| Feature | Description |
|---|---|
| **Built-in training modules** | Security awareness, phishing recognition, data handling, incident reporting. Open-source content. |
| **Training assignment engine** | Auto-assign based on role, department, framework requirements. New hire assignments on onboarding. |
| **Completion tracking** | Dashboard showing completion rates by department, due dates, overdue alerts. |
| **Policy quiz generation** | AI generates quizzes from your actual policies. Ensures employees understand content. |
| **Training evidence** | Auto-generate evidence artifacts showing training completion rates for auditors. |
| **Phishing simulation** | Basic phishing test campaigns using **GoPhish** (MIT license). |
| **Annual recertification** | Auto-schedule annual refresher training. |
| **Custom content** | Upload custom training materials (video, PDF, slides). |
| **Integration with LMS** | Connect to existing LMS if org already has one. |

### 17.2 Training Tool

| Tool | License | Purpose |
|---|---|---|
| **GoPhish** | MIT | Phishing simulation campaigns |

---

## 18. Security Questionnaire Automation

### 18.1 Features

| Feature | Description |
|---|---|
| **Questionnaire ingestion** | Upload Excel, PDF, or paste web form URL. AI parses into structured Q&A. |
| **Knowledge base** | Build knowledge base from your controls, policies, evidence, previous responses. |
| **AI auto-fill** | Match each question to knowledge base. Generate response. Confidence score per answer. |
| **Human review** | Flag low-confidence answers for human review. Show source control/policy for each answer. |
| **Export** | Export completed questionnaire in original format (Excel, PDF). |
| **Standard questionnaires** | Pre-built responses for SIG Lite, SIG Full, CAIQ, HECVAT, VSA. |
| **Response library** | Searchable library of approved responses. Reuse across questionnaires. |
| **Analytics** | Track questionnaires received, turnaround time, common questions. |

---

## 19. Trust Center

### 19.1 Features

| Feature | Description |
|---|---|
| **Public security page** | Customizable public page showing compliance posture, certifications, security practices. |
| **Compliance badges** | Display verified framework badges (SOC 2, ISO 27001, HIPAA, etc.). |
| **Document sharing** | Gated access to SOC 2 reports, penetration test summaries, policies. |
| **NDA workflow** | Require NDA acceptance before accessing sensitive documents. Track NDA signatures. |
| **FAQ** | Common security questions with answers pulled from knowledge base. |
| **Sub-processor list** | Public list of sub-processors (GDPR). |
| **Security updates** | Post security updates, incident notifications (if applicable). |
| **Custom branding** | Company logo, colors, domain (trust.yourcompany.com). |
| **Request access** | Prospects can request access to specific documents. Routed to security team for approval. |
| **Analytics** | Track page views, document downloads, NDA completions. |

---

## 20. Reporting & Dashboards

### 20.1 Dashboard Views

| Dashboard | Audience | Content |
|---|---|---|
| **Executive Overview** | C-suite, Board | Overall compliance score, top risks, audit timeline, trend |
| **Compliance Manager** | Compliance team | Framework-specific status, failing controls, upcoming tasks, evidence gaps |
| **Control Owner** | Department leads | Assigned controls, test results, remediation tasks |
| **Security Posture** | Security team | Vulnerability counts, scan results, incident metrics |
| **Audit Readiness** | Pre-audit | Per-framework readiness score, evidence completeness, gap list |
| **Vendor Risk** | Procurement/Security | Vendor risk scores, due diligence status, review schedule |

### 20.2 Reports

| Report | Format | Frequency |
|---|---|---|
| Board compliance report | PDF / PPTX | Quarterly |
| Framework compliance detail | PDF / CSV | On-demand |
| Risk register | PDF / CSV | Quarterly |
| Audit readiness | PDF | Pre-audit |
| Vendor risk summary | PDF | Quarterly |
| Pen test report | PDF | Per engagement |
| Access review summary | PDF / CSV | Per campaign |
| Incident summary | PDF | Monthly / Quarterly |
| Training completion | PDF / CSV | On-demand |
| Compliance trend | PDF | Monthly |

### 20.3 Report Generation

| Tool | License | Purpose |
|---|---|---|
| **Carbone** | Community (free) | Template-based document generation (DOCX, PDF, XLSX, PPTX from JSON data) |
| **Puppeteer** | Apache 2.0 | HTML-to-PDF for custom formatted reports |
| **React-PDF** | MIT | Programmatic PDF generation |
| **Apache ECharts** | Apache 2.0 | Charts and visualizations for dashboards |

---

## 21. SaaS Platform Features

### 21.1 Multi-Tenancy

| Feature | Description |
|---|---|
| **Tenant isolation** | Row-level security in PostgreSQL. Each tenant's data is isolated. |
| **Shared infrastructure** | All tenants share compute, with isolated data. Cost-efficient. |
| **Tenant-specific configs** | Each tenant has own: integrations, frameworks, controls, policies, users. |
| **Data residency** | Option to specify data region (US, EU, APAC) for regulated industries. |

### 21.2 Pricing Tiers (SaaS)

| Tier | Target | Included |
|---|---|---|
| **Free / Community** | Startups < 50 employees | 1 framework, 5 integrations, basic scanning, community support |
| **Pro** | Growing companies | Unlimited frameworks, unlimited integrations, all scanning, AI agents, email support |
| **Enterprise** | Large orgs | Everything in Pro + SSO/SAML, custom frameworks, SLA, dedicated support, data residency, audit API |

### 21.3 SaaS-Specific Features

| Feature | Description |
|---|---|
| **Onboarding wizard** | Guided setup: company profile → framework selection → integration connection → first scan |
| **Billing** | Stripe integration. Monthly/annual billing. Usage-based add-ons (pen test agent runs, extra storage). |
| **SSO/SAML** | Enterprise SSO via SAML 2.0 / OIDC. |
| **API access** | Full REST API with API key authentication. Rate limiting per tier. |
| **Webhooks** | Send events to customer systems (compliance change, alert, task created). |
| **White-labeling** | Enterprise tier: custom domain, logo, colors for trust center. |
| **Uptime SLA** | 99.9% for Pro, 99.95% for Enterprise. |
| **Data export** | Full data export in standard formats. No lock-in. |
| **Account deletion** | GDPR-compliant account and data deletion. |

### 21.4 Authentication & Identity

| Tool | License | Purpose |
|---|---|---|
| **Keycloak** | Apache 2.0 | Identity and access management. SSO, SAML, OIDC, MFA, user federation. |
| **Alternative: ZITADEL** | Apache 2.0 | Modern identity management. Better DX than Keycloak. OIDC-native. |

---

## 22. Technical Architecture

### 22.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │  Web App      │  │  Auditor     │  │  Trust Center │             │
│  │  (Next.js)    │  │  Portal      │  │  (Public)     │             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
│         │                  │                  │                      │
│  ┌──────▼──────────────────▼──────────────────▼───────┐            │
│  │              API Gateway (Kong / Traefik)           │            │
│  └──────────────────────┬─────────────────────────────┘            │
└─────────────────────────┼───────────────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────────────────┐
│                    APPLICATION LAYER                                 │
│  ┌──────────────────────▼─────────────────────────────┐            │
│  │              Core API (FastAPI / Python)             │            │
│  │                                                     │            │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐           │            │
│  │  │Framework │ │Controls  │ │Policy    │           │            │
│  │  │Service   │ │Service   │ │Service   │           │            │
│  │  └──────────┘ └──────────┘ └──────────┘           │            │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐           │            │
│  │  │Evidence  │ │Risk      │ │Audit     │           │            │
│  │  │Service   │ │Service   │ │Service   │           │            │
│  │  └──────────┘ └──────────┘ └──────────┘           │            │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐           │            │
│  │  │Vendor    │ │Training  │ │Report    │           │            │
│  │  │Service   │ │Service   │ │Service   │           │            │
│  │  └──────────┘ └──────────┘ └──────────┘           │            │
│  └─────────────────────────────────────────────────────┘            │
│                                                                      │
│  ┌─────────────────────────────────────────────────────┐            │
│  │              Agent Orchestration Layer               │            │
│  │                                                     │            │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐   │            │
│  │  │ LangGraph  │  │ CrewAI     │  │ LiteLLM    │   │            │
│  │  │ Workflows  │  │ Multi-Agent│  │ LLM Router │   │            │
│  │  └────────────┘  └────────────┘  └────────────┘   │            │
│  │                                                     │            │
│  │  ┌────────────────────────────────────────────────┐│            │
│  │  │ Agent Registry (10 agents — see Section 4)     ││            │
│  │  └────────────────────────────────────────────────┘│            │
│  └─────────────────────────────────────────────────────┘            │
│                                                                      │
│  ┌─────────────────────────────────────────────────────┐            │
│  │              Integration Hub                         │            │
│  │                                                     │            │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐   │            │
│  │  │ Cloud      │  │ SaaS       │  │ Security   │   │            │
│  │  │ Connectors │  │ Connectors │  │ Scanners   │   │            │
│  │  └────────────┘  └────────────┘  └────────────┘   │            │
│  └─────────────────────────────────────────────────────┘            │
│                                                                      │
│  ┌─────────────────────────────────────────────────────┐            │
│  │              Scanner Engine                          │            │
│  │                                                     │            │
│  │  Prowler │ Trivy │ Checkov │ Semgrep │ Nuclei │ ZAP│            │
│  │  TruffleHog │ OSV-Scanner │ Nmap │ Wazuh          │            │
│  └─────────────────────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────────────────┐
│                     DATA LAYER                                       │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ PostgreSQL   │  │ Redis        │  │ MinIO        │              │
│  │ + pgvector   │  │ (Cache +     │  │ (Evidence    │              │
│  │ (Primary DB) │  │  Queue)      │  │  Storage)    │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Meilisearch  │  │ Infisical    │  │ Temporal     │              │
│  │ (Search)     │  │ (Secrets)    │  │ (Workflows)  │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└──────────────────────────────────────────────────────────────────────┘
```

### 22.2 Technology Stack

#### Backend

| Component | Technology | License | Justification |
|---|---|---|---|
| **API Framework** | FastAPI (Python) | MIT | Async, fast, auto-docs, type-safe. Python ecosystem for AI/ML. |
| **ORM** | SQLAlchemy 2.0 + Alembic | MIT | Mature, async support, migration management |
| **Task Queue** | BullMQ (via Python bridge) or Celery | MIT / BSD | Background job processing |
| **Workflow Engine** | Temporal | Apache 2.0 | Durable workflows for long-running agent tasks |
| **API Gateway** | Traefik | MIT | Reverse proxy, load balancing, automatic TLS |

#### Frontend

| Component | Technology | License | Justification |
|---|---|---|---|
| **Framework** | Next.js 15 (App Router) | MIT | SSR, RSC, file-based routing, mature ecosystem |
| **UI Components** | shadcn/ui + Radix | MIT | Accessible, customizable, no vendor lock-in |
| **Styling** | Tailwind CSS 4 | MIT | Utility-first, consistent design |
| **Charts** | Apache ECharts or Recharts | Apache 2.0 / MIT | Rich chart library for dashboards |
| **Tables** | TanStack Table | MIT | Headless, sortable, filterable data tables |
| **Forms** | React Hook Form + Zod | MIT | Performant forms with schema validation |
| **State** | Zustand | MIT | Simple, lightweight state management |
| **Real-time** | Socket.io or Server-Sent Events | MIT | Live updates for monitoring dashboard |

#### Database & Storage

| Component | Technology | License | Justification |
|---|---|---|---|
| **Primary Database** | PostgreSQL 16 | PostgreSQL | Battle-tested, JSONB, RLS for multi-tenancy, pgvector for AI |
| **Vector Store** | pgvector extension | PostgreSQL | AI embeddings for semantic search (policies, controls, questionnaire matching) |
| **Cache** | Redis 7 | BSD | Session cache, rate limiting, pub/sub for real-time |
| **Object Storage** | MinIO | AGPLv3 | S3-compatible. Evidence files, reports, policy PDFs. |
| **Search Engine** | Meilisearch | MIT | Full-text search across controls, policies, evidence, risks |

#### AI / Agent Layer

| Component | Technology | License | Justification |
|---|---|---|---|
| **Agent Framework** | LangGraph | MIT | Complex stateful agent workflows |
| **Multi-Agent** | CrewAI | MIT | Multi-agent collaboration |
| **LLM Gateway** | LiteLLM | MIT | Unified API for any LLM provider. Switch models without code change. |
| **Embeddings** | sentence-transformers | Apache 2.0 | Local embedding generation for semantic search |
| **PDF Parsing** | Apache Tika / PyMuPDF | Apache 2.0 / AGPLv3 | Parse SOC 2 reports, questionnaires, policies |

#### DevOps & Infrastructure

| Component | Technology | License | Justification |
|---|---|---|---|
| **Containers** | Docker | Apache 2.0 | Containerization for all services |
| **Orchestration** | Docker Compose (simple) / Kubernetes (scale) | Apache 2.0 | Deployment orchestration |
| **CI/CD** | GitHub Actions | Free for OSS | Automated testing, building, deployment |
| **Monitoring** | Prometheus + Grafana | Apache 2.0 / AGPLv3 | Platform health monitoring |
| **Logging** | Loki + Grafana | AGPLv3 | Centralized logging |
| **Reverse Proxy** | Traefik | MIT | Ingress, TLS termination, routing |

### 22.3 API Design

- **REST API** with OpenAPI 3.1 specification (auto-generated by FastAPI)
- **Versioned**: `/api/v1/...`
- **Authentication**: JWT tokens (short-lived) + refresh tokens. API keys for service accounts.
- **Authorization**: RBAC with row-level security. Permissions checked at API layer and DB layer.
- **Rate limiting**: Per-tenant, per-endpoint. Configurable per tier.
- **Pagination**: Cursor-based for large collections.
- **Webhooks**: Outbound webhooks for events (compliance change, alert, task).
- **Bulk operations**: Batch endpoints for bulk updates.
- **Idempotency**: Idempotency keys for write operations.

---

## 23. Open Source Tool Registry

Complete list of all open-source tools used by the platform:

### 23.1 Cloud Security & CSPM

| Tool | License | Category | URL |
|---|---|---|---|
| Prowler | Apache 2.0 | Cloud Security Assessment | github.com/prowler-cloud/prowler |
| ScoutSuite | GPL 2.0 | Multi-Cloud Audit | github.com/nccgroup/ScoutSuite |
| CloudSploit | GPL 2.0 | Cloud Security Monitoring | github.com/aquasecurity/cloudsploit |
| Steampipe | AGPLv3 | Cloud SQL Queries | github.com/turbot/steampipe |

### 23.2 IaC Security

| Tool | License | Category | URL |
|---|---|---|---|
| Checkov | Apache 2.0 | IaC Static Analysis | github.com/bridgecrewio/checkov |
| tfsec | MIT | Terraform Security | github.com/aquasecurity/tfsec |
| KICS | Apache 2.0 | IaC Security | github.com/Checkmarx/kics |
| Terrascan | Apache 2.0 | IaC Compliance | github.com/tenable/terrascan |

### 23.3 Container & Image Security

| Tool | License | Category | URL |
|---|---|---|---|
| Trivy | Apache 2.0 | Vulnerability Scanner | github.com/aquasecurity/trivy |
| Grype | Apache 2.0 | Image Vulnerability | github.com/anchore/grype |
| Syft | Apache 2.0 | SBOM Generator | github.com/anchore/syft |
| Clair | Apache 2.0 | Container Vulnerability | github.com/quay/clair |
| Falco | Apache 2.0 | Runtime Security | github.com/falcosecurity/falco |

### 23.4 Secret Detection

| Tool | License | Category | URL |
|---|---|---|---|
| TruffleHog | AGPLv3 | Secret Scanning | github.com/trufflesecurity/trufflehog |
| Gitleaks | MIT | Git Secret Scanning | github.com/gitleaks/gitleaks |
| detect-secrets | Apache 2.0 | Secret Prevention | github.com/Yelp/detect-secrets |

### 23.5 SAST & SCA

| Tool | License | Category | URL |
|---|---|---|---|
| Semgrep | LGPL 2.1 | Static Analysis | github.com/semgrep/semgrep |
| SonarQube CE | LGPL 3.0 | Code Quality + Security | github.com/SonarSource/sonarqube |
| OSV-Scanner | Apache 2.0 | Dependency Vulnerability | github.com/google/osv-scanner |
| OWASP Dep-Check | Apache 2.0 | Dependency Vulnerability | github.com/jeremylong/DependencyCheck |

### 23.6 SIEM & Monitoring

| Tool | License | Category | URL |
|---|---|---|---|
| Wazuh | GPL 2.0 | SIEM + HIDS | github.com/wazuh/wazuh |
| Suricata | GPL 2.0 | Network IDS/IPS | github.com/OISF/suricata |
| Prometheus | Apache 2.0 | Metrics | github.com/prometheus/prometheus |
| Grafana | AGPLv3 | Visualization | github.com/grafana/grafana |
| Loki | AGPLv3 | Log Aggregation | github.com/grafana/loki |
| Uptime Kuma | MIT | Uptime Monitoring | github.com/louislam/uptime-kuma |

### 23.7 Penetration Testing

| Tool | License | Category | URL |
|---|---|---|---|
| Nmap | Custom OSS | Network Scanner | nmap.org |
| RustScan | GPL 3.0 | Fast Port Scanner | github.com/RustScan/RustScan |
| Masscan | AGPLv3 | Mass Port Scanner | github.com/robertdavidgraham/masscan |
| Subfinder | MIT | Subdomain Discovery | github.com/projectdiscovery/subfinder |
| Amass | Apache 2.0 | Attack Surface Mapping | github.com/owasp-amass/amass |
| httpx | MIT | HTTP Probing | github.com/projectdiscovery/httpx |
| Katana | MIT | Web Crawling | github.com/projectdiscovery/katana |
| OWASP ZAP | Apache 2.0 | Web App Scanner | github.com/zaproxy/zaproxy |
| Nuclei | MIT | Template Scanner | github.com/projectdiscovery/nuclei |
| Nikto | GPL | Web Server Scanner | github.com/sullo/nikto |
| ffuf | MIT | Web Fuzzer | github.com/ffuf/ffuf |
| Gobuster | Apache 2.0 | Dir Brute Force | github.com/OJ/gobuster |
| SQLMap | GPL 2.0 | SQL Injection | github.com/sqlmapproject/sqlmap |
| Metasploit | BSD | Exploitation Framework | github.com/rapid7/metasploit-framework |
| Pacu | BSD | AWS Exploitation | github.com/RhinoSecurityLabs/pacu |
| CloudFox | MIT | Cloud Pen Testing | github.com/BishopFox/cloudfox |
| Hydra | GPL 3.0 | Password Testing | github.com/vanhauser-thc/thc-hydra |

### 23.8 Phishing Simulation

| Tool | License | Category | URL |
|---|---|---|---|
| GoPhish | MIT | Phishing Simulation | github.com/gophish/gophish |

### 23.9 Identity & Auth

| Tool | License | Category | URL |
|---|---|---|---|
| Keycloak | Apache 2.0 | IAM / SSO | github.com/keycloak/keycloak |
| ZITADEL | Apache 2.0 | Identity Management | github.com/zitadel/zitadel |

### 23.10 Secrets Management

| Tool | License | Category | URL |
|---|---|---|---|
| Infisical | MIT (core) | Secret Management | github.com/Infisical/infisical |
| SOPS | MPL 2.0 | Encrypted Secrets | github.com/getsops/sops |

### 23.11 Data & Storage

| Tool | License | Category | URL |
|---|---|---|---|
| PostgreSQL | PostgreSQL | Primary Database | postgresql.org |
| pgvector | PostgreSQL | Vector Search | github.com/pgvector/pgvector |
| Redis | BSD | Cache / Queue | github.com/redis/redis |
| MinIO | AGPLv3 | Object Storage | github.com/minio/minio |
| Meilisearch | MIT | Search Engine | github.com/meilisearch/meilisearch |

### 23.12 Workflow & Orchestration

| Tool | License | Category | URL |
|---|---|---|---|
| Temporal | Apache 2.0 | Workflow Engine | github.com/temporalio/temporal |
| BullMQ | MIT | Job Queue | github.com/taskforcesh/bullmq |

### 23.13 AI & Agent Frameworks

| Tool | License | Category | URL |
|---|---|---|---|
| LangGraph | MIT | Agent Workflows | github.com/langchain-ai/langgraph |
| CrewAI | MIT | Multi-Agent | github.com/crewAIInc/crewAI |
| LiteLLM | MIT | LLM Gateway | github.com/BerriAI/litellm |
| sentence-transformers | Apache 2.0 | Embeddings | github.com/UKPLab/sentence-transformers |
| Apache Tika | Apache 2.0 | Document Parsing | tika.apache.org |

### 23.14 Frontend

| Tool | License | Category | URL |
|---|---|---|---|
| Next.js | MIT | React Framework | github.com/vercel/next.js |
| shadcn/ui | MIT | UI Components | github.com/shadcn-ui/ui |
| Tailwind CSS | MIT | CSS Framework | github.com/tailwindlabs/tailwindcss |
| Apache ECharts | Apache 2.0 | Charts | github.com/apache/echarts |
| TanStack Table | MIT | Data Tables | github.com/TanStack/table |

### 23.15 Infrastructure

| Tool | License | Category | URL |
|---|---|---|---|
| Docker | Apache 2.0 | Containerization | docker.com |
| Traefik | MIT | Reverse Proxy | github.com/traefik/traefik |
| Playwright | Apache 2.0 | Browser Automation | github.com/microsoft/playwright |

### 23.16 Policy as Code

| Tool | License | Category | URL |
|---|---|---|---|
| Open Policy Agent | Apache 2.0 | Policy Engine | github.com/open-policy-agent/opa |
| InSpec | Apache 2.0 | Infrastructure Testing | github.com/inspec/inspec |

---

## 24. Data Model

### 24.1 Core Entities

```
Organization
├── id, name, industry, size, cloud_providers[], tech_stack{}
├── subscription_tier, billing_info
└── settings{}

Framework
├── id, name, version, category
├── domains[] → Domain
│   └── requirements[] → Requirement
│       └── control_objectives[] → ControlObjective
└── cross_framework_mappings[]

ControlTemplate (Library)
├── id, title, domain, description
├── implementation_guidance
├── test_procedure
├── evidence_template_id
├── automation_level (full | partial | manual)
├── applicable_frameworks[] (framework + requirement ref)
└── integration_tests[]

Control (Org-specific, instantiated from template)
├── id, org_id, template_id
├── title, description, implementation_details
├── owner_id (User)
├── status (implemented | partially_implemented | not_implemented | not_applicable)
├── effectiveness (effective | needs_improvement | ineffective)
├── frameworks[] (which frameworks this control satisfies)
├── last_test_date, last_test_result
└── exceptions[]

EvidenceTemplate (Library)
├── id, title, evidence_type, format
├── collection_method, refresh_frequency
├── fields[], pass_criteria{}
└── integrations[]

Evidence (Collected)
├── id, org_id, control_id, template_id
├── collected_at, expires_at
├── status (pass | fail | error | pending)
├── artifact_url (MinIO path)
├── artifact_hash (SHA-256)
├── data{} (structured evidence data)
└── collection_method, collector (agent | manual)

Policy
├── id, org_id, template_id
├── title, content (markdown), version
├── status (draft | in_review | approved | published | archived)
├── owner_id, reviewer_ids[]
├── approved_at, next_review_date
├── acknowledgments[] → PolicyAcknowledgment
└── controls[] (which controls this policy covers)

Risk
├── id, org_id
├── title, description, category
├── likelihood (1-5), impact (1-5)
├── inherent_score, residual_score
├── treatment (mitigate | accept | transfer | avoid)
├── treatment_plan, treatment_status
├── owner_id
├── controls[] (mitigating controls)
└── assets[] (affected assets)

Vendor
├── id, org_id
├── name, category, risk_tier (critical | high | medium | low)
├── data_access_level, business_criticality
├── security_score
├── soc2_report_url, certifications[]
├── contract_expiry, last_review_date
└── questionnaire_responses[]

Audit
├── id, org_id, framework_id
├── type (type_1 | type_2 | internal | certification)
├── period_start, period_end
├── status (planning | fieldwork | reporting | complete)
├── auditor_id (User with auditor role)
├── readiness_score
├── findings[] → Finding
└── workpapers[]

Finding
├── id, audit_id
├── control_id, severity
├── description, recommendation
├── management_response
├── remediation_status (open | in_progress | resolved)
└── resolved_at

User
├── id, org_id, email, name
├── role (super_admin | compliance_manager | control_owner | employee | auditor)
├── department, manager_id
├── training_assignments[]
└── policy_acknowledgments[]

Auditor (extends User for auditor marketplace)
├── firm_name, credentials[]
├── specializations[] (frameworks)
├── geography, verified (boolean)
├── profile_url, rating
└── engagements[]

Integration
├── id, org_id
├── type (aws | github | okta | etc.)
├── status (connected | error | disconnected)
├── credentials_ref (Infisical path)
├── last_sync, sync_frequency
└── configuration{}

ScanResult
├── id, org_id, scanner (prowler | trivy | nuclei | etc.)
├── scan_type, started_at, completed_at
├── findings_count{critical, high, medium, low, info}
├── findings[] → ScanFinding
└── evidence_id (linked evidence artifact)

Incident
├── id, org_id
├── title, description, severity (P1-P4)
├── status (open | investigating | contained | resolved | closed)
├── detected_at, resolved_at
├── playbook_id
├── timeline[] → IncidentEvent
├── post_mortem{}
└── notification_status{}

Task
├── id, org_id
├── type (remediation | review | training | evidence_request)
├── title, description
├── assignee_id, due_date
├── status (pending | in_progress | completed | overdue)
├── related_entity (control_id | risk_id | finding_id)
└── priority (critical | high | medium | low)

AgentRun
├── id, org_id, agent_type
├── trigger (scheduled | manual | event)
├── started_at, completed_at
├── status (running | completed | failed)
├── input{}, output{}
├── actions_taken[]
└── tokens_used, cost
```

### 24.2 Audit Trail Table (Append-Only)

```
AuditLog
├── id (ULID, sortable)
├── org_id
├── actor_type (user | agent | system)
├── actor_id
├── action (created | updated | deleted | viewed | approved | rejected)
├── entity_type, entity_id
├── changes{} (before/after diff)
├── ip_address, user_agent
└── timestamp (immutable)
```

---

## 25. Deployment

### 25.1 Self-Hosted: Docker Compose

```yaml
# docker-compose.yml (simplified)
services:
  # Core
  api:          # FastAPI backend
  web:          # Next.js frontend
  worker:       # Celery/BullMQ workers

  # Data
  postgres:     # PostgreSQL 16 + pgvector
  redis:        # Redis 7
  minio:        # MinIO object storage
  meilisearch:  # Full-text search

  # Orchestration
  temporal:     # Workflow engine
  temporal-ui:  # Temporal dashboard

  # Auth
  keycloak:     # Identity management

  # Secrets
  infisical:    # Secret management

  # Monitoring
  prometheus:   # Metrics
  grafana:      # Dashboards
  loki:         # Logs

  # Reverse Proxy
  traefik:      # Ingress + TLS

  # Security Scanners (optional, on-demand)
  prowler:      # Cloud security
  trivy:        # Container/dependency scanning
  wazuh:        # SIEM

  # Pen Test (optional, on-demand)
  pentest-agent: # Container with pen test toolchain
```

### 25.2 Self-Hosted: Kubernetes

- Helm chart for production deployment
- Horizontal pod autoscaling for API and workers
- PersistentVolumeClaims for data services
- Ingress via Traefik
- Secrets via external-secrets-operator + Infisical

### 25.3 SaaS Deployment

- Kubernetes on AWS EKS (primary) or GCP GKE
- RDS PostgreSQL (multi-AZ)
- ElastiCache Redis
- S3 for evidence storage (MinIO compatibility)
- CloudFront CDN for frontend
- GitHub Actions for CI/CD
- Terraform for infrastructure management

### 25.4 System Requirements (Self-Hosted)

| Component | Minimum | Recommended |
|---|---|---|
| CPU | 4 cores | 8+ cores |
| RAM | 16 GB | 32+ GB |
| Storage | 100 GB SSD | 500+ GB SSD |
| Network | 100 Mbps | 1 Gbps |
| OS | Linux (Ubuntu 22.04+, Debian 12+) | Linux |

---

## 26. Roadmap & Phasing

### Phase 1: Foundation (Months 1-3)

- [ ] Project scaffolding (monorepo, CI/CD, Docker Compose)
- [ ] PostgreSQL schema + migrations
- [ ] Authentication (Keycloak/ZITADEL integration)
- [ ] Core API: organizations, users, RBAC
- [ ] Framework engine: load SOC 2, ISO 27001 frameworks
- [ ] Control template library (first 50 templates)
- [ ] Evidence template library (first 50 templates)
- [ ] Policy template library (first 10 policies)
- [ ] Basic web UI: dashboard, frameworks, controls list
- [ ] First AI agent: Controls Generation Agent
- [ ] First AI agent: Policy Generation Agent
- [ ] MinIO integration for evidence storage

### Phase 2: Integration & Collection (Months 3-5)

- [ ] Integration hub architecture (plugin system)
- [ ] First 10 connectors: AWS, GCP, Azure, GitHub, Okta, Google Workspace, Slack, Jira, Azure AD, CrowdStrike
- [ ] Evidence Collection Agent
- [ ] Automated evidence collection on schedule
- [ ] Prowler integration (cloud security scanning)
- [ ] Trivy integration (container/dependency scanning)
- [ ] Continuous Monitoring Agent (basic)
- [ ] Dashboard: compliance score, evidence freshness
- [ ] Control testing automation

### Phase 3: Risk & Audit (Months 5-7)

- [ ] Risk management module (register, scoring, treatment)
- [ ] Risk Assessment Agent
- [ ] Audit management module
- [ ] Auditor registration system
- [ ] Auditor portal (read-only evidence view)
- [ ] Audit Preparation Agent
- [ ] Finding tracking and remediation
- [ ] Access review module
- [ ] Vendor risk management (basic)
- [ ] Expand control templates to 200+

### Phase 4: Security Scanning & Pen Testing (Months 7-9)

- [ ] Scanner orchestration engine
- [ ] Checkov, Semgrep, TruffleHog, Gitleaks, OSV-Scanner integration
- [ ] Wazuh integration (SIEM)
- [ ] Penetration Testing Orchestrator Agent
- [ ] Nuclei, ZAP, Nmap, Subfinder integration
- [ ] Pen test report generation
- [ ] Remediation Agent (auto-fix with approval)
- [ ] Scan result → evidence mapping

### Phase 5: SaaS & Polish (Months 9-11)

- [ ] Multi-tenancy (row-level security)
- [ ] SaaS onboarding wizard
- [ ] Billing integration (Stripe)
- [ ] Trust Center module
- [ ] Security Questionnaire Agent
- [ ] Training & awareness module (GoPhish integration)
- [ ] Reporting engine (Carbone templates)
- [ ] Board-ready report generation
- [ ] Additional connectors (20+ total)
- [ ] API documentation and developer portal

### Phase 6: Scale & Community (Months 11-13)

- [ ] Kubernetes Helm chart
- [ ] Performance optimization and load testing
- [ ] Plugin SDK for community connectors
- [ ] Auditor marketplace features
- [ ] Advanced vendor risk (SOC 2 report parsing)
- [ ] Custom framework builder
- [ ] White-labeling for enterprise
- [ ] Community contribution guidelines
- [ ] Documentation site
- [ ] Launch: ProductHunt, HackerNews, Reddit

---

## Appendix A: Competitive Analysis

| Feature | Vanta | Drata | Sprinto | **OpenComply** |
|---|---|---|---|---|
| Open source | No | No | No | **Yes (AGPLv3)** |
| Self-hosted | No | No | No | **Yes** |
| AI agents | Basic | Basic | Basic | **10 specialized agents** |
| Auto-remediation | Limited | Limited | No | **Yes (with approval)** |
| Pen testing | No | No | No | **Built-in (open source tools)** |
| Policy generation | Templates | Templates | Templates | **AI-generated from context** |
| Controls auto-generation | No | No | No | **Template library + AI** |
| Auditor marketplace | No | No | No | **Yes** |
| Pricing | $20k+/yr | $15k+/yr | $10k+/yr | **Free (self-hosted) / Freemium (SaaS)** |
| Vendor lock-in | High | High | High | **None** |
| Integration count | 200+ | 100+ | 100+ | **Community-driven, unlimited** |
| Cloud security scanning | Via integrations | Via integrations | Via integrations | **Built-in (Prowler, Trivy, etc.)** |
| Questionnaire automation | Yes | Yes | Yes | **AI-powered with knowledge base** |
| Trust center | Yes | Yes | Yes | **Yes** |

## Appendix B: License Compatibility Notes

The platform uses AGPLv3 as its license. All included open-source tools have been selected for license compatibility:

| License | Compatible | Notes |
|---|---|---|
| MIT | Yes | Permissive, fully compatible |
| Apache 2.0 | Yes | Permissive, compatible with AGPLv3 |
| BSD | Yes | Permissive, fully compatible |
| GPL 2.0 | Yes | Copyleft, compatible when tools run as separate processes |
| GPL 3.0 | Yes | Copyleft, compatible with AGPLv3 |
| AGPLv3 | Yes | Same license family |
| LGPL | Yes | Library exception allows linking |
| MPL 2.0 | Yes | File-level copyleft, compatible |
| PostgreSQL License | Yes | Permissive, similar to BSD |
| Custom OSS (Nmap) | Yes | Separate process, not linked |

**Note**: Tools that have changed to non-OSS licenses (e.g., HashiCorp Vault → BUSL) have been replaced with fully open-source alternatives (Infisical).
