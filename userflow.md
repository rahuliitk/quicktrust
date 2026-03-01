# QuickTrust - User Flow Diagrams

## 1. High-Level Platform Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        QuickTrust GRC Platform                         │
└─────────────────────────────────────────────────────────────────────────┘

                          ┌──────────────┐
                          │   New User   │
                          └──────┬───────┘
                                 │
                          ┌──────▼───────┐
                          │  Keycloak    │
                          │  Login/SSO   │
                          └──────┬───────┘
                                 │
                     ┌───────────▼───────────┐
                     │  Role-Based Routing   │
                     └───────────┬───────────┘
                                 │
         ┌───────────┬───────────┼───────────┬───────────┐
         ▼           ▼           ▼           ▼           ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
    │  Admin  │ │Compliance│ │ Control │ │Employee │ │ Auditor │
    │         │ │ Manager  │ │  Owner  │ │         │ │(External)│
    └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
         │           │           │           │           │
         ▼           ▼           ▼           ▼           ▼
    Full Access  Frameworks  Controls    Training   Read-Only
    + Settings   + Policies  + Evidence  + Reviews  Audit Portal
    + Users      + Risks     + Testing              via Token
    + Integrations+ Audits
```

---

## 2. Onboarding Flow

```
┌──────────────┐
│  User Signup │
│  (Keycloak)  │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ Step 1: Org Setup│
│ - Company name   │
│ - Industry       │
│ - Company size   │
│ - Cloud providers│
│ - Tech stack     │
└──────┬───────────┘
       │
       ▼
┌───────────────────────┐
│ Step 2: Framework     │
│ Selection             │
│ - SOC 2 Type II       │
│ - ISO 27001           │
│ - HIPAA               │
│ - PCI DSS             │
│ - GDPR                │
│ - NIST CSF            │
│ (multi-select)        │
└──────┬────────────────┘
       │
       ▼
┌───────────────────────┐
│ Step 3: AI Agent      │
│ Generation            │
│                       │
│ ┌───────────────────┐ │
│ │Controls Generation│ │
│ │Agent (LangGraph)  │ │
│ │                   │ │
│ │ load_requirements │ │
│ │       ▼           │ │
│ │ match_templates   │ │
│ │       ▼           │ │
│ │ customize_controls│ │
│ │       ▼           │ │
│ │ deduplicate       │ │
│ │       ▼           │ │
│ │ suggest_owners    │ │
│ │       ▼           │ │
│ │ finalize          │ │
│ └───────────────────┘ │
│                       │
│ ┌───────────────────┐ │
│ │Policy Generation  │ │
│ │Agent              │ │
│ └───────────────────┘ │
│                       │
│ ┌───────────────────┐ │
│ │Evidence Generation│ │
│ │Agent              │ │
│ └───────────────────┘ │
└──────┬────────────────┘
       │
       ▼
┌───────────────────────┐
│ Step 4: Review &      │
│ Dashboard             │
│ - Compliance score    │
│ - Generated controls  │
│ - Generated policies  │
│ - Evidence gaps       │
│ - Quick actions       │
└───────────────────────┘
```

---

## 3. Compliance Management Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Compliance Lifecycle                           │
└─────────────────────────────────────────────────────────────────────┘

  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │Framework │───▶│ Domains  │───▶│Requirem- │───▶│ Control  │
  │Selection │    │          │    │  ents    │    │Objectives│
  └──────────┘    └──────────┘    └──────────┘    └────┬─────┘
                                                       │
                                        ┌──────────────┘
                                        ▼
                                  ┌──────────┐
                                  │ Controls │
                                  │ (per org)│
                                  └────┬─────┘
                                       │
                    ┌──────────────────┬┴──────────────────┐
                    ▼                  ▼                    ▼
              ┌──────────┐      ┌──────────┐        ┌──────────┐
              │ Evidence │      │ Policies │        │   Risk   │
              │Collection│      │Lifecycle │        │ Mapping  │
              └────┬─────┘      └────┬─────┘        └────┬─────┘
                   │                 │                    │
                   ▼                 ▼                    ▼
              ┌──────────┐      ┌──────────┐        ┌──────────┐
              │Monitoring│      │  Audits  │        │  Gap     │
              │& Alerts  │      │& Findings│        │ Analysis │
              └──────────┘      └──────────┘        └──────────┘
```

