# QuickTrust — Open Source Integrations Roadmap

A comprehensive list of all open source integrations needed for the QuickTrust GRC platform, organized by category and priority.

---

## Already Integrated (Current Stack)

These open source projects are already in use:

| Category | Tool | License | Purpose |
|----------|------|---------|---------|
| API Framework | FastAPI | MIT | REST API backend |
| ORM | SQLAlchemy 2.0 (async) | MIT | Database abstraction |
| Migrations | Alembic | MIT | Schema versioning |
| AI Agents | LangGraph | MIT | Stateful multi-step agent workflows |
| LLM Gateway | LiteLLM | MIT | Unified LLM provider routing |
| Embeddings | sentence-transformers | Apache 2.0 | Semantic search / vector embeddings |
| PDF Generation | ReportLab | BSD | PDF report rendering |
| Scheduling | APScheduler | MIT | Periodic monitoring jobs |
| HTTP Client | httpx | BSD | Async HTTP requests |
| JWT | python-jose | MIT | Token handling |
| AWS SDK | boto3 | Apache 2.0 | AWS service integration |
| Frontend | Next.js 15 | MIT | React framework (SSR) |
| UI Library | React 19 | MIT | Component-based UI |
| Styling | Tailwind CSS 4 | MIT | Utility-first CSS |
| Components | Radix UI (shadcn/ui) | MIT | Accessible headless components |
| Data Fetching | TanStack Query | MIT | Server state management |
| Tables | TanStack React Table | MIT | Advanced data tables |
| Charts | Recharts | MIT | Data visualization |
| Icons | lucide-react | ISC | Icon library |
| Theme | next-themes | MIT | Dark/light mode |
| Database | PostgreSQL 16 + pgvector | PostgreSQL / BSD | Relational DB + vector search |
| Cache | Redis 7 | BSD | Caching and session store |
| Object Storage | MinIO | AGPLv3 | S3-compatible file storage |
| Auth Server | Keycloak 26 | Apache 2.0 | OIDC/SAML identity provider |
| Reverse Proxy | Traefik v3.2 | MIT | API gateway / load balancer |
| Containers | Docker Compose | Apache 2.0 | Multi-service orchestration |
| Linting | Ruff | MIT | Python linting + formatting |
| Testing | pytest | MIT | Python test framework |
| Pre-commit | pre-commit | MIT | Git hook management |
| Security Scan | Safety | MIT | Python dependency vulnerability scanning |

---

## HIGH PRIORITY — Security Scanning & Vulnerability Management

### 1. Trivy
- **Source:** https://github.com/aquasecurity/trivy
- **License:** Apache 2.0
- **Purpose:** Container image, filesystem, and dependency vulnerability scanning
- **Integration Point:** CI/CD pipeline + evidence collection for security controls
- **Why:** Auto-generate vulnerability scan evidence for SOC 2, ISO 27001, PCI DSS

### 2. OWASP ZAP (Zed Attack Proxy)
- **Source:** https://github.com/zaproxy/zaproxy
- **License:** Apache 2.0
- **Purpose:** Dynamic Application Security Testing (DAST)
- **Integration Point:** Pentest agent orchestration, scheduled security scans
- **Why:** Automated web app vulnerability scanning tied to compliance controls

### 3. Grype
- **Source:** https://github.com/anchore/grype
- **License:** Apache 2.0
- **Purpose:** Software composition analysis (SCA) — vulnerability scanner for container images and filesystems
- **Integration Point:** CI/CD pipeline, evidence collection
- **Why:** Complementary to Trivy; maps CVEs to compliance requirements

### 4. Semgrep
- **Source:** https://github.com/semgrep/semgrep
- **License:** LGPL 2.1
- **Purpose:** Static Application Security Testing (SAST) — code pattern matching for security bugs
- **Integration Point:** CI/CD pipeline, pre-commit hooks
- **Why:** Catches OWASP Top 10 vulnerabilities in source code; generates evidence for secure development controls

