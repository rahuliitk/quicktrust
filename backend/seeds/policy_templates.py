"""Policy template seed data — 10 core policy templates with full Markdown content."""

POLICY_TEMPLATES = [
    {
        "template_code": "POL-001",
        "title": "Information Security Policy",
        "description": "Master information security policy establishing the organization's security program and governance structure.",
        "category": "Security",
        "sections": ["Purpose", "Scope", "Policy Statement", "Roles and Responsibilities", "Risk Management", "Compliance", "Review and Updates"],
        "variables": ["company_name", "industry", "cloud_providers"],
        "required_by_frameworks": ["SOC 2", "ISO 27001"],
        "review_frequency": "annual",
        "content_template": """# Information Security Policy

## 1. Purpose
This policy establishes the information security program for {company_name} and defines the principles, responsibilities, and requirements for protecting information assets.

## 2. Scope
This policy applies to all employees, contractors, consultants, and third parties who access {company_name}'s information systems, data, and technology resources.

## 3. Policy Statement
{company_name} is committed to protecting the confidentiality, integrity, and availability of all information assets. The organization shall implement and maintain an information security management system aligned with industry best practices and regulatory requirements.

### 3.1 Information Security Principles
- **Confidentiality**: Information shall be accessible only to authorized individuals.
- **Integrity**: Information shall be accurate, complete, and protected from unauthorized modification.
- **Availability**: Information and systems shall be available when needed by authorized users.

### 3.2 Security Controls
The organization shall implement appropriate technical, administrative, and physical controls to protect information assets hosted on {cloud_providers} and other infrastructure.

## 4. Roles and Responsibilities
- **Executive Management**: Approve security policies and allocate resources for the security program.
- **Security Team**: Develop, implement, and monitor security controls.
- **Department Managers**: Ensure compliance within their teams.
- **All Personnel**: Follow security policies and report incidents.

## 5. Risk Management
{company_name} shall maintain a risk management program to identify, assess, and mitigate information security risks. Risk assessments shall be conducted at least annually and whenever significant changes occur.

## 6. Compliance
This policy supports compliance with applicable laws, regulations, and contractual obligations relevant to the {industry} industry.

## 7. Review and Updates
This policy shall be reviewed annually and updated as needed to address changes in the threat landscape, technology, or business operations.

**Effective Date**: [Date]
**Last Reviewed**: [Date]
**Approved By**: [Name, Title]
""",
    },
    {
        "template_code": "POL-002",
        "title": "Acceptable Use Policy",
        "description": "Defines acceptable and prohibited uses of organizational technology resources and information assets.",
        "category": "Security",
        "sections": ["Purpose", "Scope", "Acceptable Use", "Prohibited Activities", "Monitoring", "Enforcement"],
        "variables": ["company_name"],
        "required_by_frameworks": ["SOC 2", "ISO 27001"],
        "review_frequency": "annual",
        "content_template": """# Acceptable Use Policy

## 1. Purpose
This policy defines the acceptable use of technology resources at {company_name} to protect the organization and its employees from security threats.

## 2. Scope
This policy applies to all employees, contractors, and third parties using {company_name}'s technology resources, including computers, networks, email, internet access, and cloud services.

## 3. Acceptable Use
### 3.1 General Use
- Technology resources are provided primarily for business purposes.
- Limited personal use is permitted provided it does not interfere with work duties or violate this policy.
- Users are responsible for the security of their accounts and devices.

### 3.2 Email and Communication
- Business email shall be used for professional communications.
- Sensitive information must be encrypted when transmitted externally.
- Users shall not open suspicious attachments or links.

### 3.3 Internet Access
- Internet access is provided for business-related activities.
- Users shall exercise good judgment when browsing the web.
- Downloads must be from trusted and verified sources.

## 4. Prohibited Activities
The following activities are strictly prohibited:
- Unauthorized access to systems, data, or networks
- Installing unauthorized software on company devices
- Sharing credentials or authentication tokens
- Transmitting confidential data through unapproved channels
- Bypassing security controls or monitoring systems
- Using company resources for illegal activities
- Connecting unauthorized devices to the corporate network

## 5. Monitoring
{company_name} reserves the right to monitor technology resource usage to ensure compliance with this policy and to protect organizational assets. Monitoring may include network traffic, email, and system access logs.

## 6. Enforcement
Violations of this policy may result in disciplinary action, up to and including termination of employment. Serious violations may be referred to law enforcement.

**Effective Date**: [Date]
**Last Reviewed**: [Date]
**Approved By**: [Name, Title]
""",
    },
    {
        "template_code": "POL-003",
        "title": "Access Control Policy",
        "description": "Establishes controls for logical and physical access to information systems and data.",
        "category": "Security",
        "sections": ["Purpose", "Scope", "Access Control Principles", "User Access Management", "Authentication", "Access Reviews", "Enforcement"],
        "variables": ["company_name", "cloud_providers"],
        "required_by_frameworks": ["SOC 2", "ISO 27001"],
        "review_frequency": "annual",
        "content_template": """# Access Control Policy

## 1. Purpose
This policy establishes the requirements for controlling access to {company_name}'s information systems, applications, and data to ensure only authorized individuals can access resources appropriate to their role.

## 2. Scope
This policy applies to all access to {company_name}'s systems, including on-premises infrastructure, cloud services ({cloud_providers}), SaaS applications, and physical facilities.

## 3. Access Control Principles
- **Least Privilege**: Users shall be granted the minimum access necessary to perform their job functions.
- **Need-to-Know**: Access to information shall be restricted to individuals who require it for their role.
- **Separation of Duties**: Critical functions shall be divided among different individuals to reduce risk.
- **Defense in Depth**: Multiple layers of access controls shall be implemented.

## 4. User Access Management
### 4.1 User Registration
- All user accounts must be approved by the appropriate manager before creation.
- Each user shall have a unique identifier; shared accounts are prohibited.

### 4.2 Provisioning
- Access shall be provisioned based on role-based access control (RBAC).
- Privileged access requires additional approval from the security team.

### 4.3 Deprovisioning
- Access shall be revoked within 24 hours of employment termination.
- Access shall be modified within 48 hours of role changes.

## 5. Authentication
- Multi-factor authentication (MFA) is required for all access to production systems and cloud consoles.
- Passwords must meet minimum complexity requirements (12+ characters, mixed case, numbers, symbols).
- Service accounts must use API keys or certificates, not passwords.

## 6. Access Reviews
- Access reviews shall be conducted quarterly for privileged accounts.
- Access reviews shall be conducted semi-annually for all user accounts.
- Unused accounts shall be disabled after 90 days of inactivity.

## 7. Enforcement
Unauthorized access attempts will be logged, investigated, and may result in disciplinary action.

**Effective Date**: [Date]
**Last Reviewed**: [Date]
**Approved By**: [Name, Title]
""",
    },
    {
        "template_code": "POL-004",
        "title": "Data Classification Policy",
        "description": "Defines data classification levels and handling requirements for each level.",
        "category": "Security",
        "sections": ["Purpose", "Scope", "Classification Levels", "Handling Requirements", "Labeling", "Data Lifecycle"],
        "variables": ["company_name", "industry"],
        "required_by_frameworks": ["SOC 2", "ISO 27001"],
        "review_frequency": "annual",
        "content_template": """# Data Classification Policy

## 1. Purpose
This policy defines the classification scheme for {company_name}'s information assets and establishes handling requirements for each classification level.

## 2. Scope
This policy applies to all data created, collected, stored, processed, or transmitted by {company_name}, regardless of format or location.

## 3. Classification Levels

### 3.1 Public
Information approved for public release. No special handling required.
- Examples: Marketing materials, published blog posts, public documentation.

### 3.2 Internal
Information intended for internal use only. Moderate protection required.
- Examples: Internal policies, organizational charts, project documentation.

### 3.3 Confidential
Sensitive business information requiring strong protection. Unauthorized disclosure could harm {company_name}.
- Examples: Financial reports, business strategies, employee records, customer lists.

### 3.4 Restricted
Highly sensitive data requiring the strongest protection. Unauthorized disclosure could cause severe damage.
- Examples: Encryption keys, authentication credentials, PII, PHI, payment card data.

## 4. Handling Requirements

| Requirement | Public | Internal | Confidential | Restricted |
|---|---|---|---|---|
| Encryption at Rest | Optional | Recommended | Required | Required |
| Encryption in Transit | Optional | Required | Required | Required |
| Access Control | None | Role-based | Need-to-know | Strict need-to-know |
| Sharing | Unrestricted | Internal only | Approved recipients | Named individuals |
| Retention | Per schedule | Per schedule | Per schedule + legal | Per schedule + legal |
| Disposal | Standard delete | Secure delete | Secure wipe | Certified destruction |

## 5. Labeling
- All documents should include a classification label in the header or footer.
- Electronic files should be tagged with the appropriate classification metadata.
- Data owners are responsible for classifying their data assets.

## 6. Data Lifecycle
Data classification shall be reviewed when data is created, modified, shared, or archived. Data owners shall ensure appropriate classification throughout the data lifecycle relevant to {industry} regulatory requirements.

**Effective Date**: [Date]
**Last Reviewed**: [Date]
**Approved By**: [Name, Title]
""",
    },
    {
        "template_code": "POL-005",
        "title": "Incident Response Plan",
        "description": "Establishes procedures for detecting, responding to, and recovering from security incidents.",
        "category": "Operations",
        "sections": ["Purpose", "Scope", "Incident Categories", "Response Procedures", "Communication", "Post-Incident Review", "Testing"],
        "variables": ["company_name"],
        "required_by_frameworks": ["SOC 2", "ISO 27001"],
        "review_frequency": "semi-annual",
        "content_template": """# Incident Response Plan

## 1. Purpose
This plan establishes the procedures for {company_name} to detect, respond to, contain, and recover from information security incidents in a timely and effective manner.

## 2. Scope
This plan covers all information security incidents affecting {company_name}'s systems, data, personnel, and operations.

## 3. Incident Categories

| Severity | Description | Response Time | Examples |
|---|---|---|---|
| Critical (P1) | Active breach or data exfiltration | 15 minutes | Active attack, ransomware, data breach |
| High (P2) | Potential breach or significant vulnerability | 1 hour | Compromised credentials, malware detection |
| Medium (P3) | Security event requiring investigation | 4 hours | Unusual access patterns, policy violation |
| Low (P4) | Minor security event | 24 hours | Failed login attempts, phishing email |

## 4. Response Procedures

### 4.1 Detection and Reporting
- Security events can be detected through automated monitoring, employee reports, or third-party notifications.
- All personnel must report suspected incidents to the security team immediately.

### 4.2 Triage and Classification
- The on-call security engineer assesses the event and assigns severity.
- Critical and high-severity incidents trigger the incident response team.

### 4.3 Containment
- Isolate affected systems to prevent further damage.
- Preserve evidence for forensic analysis.
- Implement temporary mitigations as needed.

### 4.4 Eradication
- Remove the threat from all affected systems.
- Patch vulnerabilities that were exploited.
- Reset compromised credentials.

### 4.5 Recovery
- Restore affected systems from verified clean backups.
- Gradually restore services with enhanced monitoring.
- Verify system integrity before full restoration.

## 5. Communication
- Internal stakeholders shall be notified per severity escalation matrix.
- Affected customers shall be notified within 72 hours of confirmed data breach.
- Regulatory notifications shall be made as required by applicable laws.

## 6. Post-Incident Review
- A post-incident review shall be conducted within 5 business days of incident closure.
- Lessons learned shall be documented and used to improve controls.
- The incident response plan shall be updated based on findings.

## 7. Testing
- Tabletop exercises shall be conducted semi-annually.
- The incident response plan shall be tested at least annually.

**Effective Date**: [Date]
**Last Reviewed**: [Date]
**Approved By**: [Name, Title]
""",
    },
    {
        "template_code": "POL-006",
        "title": "Change Management Policy",
        "description": "Defines the process for managing changes to IT systems, applications, and infrastructure.",
        "category": "Operations",
        "sections": ["Purpose", "Scope", "Change Types", "Change Process", "Approval", "Emergency Changes", "Documentation"],
        "variables": ["company_name", "tech_stack"],
        "required_by_frameworks": ["SOC 2", "ISO 27001"],
        "review_frequency": "annual",
        "content_template": """# Change Management Policy

## 1. Purpose
This policy establishes the process for managing changes to {company_name}'s information systems, applications ({tech_stack}), and infrastructure to minimize risk and ensure service continuity.

## 2. Scope
This policy applies to all changes to production systems, including software deployments, infrastructure modifications, configuration changes, and database schema updates.

## 3. Change Types

### 3.1 Standard Changes
Pre-approved, low-risk changes with established procedures. Examples: routine patches, certificate renewals.

### 3.2 Normal Changes
Changes requiring approval through the standard change process. Examples: feature releases, infrastructure upgrades.

### 3.3 Emergency Changes
Urgent changes needed to resolve critical incidents. Examples: security patches for active vulnerabilities, emergency hotfixes.

## 4. Change Process

### 4.1 Request
- All changes must be documented with description, risk assessment, rollback plan, and testing evidence.
- Change requests must include impact analysis and affected systems.

### 4.2 Review
- Changes are reviewed by the technical lead and relevant stakeholders.
- Security-impacting changes require security team review.

### 4.3 Testing
- All changes must be tested in a staging environment before production deployment.
- Test results must be documented and attached to the change request.

### 4.4 Deployment
- Changes shall be deployed during approved maintenance windows when possible.
- Deployment must follow the documented deployment procedure.
- Monitoring shall be enhanced during and after deployment.

### 4.5 Validation
- Post-deployment verification shall confirm the change was successful.
- Rollback shall be executed if critical issues are detected.

## 5. Approval
- Standard changes: No additional approval required (pre-approved).
- Normal changes: Requires approval from technical lead and change manager.
- Emergency changes: Can be deployed with verbal approval, with formal documentation within 24 hours.

## 6. Emergency Changes
Emergency changes bypass the standard approval process but must:
- Be documented retrospectively within 24 hours
- Include a post-implementation review
- Be reported to the change advisory board

## 7. Documentation
All changes shall be tracked in the change management system with full audit trail including requester, approver, deployment details, and outcome.

**Effective Date**: [Date]
**Last Reviewed**: [Date]
**Approved By**: [Name, Title]
""",
    },
    {
        "template_code": "POL-007",
        "title": "Vendor Management Policy",
        "description": "Establishes requirements for assessing and managing third-party vendor risks.",
        "category": "Operations",
        "sections": ["Purpose", "Scope", "Vendor Classification", "Risk Assessment", "Security Requirements", "Monitoring", "Termination"],
        "variables": ["company_name", "industry"],
        "required_by_frameworks": ["SOC 2", "ISO 27001"],
        "review_frequency": "annual",
        "content_template": """# Vendor Management Policy

## 1. Purpose
This policy establishes the requirements for assessing, selecting, and monitoring third-party vendors that access or process {company_name}'s data and systems.

## 2. Scope
This policy applies to all third-party vendors, suppliers, and service providers who access, process, store, or transmit {company_name}'s information or connect to its networks.

## 3. Vendor Classification

| Tier | Criteria | Assessment Frequency |
|---|---|---|
| Critical | Access to sensitive data, core business operations | Annual + continuous monitoring |
| High | Access to internal systems, non-critical data | Annual |
| Medium | Limited system access, no sensitive data | Every 2 years |
| Low | No system access, no data access | Initial assessment only |

## 4. Risk Assessment
- All vendors shall undergo a security risk assessment before onboarding.
- Assessment shall include review of security certifications (SOC 2, ISO 27001), security questionnaire, and contractual review.
- Vendors processing data subject to {industry} regulations must demonstrate relevant compliance.

## 5. Security Requirements
Vendor agreements shall include:
- Data protection and confidentiality obligations
- Incident notification requirements (within 24 hours)
- Right to audit or assess security controls
- Data return and destruction upon termination
- Subcontractor security requirements
- Compliance with applicable regulations

## 6. Monitoring
- Critical vendors shall be monitored continuously for security incidents and compliance.
- Vendor security assessments shall be conducted per the classification schedule.
- Vendor security certifications and insurance shall be verified annually.

## 7. Termination
Upon vendor relationship termination:
- All {company_name} data shall be returned or securely destroyed
- Access to systems shall be revoked immediately
- Confirmation of data destruction shall be obtained in writing

**Effective Date**: [Date]
**Last Reviewed**: [Date]
**Approved By**: [Name, Title]
""",
    },
    {
        "template_code": "POL-008",
        "title": "Password & Authentication Policy",
        "description": "Defines requirements for passwords, authentication mechanisms, and credential management.",
        "category": "Security",
        "sections": ["Purpose", "Scope", "Password Requirements", "Multi-Factor Authentication", "Service Accounts", "Credential Storage"],
        "variables": ["company_name", "cloud_providers"],
        "required_by_frameworks": ["SOC 2", "ISO 27001"],
        "review_frequency": "annual",
        "content_template": """# Password & Authentication Policy

## 1. Purpose
This policy defines the requirements for authentication mechanisms at {company_name} to ensure strong identity verification and prevent unauthorized access.

## 2. Scope
This policy applies to all user accounts, service accounts, and API credentials used to access {company_name}'s systems, including {cloud_providers} cloud infrastructure.

## 3. Password Requirements
### 3.1 Complexity
- Minimum length: 12 characters
- Must include: uppercase, lowercase, numbers, and special characters
- Must not contain the username or common dictionary words
- Must not reuse the last 12 passwords

### 3.2 Expiration
- Standard user passwords: Expire every 90 days
- Privileged account passwords: Expire every 60 days
- Password change is required immediately if compromise is suspected

### 3.3 Lockout
- Accounts shall be locked after 5 consecutive failed login attempts
- Lockout duration: 15 minutes minimum
- Administrative unlock required after 10 consecutive failures

## 4. Multi-Factor Authentication (MFA)
MFA is required for:
- All access to production systems and cloud consoles
- VPN and remote access
- Administrative and privileged accounts
- Access to sensitive data repositories
- SSO portal access

Acceptable MFA methods:
- Hardware security keys (preferred for privileged accounts)
- Authenticator apps (TOTP)
- Push notifications from approved apps

SMS-based MFA is not permitted for privileged accounts.

## 5. Service Accounts
- Service accounts must use API keys, certificates, or managed identities
- Service account credentials must be stored in a secrets manager
- Service account credentials must be rotated at least every 90 days
- Service accounts must follow least-privilege principles

## 6. Credential Storage
- Passwords shall never be stored in plaintext
- Credentials shall not be stored in source code or configuration files
- All credentials shall be stored in an approved secrets management solution
- Shared credentials are prohibited

**Effective Date**: [Date]
**Last Reviewed**: [Date]
**Approved By**: [Name, Title]
""",
    },
    {
        "template_code": "POL-009",
        "title": "Remote Work & BYOD Policy",
        "description": "Defines security requirements for remote working and personal device usage.",
        "category": "Operations",
        "sections": ["Purpose", "Scope", "Remote Work Requirements", "BYOD Requirements", "Network Security", "Data Protection"],
        "variables": ["company_name"],
        "required_by_frameworks": ["ISO 27001"],
        "review_frequency": "annual",
        "content_template": """# Remote Work & BYOD Policy

## 1. Purpose
This policy establishes the security requirements for {company_name} employees working remotely and using personal devices (Bring Your Own Device) for business purposes.

## 2. Scope
This policy applies to all {company_name} personnel who work remotely or use personal devices to access company resources.

## 3. Remote Work Requirements
### 3.1 Approved Locations
- Remote work must be conducted from a secure, private location.
- Public Wi-Fi shall not be used without VPN connection.
- Screens must be positioned to prevent unauthorized viewing.

### 3.2 Equipment
- Company-provided laptops are required for accessing sensitive data.
- All devices must have endpoint protection software installed and active.
- Devices must have full disk encryption enabled.
- Operating systems and software must be kept up to date.

### 3.3 Physical Security
- Devices must be locked when unattended.
- Sensitive documents must be stored securely and shredded when no longer needed.
- Devices must not be left in vehicles or other unsecured locations.

## 4. BYOD Requirements
### 4.1 Enrollment
- Personal devices must be registered with IT before accessing company resources.
- Devices must meet minimum security requirements (OS version, encryption, passcode).

### 4.2 Security Controls
- Mobile device management (MDM) software may be required.
- Remote wipe capability must be enabled for devices accessing company data.
- Company data must be stored in approved applications only.

### 4.3 Separation
- Personal and business data must be separated where technically feasible.
- Company data shall be removed from personal devices upon employment termination.

## 5. Network Security
- VPN must be used when accessing company resources from external networks.
- Home Wi-Fi networks should use WPA3 or WPA2 encryption with strong passwords.
- Network sharing with unknown devices is prohibited.

## 6. Data Protection
- Sensitive data shall not be stored locally on personal devices.
- Cloud storage of company data must use approved services only.
- Data transfer between personal and company devices must use approved methods.

**Effective Date**: [Date]
**Last Reviewed**: [Date]
**Approved By**: [Name, Title]
""",
    },
    {
        "template_code": "POL-010",
        "title": "Risk Management Policy",
        "description": "Defines the organization's approach to identifying, assessing, and managing information security risks.",
        "category": "Security",
        "sections": ["Purpose", "Scope", "Risk Management Framework", "Risk Assessment", "Risk Treatment", "Risk Monitoring", "Governance"],
        "variables": ["company_name", "industry"],
        "required_by_frameworks": ["SOC 2", "ISO 27001"],
        "review_frequency": "annual",
        "content_template": """# Risk Management Policy

## 1. Purpose
This policy defines {company_name}'s approach to identifying, assessing, treating, and monitoring information security risks to protect organizational objectives and assets.

## 2. Scope
This policy applies to all information security risks across {company_name}'s operations, technology, processes, and third-party relationships.

## 3. Risk Management Framework
{company_name} adopts a risk management framework aligned with ISO 31000 and tailored to {industry} industry requirements. The framework includes:
- Risk identification
- Risk analysis and evaluation
- Risk treatment
- Risk monitoring and review
- Risk communication and reporting

## 4. Risk Assessment
### 4.1 Frequency
- Comprehensive risk assessment: Annually
- Targeted assessments: When significant changes occur
- Continuous assessment: Automated vulnerability scanning

### 4.2 Methodology
- Risks are identified through threat modeling, vulnerability assessments, incident analysis, and stakeholder input.
- Risk is evaluated based on likelihood (1-5) and impact (1-5).
- Risk score = Likelihood x Impact (1-25).

### 4.3 Risk Levels

| Score | Level | Action Required |
|---|---|---|
| 20-25 | Critical | Immediate action required; escalate to executive management |
| 12-19 | High | Risk treatment plan required within 30 days |
| 6-11 | Medium | Risk treatment plan required within 90 days |
| 1-5 | Low | Accept and monitor; address opportunistically |

## 5. Risk Treatment
Risk treatment options include:
- **Mitigate**: Implement controls to reduce likelihood or impact
- **Transfer**: Transfer risk through insurance or third-party agreements
- **Accept**: Accept the risk with documented rationale and management approval
- **Avoid**: Eliminate the activity that gives rise to the risk

Residual risk after treatment must be formally accepted by the risk owner.

## 6. Risk Monitoring
- The risk register shall be reviewed quarterly.
- Key risk indicators (KRIs) shall be monitored continuously.
- Risk treatment progress shall be reported to management monthly.

## 7. Governance
- **Risk Owner**: Accountable for managing specific risks.
- **Security Team**: Facilitates risk assessments and maintains the risk register.
- **Executive Management**: Reviews and approves risk appetite and treatment plans.
- **Audit Committee**: Provides independent oversight of the risk management program.

**Effective Date**: [Date]
**Last Reviewed**: [Date]
**Approved By**: [Name, Title]
""",
    },
]


async def seed_policy_templates(db):
    from app.models.policy_template import PolicyTemplate
    from sqlalchemy import select

    # Check if already seeded
    existing = await db.execute(select(PolicyTemplate).limit(1))
    if existing.scalar_one_or_none():
        print("Policy templates already seeded, skipping.")
        return

    for tmpl_data in POLICY_TEMPLATES:
        template = PolicyTemplate(**tmpl_data)
        db.add(template)

    await db.commit()
    print(f"Seeded {len(POLICY_TEMPLATES)} policy templates.")