---

## 4. Control Lifecycle Flow

```
                    ┌─────────┐
                    │  Draft  │◀──── AI Agent generates
                    └────┬────┘      or manual creation
                         │
                    ┌────▼────┐
                    │  Not    │
                    │Implement│◀──── Acknowledged but
                    │  -ed    │      not yet started
                    └────┬────┘
                         │
                    ┌────▼────┐
                    │   In    │◀──── Implementation
                    │Progress │      underway
                    └────┬────┘
                         │
                    ┌────▼────┐
                    │Implement│◀──── Fully deployed
                    │   -ed   │      and operational
                    └────┬────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │Effective │   │Partially │   │   Not    │
    │(tested   │   │Effective │   │Effective │
    │& passed) │   │(gaps     │   │(failed   │
    │          │   │ found)   │   │ testing) │
    └──────────┘   └────┬─────┘   └────┬─────┘
                        │              │
                        ▼              ▼
                   ┌──────────────────────┐
                   │  Remediation Agent   │
                   │  suggests fixes      │
                   └──────────────────────┘

  Evidence Collection:
  ┌──────────┐    ┌──────────┐    ┌──────────┐
  │  Manual  │    │Automated │    │ Prowler  │
  │  Upload  │    │Collectors│    │  Scan    │
  │(file/URL)│    │(AWS/GH/  │    │ Results  │
  │          │    │ Okta)    │    │          │
  └─────┬────┘    └─────┬────┘    └─────┬────┘
        │               │              │
        └───────────────┼──────────────┘
                        ▼
                  ┌──────────┐
                  │ Evidence │
                  │  Record  │
                  │(+ hash)  │
                  └──────────┘
```

---

## 5. Policy Lifecycle Flow

```
  ┌────────────┐
  │AI Generate │     ┌────────────┐
  │from Template├────▶│   Draft    │◀───── Manual creation
  └────────────┘     └─────┬──────┘
                           │
                     ┌─────▼──────┐
                     │  Pending   │◀───── Submitted for
                     │  Review    │       approval
                     └─────┬──────┘
                           │
                ┌──────────┼──────────┐
                ▼                     ▼
          ┌──────────┐          ┌──────────┐
          │ Approved │          │ Rejected │
          │(by admin)│          │(back to  │
          │          │          │ draft)   │
          └─────┬────┘          └──────────┘
                │
          ┌─────▼────┐
          │Published │◀───── Available to org
          └─────┬────┘
                │
          ┌─────▼────┐
          │ Review   │◀───── Periodic review
          │ Due      │       (next_review_date)
          └─────┬────┘
                │
          ┌─────▼────┐
          │ Archived │◀───── End of life
          └──────────┘
```

---

## 6. Risk Management Flow

```
  ┌────────────────┐
  │ Risk Identified│
  │ (manual or AI) │
  └───────┬────────┘
          │
          ▼
  ┌────────────────┐    ┌──────────────────────────────┐
  │  Risk Scoring  │    │  5x5 Risk Matrix             │
  │                │    │                              │
  │ Likelihood(1-5)│    │  5 │ M  H  H  C  C          │
  │ × Impact(1-5)  │    │  4 │ M  M  H  H  C          │
  │ = Score(1-25)  │    │  3 │ L  M  M  H  H          │
  │                │    │  2 │ L  L  M  M  H          │
  │ Level:         │    │  1 │ L  L  L  M  M          │
  │ low/med/high/  │    │    └──────────────────       │
  │ critical       │    │      1  2  3  4  5           │
  └───────┬────────┘    │      Impact ──────▶          │
          │             └──────────────────────────────┘
          ▼
  ┌────────────────┐
  │ Treatment Plan │
  ├────────────────┤
  │ - Mitigate     │──▶ Link to Controls
  │ - Transfer     │──▶ Insurance/Vendor
  │ - Accept       │──▶ Document rationale
  │ - Avoid        │──▶ Remove activity
  └───────┬────────┘
          │
          ▼
  ┌────────────────┐
  │ Residual Risk  │
  │ Re-assessment  │
  │ (post-control) │
  └───────┬────────┘
          │
          ▼
  ┌────────────────┐
  │ Periodic Review│
  │ (scheduled)    │
  └────────────────┘
```