### 5. Nuclei
- **Source:** https://github.com/projectdiscovery/nuclei
- **License:** MIT
- **Purpose:** Template-based vulnerability scanner for web apps, APIs, networks
- **Integration Point:** Pentest agent, scheduled scanning
- **Why:** Community-driven vulnerability templates; ideal for recurring compliance scans

---

## HIGH PRIORITY — Cloud Security & Configuration Monitoring

### 6. CloudSploit
- **Source:** https://github.com/aquasecurity/cloudsploit
- **License:** GPL 2.0
- **Purpose:** Cloud security configuration scanning (AWS, Azure, GCP, Oracle)
- **Integration Point:** Integration connectors, monitoring rules
- **Why:** Automated cloud misconfiguration detection mapped to CIS Benchmarks, SOC 2, HIPAA

### 7. ScoutSuite
- **Source:** https://github.com/nccgroup/ScoutSuite
- **License:** GPL 3.0
- **Purpose:** Multi-cloud security auditing (AWS, Azure, GCP, Alibaba, Oracle)
- **Integration Point:** Evidence collection, gap analysis
- **Why:** Generates comprehensive cloud security posture reports

### 8. Prowler
- **Source:** https://github.com/prowler-cloud/prowler
- **License:** Apache 2.0
- **Purpose:** AWS/Azure/GCP security assessment tool aligned to CIS, NIST, PCI, HIPAA
- **Integration Point:** Integration connectors, scheduled scans, evidence collection
- **Why:** Maps directly to compliance frameworks; generates audit-ready evidence

### 9. Checkov
- **Source:** https://github.com/bridgecrewio/checkov
- **License:** Apache 2.0
- **Purpose:** Infrastructure-as-Code (IaC) static analysis for Terraform, CloudFormation, Kubernetes, Helm
- **Integration Point:** CI/CD pipeline, pre-deployment compliance checks
- **Why:** Prevents non-compliant infrastructure from being deployed

---

## HIGH PRIORITY — Observability & Monitoring

### 10. Prometheus
- **Source:** https://github.com/prometheus/prometheus
- **License:** Apache 2.0
- **Purpose:** Metrics collection and alerting
- **Integration Point:** Platform health monitoring, SLA tracking, compliance metrics
- **Why:** Foundation for operational observability; required for SOC 2 availability criteria

### 11. Grafana
- **Source:** https://github.com/grafana/grafana
- **License:** AGPLv3
- **Purpose:** Metrics visualization and dashboarding
- **Integration Point:** Executive compliance dashboards, operational monitoring
- **Why:** Rich visual dashboards for compliance posture, risk trends, control health

### 12. OpenTelemetry
- **Source:** https://github.com/open-telemetry/opentelemetry-python
- **License:** Apache 2.0
- **Purpose:** Distributed tracing, metrics, and logging (vendor-neutral)
- **Integration Point:** FastAPI instrumentation, agent execution tracing
- **Why:** End-to-end request tracing for debugging and audit trails

### 13. Uptime Kuma
- **Source:** https://github.com/louislam/uptime-kuma
- **License:** MIT
- **Purpose:** Self-hosted uptime monitoring with status pages
- **Integration Point:** Trust Center, availability SLA tracking
- **Why:** Public status page for trust center; evidence for availability controls

### 14. Sentry (self-hosted)
- **Source:** https://github.com/getsentry/sentry
- **License:** FSL (functional source license)
- **Purpose:** Error tracking and performance monitoring
- **Integration Point:** Backend + frontend error capture, incident auto-creation
- **Why:** Automated error detection feeds into incident management workflow

---

## HIGH PRIORITY — Runtime Security & SIEM

### 15. Falco
- **Source:** https://github.com/falcosecurity/falco
- **License:** Apache 2.0
- **Purpose:** Runtime security and threat detection for containers/Kubernetes
- **Integration Point:** Monitoring daemon agent, alert ingestion
- **Why:** Real-time container anomaly detection; evidence for runtime security controls