---

## 7. Audit Workflow

```
  ┌────────────┐
  │  Planning  │◀──── Select framework, audit type,
  └─────┬──────┘      schedule dates, assign auditor
        │
  ┌─────▼──────┐
  │  Fieldwork │◀──── Active audit period
  └─────┬──────┘
        │
        │  ┌─────────────────────────────────────────────┐
        │  │ Audit Readiness Score Calculation            │
        │  │                                             │
        │  │ Controls (40%) + Evidence (30%)              │
        │  │ + Policies (20%) + Risks (10%)               │
        │  │ = Readiness %                                │
        │  └─────────────────────────────────────────────┘
        │
  ┌─────▼──────┐
  │  Review    │◀──── Findings documented
  └─────┬──────┘
        │
        │  ┌─────────────────────────────────────────────┐
        │  │ Auditor Portal (External)                   │
        │  │                                             │
        │  │ Access Token ──▶ Read-Only View of:         │
        │  │   • Controls & Evidence                     │
        │  │   • Policies                                │
        │  │   • Risks                                   │
        │  │   • Audit Findings                          │
        │  │                                             │
        │  │ Token expires after configured duration     │
        │  └─────────────────────────────────────────────┘
        │
  ┌─────▼──────┐
  │ Completed  │◀──── Report generated
  └─────┬──────┘
        │
  ┌─────▼──────┐
  │ Closed     │◀──── Archived
  └────────────┘
```

---

## 8. Evidence Collection Flow (Integrations)

```
  ┌───────────────────────────────────────────────────────────────┐
  │                   Integration Setup                           │
  └───────────────────────────────────────────────────────────────┘

  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │   AWS    │    │  GitHub  │    │   Okta   │    │ Prowler  │
  │          │    │          │    │          │    │          │
  │• IAM MFA │    │• Branch  │    │• MFA     │    │• Full    │
  │  Report  │    │  Protect │    │  Enroll  │    │  Scan    │
  │• Cloud   │    │• Depend- │    │  Report  │    │• Service │
  │  Trail   │    │  abot    │    │          │    │  Scan    │
  │• Encrypt │    │  Alerts  │    │          │    │• Compli- │
  │  Check   │    │          │    │          │    │  ance    │
  └─────┬────┘    └─────┬────┘    └─────┬────┘    └─────┬────┘
        │               │              │              │
        └───────────────┴──────┬───────┴──────────────┘
                               ▼
                   ┌────────────────────┐
                   │   Collection Job   │
                   │   (Background)     │
                   ├────────────────────┤
                   │ Status:            │
                   │ pending → running  │
                   │ → completed/failed │
                   └─────────┬──────────┘
                             │
                   ┌─────────▼──────────┐
                   │  Evidence Created  │
                   │  (auto-linked to   │
                   │   control)         │
                   └────────────────────┘
```

---

## 9. Incident Management Flow

```
  ┌──────────────┐
  │   Detected   │◀──── Monitoring alert / Manual report
  │   (Open)     │
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐    ┌──────────────────────────┐
  │Investigating │    │ Timeline Events:          │
  │              │───▶│ • Status changes          │
  └──────┬───────┘    │ • Notes added             │
         │           │ • Assignments changed      │
         │           │ • Evidence collected        │
         ▼           └──────────────────────────┘
  ┌──────────────┐
  │  Resolved    │◀──── Root cause fixed
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │   Closed     │◀──── Post-mortem completed
  │              │      Lessons documented
  └──────────────┘

  Severity Levels:
  ┌────┬──────────────────────────────┐
  │ P1 │ Critical - Service outage    │
  │ P2 │ High - Major degradation     │
  │ P3 │ Medium - Limited impact      │
  │ P4 │ Low - Minimal/no impact      │
  └────┴──────────────────────────────┘
```

---

## 10. Vendor Risk Management Flow

```
  ┌──────────────┐
  │ Add Vendor   │
  │ (name, type, │
  │  contact)    │
  └──────┬───────┘
         │
         ▼
  ┌──────────────────┐
  │ Initial Risk     │
  │ Tier Assignment  │
  │ (critical/high/  │
  │  medium/low)     │
  └──────┬───────────┘
         │
         ▼
  ┌──────────────────┐    ┌──────────────────────────┐
  │ Vendor Assessment│───▶│ AI Vendor Risk Assessment│
  │ Questionnaire    │    │ Agent (optional)         │
  └──────┬───────────┘    └──────────────────────────┘
         │
         ▼
  ┌──────────────────┐
  │ Score & Risk Tier│
  │ Update           │
  └──────┬───────────┘
         │
         ▼
  ┌──────────────────┐
  │ Contract Tracking│
  │ • Start/End dates│
  │ • Next assessment│
  │ • Status: active/│
  │   under_review/  │
  │   terminated     │
  └──────────────────┘
```

---

## 11. Training & Access Review Flow

```
  Training Flow:                       Access Review Flow:
  ═══════════════                      ═══════════════════

  ┌──────────────┐                     ┌──────────────┐
  │ Create Course│                     │Create Campaign│
  │ (video/doc/  │                     │ (title, due  │
  │  quiz)       │                     │  date)       │
  └──────┬───────┘                     └──────┬───────┘
         │                                    │
         ▼                                    ▼
  ┌──────────────┐                     ┌──────────────┐
  │ Assign to    │                     │ Add Entries  │
  │ Users/Roles  │                     │ (user, system│
  └──────┬───────┘                     │  access lvl) │
         │                             └──────┬───────┘
         ▼                                    │
  ┌──────────────┐                            ▼
  │  assigned    │                     ┌──────────────┐
  └──────┬───────┘                     │   Draft      │
         │                             └──────┬───────┘
         ▼                                    │
  ┌──────────────┐                            ▼
  │ in_progress  │                     ┌──────────────┐
  └──────┬───────┘                     │   Active     │
         │                             └──────┬───────┘
         ▼                                    │
  ┌──────────────┐                            ▼
  │ completed    │                     Per Entry Decision:
  │ (score, date)│                     ┌──────────────┐
  └──────────────┘                     │  approved /  │
                                       │  revoked /   │
  Overdue if past                      │  modified    │
  due_date without                     └──────┬───────┘
  completion                                  │
                                              ▼
                                       ┌──────────────┐
                                       │  Completed   │
                                       └──────────────┘
```

---

## 12. Monitoring & Notification Flow

```
  ┌─────────────────────────────────────────────────────────────┐
  │                  APScheduler (Background)                   │
  └──────────────────────────┬──────────────────────────────────┘
                             │
               Runs on schedule (hourly/daily/weekly)
                             │
                             ▼
  ┌────────────────────────────────────────────────────────────┐
  │                    Monitor Rules                           │
  ├────────────────────────────────────────────────────────────┤
  │ evidence_staleness │ Evidence older than N days?           │
  │ control_status     │ Controls still in draft/not_impl?    │
  │ policy_expiry      │ Policy past review date?             │
  │ manual             │ Custom check rules                   │
  └──────────────────────────┬─────────────────────────────────┘
                             │
                     Check fails?
                             │
                     ┌───────▼────────┐
                     │ Monitor Alert  │
                     │ (open)         │
                     └───────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │  In-App  │   │  Email   │   │  Slack   │
        │Notificat.│   │  (SMTP)  │   │(Webhook) │
        └──────────┘   └──────────┘   └──────────┘
                             │
                             ▼
                     ┌───────────────┐
                     │ acknowledged  │
                     └───────┬───────┘
                             │
                             ▼
                     ┌───────────────┐
                     │   resolved    │
                     └───────────────┘
```

---

## 13. Questionnaire Auto-Fill Flow