### 16. Wazuh
- **Source:** https://github.com/wazuh/wazuh
- **License:** GPL 2.0
- **Purpose:** SIEM, host-based intrusion detection (HIDS), log analysis, compliance checking
- **Integration Point:** Log aggregation, security event correlation, compliance reporting
- **Why:** Full SIEM capability; maps findings to SOC 2, PCI DSS, HIPAA, GDPR controls

### 17. OSSEC
- **Source:** https://github.com/ossec/ossec-hids
- **License:** GPL 2.0
- **Purpose:** Host-based intrusion detection system
- **Integration Point:** Server monitoring, file integrity monitoring
- **Why:** File integrity monitoring evidence for SOC 2 and PCI DSS compliance

---

## MEDIUM PRIORITY — Task Queue & Background Processing

### 18. Celery
- **Source:** https://github.com/celery/celery
- **License:** BSD
- **Purpose:** Distributed task queue for background job processing
- **Integration Point:** Replace asyncio.create_task() for agent runs, report generation, evidence collection
- **Why:** Production-grade job durability, retries, rate limiting, scheduling

### 19. RabbitMQ
- **Source:** https://github.com/rabbitmq/rabbitmq-server
- **License:** MPL 2.0
- **Purpose:** Message broker for Celery (alternative to Redis broker)
- **Integration Point:** Celery broker backend
- **Why:** Reliable message delivery, dead-letter queues for failed agent jobs

---

## MEDIUM PRIORITY — Incident Response & Ticketing Integration

### 20. n8n
- **Source:** https://github.com/n8n-io/n8n
- **License:** Sustainable Use License
- **Purpose:** Workflow automation (self-hosted Zapier alternative)
- **Integration Point:** Incident response automation, cross-tool orchestration
- **Why:** Connect QuickTrust events to Slack, Jira, PagerDuty, email, and 400+ services

### 21. Gitea
- **Source:** https://github.com/go-gitea/gitea
- **License:** MIT
- **Purpose:** Self-hosted Git service
- **Integration Point:** Alternative to GitHub for evidence collection (self-hosted environments)
- **Why:** Organizations using self-hosted Git need integration parity with GitHub

---

## MEDIUM PRIORITY — Documentation & Knowledge Base

### 22. MkDocs + Material Theme
- **Source:** https://github.com/squidfunk/mkdocs-material
- **License:** MIT
- **Purpose:** Auto-generated documentation site from Markdown
- **Integration Point:** API documentation, control library, policy templates
- **Why:** Always-in-sync documentation; shareable compliance knowledge base

### 23. Docusaurus
- **Source:** https://github.com/facebook/docusaurus
- **License:** MIT
- **Purpose:** Documentation website framework
- **Integration Point:** Community-facing docs, control template library, integration guides
- **Why:** Community contribution portal for control templates and framework mappings

---

## MEDIUM PRIORITY — Advanced Testing

### 24. pytest-cov
- **Source:** https://github.com/pytest-dev/pytest-cov
- **License:** MIT
- **Purpose:** Test coverage reporting
- **Integration Point:** CI/CD pipeline, quality gates
- **Why:** Coverage metrics as evidence for SDLC compliance controls

### 25. pytest-xdist
- **Source:** https://github.com/pytest-dev/pytest-xdist
- **License:** MIT
- **Purpose:** Parallel test execution
- **Integration Point:** CI/CD pipeline
- **Why:** Faster CI runs as test suite grows

### 26. Hypothesis
- **Source:** https://github.com/HypothesisWorks/hypothesis
- **License:** MPL 2.0
- **Purpose:** Property-based testing
- **Integration Point:** Agent input validation, edge case testing
- **Why:** Discover edge cases in compliance rule logic

### 27. Playwright
- **Source:** https://github.com/microsoft/playwright
- **License:** Apache 2.0
- **Purpose:** End-to-end browser testing
- **Integration Point:** Frontend UI testing, workflow validation
- **Why:** Ensure compliance workflows work correctly end-to-end

---

## MEDIUM PRIORITY — Data Quality & Validation

### 28. Great Expectations
- **Source:** https://github.com/great-expectations/great_expectations
- **License:** Apache 2.0
- **Purpose:** Data quality validation and profiling
- **Integration Point:** Evidence data validation, audit trail integrity checks
- **Why:** Ensure collected evidence meets quality standards before audit

### 29. Pandera
- **Source:** https://github.com/unionai-contrib/pandera
- **License:** MIT
- **Purpose:** Data validation for pandas DataFrames
- **Integration Point:** Report data pipelines, bulk import validation
- **Why:** Lightweight data validation for compliance data imports

---

## MEDIUM PRIORITY — Secrets Management

### 30. HashiCorp Vault
- **Source:** https://github.com/hashicorp/vault
- **License:** BSL 1.1 (source-available)
- **Purpose:** Secrets management, encryption-as-a-service, PKI
- **Integration Point:** Integration credentials, API keys, database passwords
- **Why:** Enterprise-grade secret rotation; evidence for access control compliance

### 31. Mozilla SOPS
- **Source:** https://github.com/getsentry/sops
- **License:** MPL 2.0
- **Purpose:** Encrypted secrets in version control
- **Integration Point:** Config file encryption, CI/CD secrets
- **Why:** Secure secret storage for GitOps workflows

---

## LOWER PRIORITY — Kubernetes & Deployment

### 32. Helm
- **Source:** https://github.com/helm/helm
- **License:** Apache 2.0
- **Purpose:** Kubernetes package manager
- **Integration Point:** QuickTrust Helm chart for K8s deployment
- **Why:** Standard enterprise deployment method; enables marketplace distribution

### 33. Argo CD
- **Source:** https://github.com/argoproj/argo-cd
- **License:** Apache 2.0
- **Purpose:** GitOps continuous delivery for Kubernetes
- **Integration Point:** Declarative deployment management
- **Why:** Auditable deployment pipeline with drift detection

### 34. cert-manager
- **Source:** https://github.com/cert-manager/cert-manager
- **License:** Apache 2.0
- **Purpose:** Automated TLS certificate management for Kubernetes
- **Integration Point:** SSL/TLS certificate lifecycle
- **Why:** Evidence for encryption-in-transit compliance controls

### 35. Kyverno
- **Source:** https://github.com/kyverno/kyverno
- **License:** Apache 2.0
- **Purpose:** Kubernetes policy engine
- **Integration Point:** Cluster compliance enforcement
- **Why:** Enforce security policies at the K8s level; evidence for infrastructure controls

---

## LOWER PRIORITY — Compliance-Specific Tools

### 36. OpenSCAP
- **Source:** https://github.com/OpenSCAP/openscap
- **License:** LGPL 2.1
- **Purpose:** Security Content Automation Protocol (SCAP) scanning
- **Integration Point:** Compliance scanning, NIST/CIS benchmark validation
- **Why:** Standards-based compliance assessment for government frameworks (FedRAMP, CMMC)

### 37. InSpec
- **Source:** https://github.com/inspec/inspec
- **License:** Apache 2.0
- **Purpose:** Compliance-as-code testing framework
- **Integration Point:** Infrastructure compliance tests, evidence collection
- **Why:** Write compliance checks as code; continuous compliance validation

### 38. OpenControl
- **Source:** https://github.com/opencontrol
- **License:** CC0 / Public Domain
- **Purpose:** Machine-readable compliance documentation standard
- **Integration Point:** Control definitions, framework mapping import/export
- **Why:** Interoperability with other GRC tools; community control libraries

---

## LOWER PRIORITY — Machine Learning & AI

### 39. scikit-learn
- **Source:** https://github.com/scikit-learn/scikit-learn
- **License:** BSD
- **Purpose:** Machine learning library
- **Integration Point:** Anomaly detection in access logs, risk scoring models
- **Why:** ML-powered risk detection and user behavior analytics