```
  ┌──────────────────┐
  │ Receive Security │
  │ Questionnaire    │
  │ (from customer)  │
  └──────┬───────────┘
         │
         ▼
  ┌──────────────────┐
  │ Import Questions │
  │ into Platform    │
  └──────┬───────────┘
         │
         ▼
  ┌──────────────────────────────────────────────┐
  │            Two-Pass Auto-Fill                 │
  │                                              │
  │  Pass 1: Keyword Matching (Fast)             │
  │  ┌────────────────────────────────┐          │
  │  │ Match questions to existing   │          │
  │  │ controls & policies by        │          │
  │  │ keyword analysis              │          │
  │  └──────────────┬─────────────────┘          │
  │                 ▼                            │
  │  Pass 2: LLM Refinement (Accurate)          │
  │  ┌────────────────────────────────┐          │
  │  │ Batch questions to LLM with   │          │
  │  │ org context for precise       │          │
  │  │ answers + confidence scores   │          │
  │  └────────────────────────────────┘          │
  └──────────────┬───────────────────────────────┘
                 │
                 ▼
  ┌──────────────────┐
  │ Review Responses │
  │ (confidence %    │
  │  per answer)     │
  └──────┬───────────┘
         │
         ▼
  ┌──────────────────┐
  │ Approve & Submit │
  │ to Customer      │
  └──────────────────┘
```

---

## 14. Trust Center (Public Portal) Flow

```
  Admin View:                          Public View:
  ═══════════                          ════════════

  ┌──────────────┐                     ┌──────────────────┐
  │ Configure    │                     │ /trust/{slug}    │
  │ Trust Center │                     │                  │
  │              │                     │ ┌──────────────┐ │
  │ • Slug       │      Publish       │ │  Company     │ │
  │ • Headline   │ ──────────────────▶ │ │  Headline    │ │
  │ • Description│                     │ └──────────────┘ │
  │ • Logo       │                     │                  │
  │ • Contact    │                     │ ┌──────────────┐ │
  └──────┬───────┘                     │ │Certifications│ │
         │                             │ │ SOC 2, ISO   │ │
         ▼                             │ └──────────────┘ │
  ┌──────────────┐                     │                  │
  │ Add Documents│                     │ ┌──────────────┐ │
  │ • SOC 2 Rpt  │                     │ │  Documents   │ │
  │ • Policies   │                     │ │ (public/NDA) │ │
  │ • Certs      │                     │ └──────────────┘ │
  │ • Pentest    │                     └──────────────────┘
  └──────────────┘
```

---

## 15. Report Generation Flow

```
  ┌──────────────────┐
  │ Select Report    │
  │ Type             │
  ├──────────────────┤
  │ • compliance_    │
  │   summary        │
  │ • risk_report    │
  │ • evidence_audit │
  │ • training_      │
  │   completion     │
  └──────┬───────────┘
         │
         ▼
  ┌──────────────────┐
  │ Choose Format    │
  │ • PDF            │
  │ • CSV            │
  │ • JSON           │
  └──────┬───────────┘
         │
         ▼
  ┌──────────────────┐
  │ Generation       │
  │ (Background)     │
  │ pending ──▶      │
  │ generating ──▶   │
  │ completed        │
  └──────┬───────────┘
         │
         ▼
  ┌──────────────────┐
  │ Stored in MinIO  │
  │ Download via URL │
  └──────────────────┘
```

---

## 16. Multi-Tenant Data Isolation

```
  ┌──────────────────────────────────────────────────────────────┐
  │                    Request Pipeline                          │
  └──────────────────────────────────────────────────────────────┘

  Incoming Request
       │
       ▼
  ┌──────────────┐
  │  Keycloak    │
  │  JWT Token   │
  │  Validation  │
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │ Extract      │
  │ user_id,     │
  │ org_id,      │
  │ role         │
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐     ┌────────────────────────────────┐
  │ RoleChecker  │     │ Roles:                         │
  │ Dependency   │────▶│ super_admin  (all access)      │
  │              │     │ admin        (org admin)        │
  │              │     │ compliance_manager              │
  │              │     │ control_owner                   │
  │              │     │ employee                        │
  │              │     │ executive                       │
  │              │     │ auditor_internal                │
  │              │     │ auditor_external                │
  └──────┬───────┘     └────────────────────────────────┘
         │
         ▼
  ┌──────────────┐
  │verify_org_   │◀──── Ensures URL org_id matches
  │access()      │      user's org_id
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │ All queries  │◀──── WHERE org_id = :user_org_id
  │ scoped to    │      on every table
  │ org_id       │
  └──────────────┘
```