### 40. PyOD
- **Source:** https://github.com/yzhao062/pyod
- **License:** BSD
- **Purpose:** Outlier detection library
- **Integration Point:** Anomalous activity detection in monitoring data
- **Why:** Specialized anomaly detection for compliance monitoring events

---

## LOWER PRIORITY — Log Management

### 41. Loki
- **Source:** https://github.com/grafana/loki
- **License:** AGPLv3
- **Purpose:** Log aggregation system (works with Grafana)
- **Integration Point:** Centralized log collection, audit log search
- **Why:** Queryable log storage for audit investigations; pairs with Grafana dashboards

### 42. Vector
- **Source:** https://github.com/vectordotdev/vector
- **License:** MPL 2.0
- **Purpose:** High-performance log/metrics pipeline
- **Integration Point:** Log routing from services to Loki/Wazuh/SIEM
- **Why:** Efficient log collection without heavy agents

---

## LOWER PRIORITY — API & Network Security

### 43. OAuth2 Proxy
- **Source:** https://github.com/oauth2-proxy/oauth2-proxy
- **License:** MIT
- **Purpose:** Reverse proxy for OAuth2/OIDC authentication
- **Integration Point:** Additional auth layer for internal services
- **Why:** Zero-trust access to internal dashboards (Grafana, MinIO console)

### 44. CrowdSec
- **Source:** https://github.com/crowdsecurity/crowdsec
- **License:** MIT
- **Purpose:** Collaborative security engine (behavioral IDS + IP reputation)
- **Integration Point:** API rate limiting, brute force protection
- **Why:** Community-driven threat intelligence for API protection

---

## Integration Summary by Category

| Category | Count | Priority |
|----------|-------|----------|
| Security Scanning & Vulnerability | 5 | High |
| Cloud Security & Config Monitoring | 4 | High |
| Observability & Monitoring | 5 | High |
| Runtime Security & SIEM | 3 | High |
| Task Queue & Background Processing | 2 | Medium |
| Incident Response & Automation | 2 | Medium |
| Documentation & Knowledge Base | 2 | Medium |
| Advanced Testing | 4 | Medium |
| Data Quality & Validation | 2 | Medium |
| Secrets Management | 2 | Medium |
| Kubernetes & Deployment | 4 | Lower |
| Compliance-Specific Tools | 3 | Lower |
| Machine Learning & AI | 2 | Lower |
| Log Management | 2 | Lower |
| API & Network Security | 2 | Lower |
| **Total New Integrations** | **44** | |

---

## Recommended Implementation Order

### Phase 1 — Production Readiness (Immediate)
1. Prometheus + Grafana (observability)
2. Sentry (error tracking)
3. Celery + RabbitMQ (task queue)
4. OpenTelemetry (distributed tracing)
5. Trivy (container scanning in CI/CD)

### Phase 2 — Compliance Automation (Short Term)
6. Prowler / CloudSploit (cloud security scanning)
7. OWASP ZAP + Nuclei (application security scanning)
8. Semgrep + Grype (SAST + SCA in CI/CD)
9. Checkov (IaC compliance)
10. Uptime Kuma (availability monitoring)

### Phase 3 — Enterprise Security (Medium Term)
11. Falco (runtime security)
12. Wazuh (SIEM + HIDS)
13. HashiCorp Vault (secrets management)
14. Loki + Vector (log management)
15. n8n (workflow automation)

### Phase 4 — Kubernetes & Scale (Long Term)
16. Helm chart packaging
17. Argo CD (GitOps deployment)
18. cert-manager + Kyverno (K8s security)
19. CrowdSec (API protection)
20. InSpec + OpenSCAP (compliance-as-code)

### Phase 5 — Advanced Intelligence (Future)
21. scikit-learn / PyOD (ML anomaly detection)
22. Great Expectations (data quality)
23. Playwright (E2E testing)
24. OpenControl (standards interoperability)
