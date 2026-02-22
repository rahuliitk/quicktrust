"""25 control templates mapped to SOC 2 requirements."""

CONTROL_TEMPLATES = [
    # Access Control (7)
    {
        "template_code": "AC-001",
        "title": "Multi-Factor Authentication (MFA)",
        "domain": "Access Control",
        "description": "Enforce multi-factor authentication for all user accounts accessing production systems and sensitive data.",
        "implementation_guidance": "1. Enable MFA on identity provider (e.g., Okta, Azure AD)\n2. Require MFA for all {cloud_provider} console access\n3. Enforce MFA for VPN and remote access\n4. Monitor MFA enrollment rates\n5. Implement hardware key support for privileged accounts",
        "test_procedure": "1. Verify MFA is enabled for all active users\n2. Attempt login without MFA and confirm denial\n3. Review MFA enrollment report\n4. Check that admin accounts use hardware keys",
        "automation_level": "automated",
        "variables": {"cloud_provider": "AWS", "identity_provider": "Okta"},
        "requirement_codes": ["CC6.1", "CC6.2"],
    },
    {
        "template_code": "AC-002",
        "title": "Single Sign-On (SSO) Implementation",
        "domain": "Access Control",
        "description": "Implement centralized SSO for all business applications to enforce consistent authentication policies.",
        "implementation_guidance": "1. Configure SSO via {identity_provider}\n2. Integrate all SaaS applications with SSO\n3. Disable local authentication where possible\n4. Set session timeout policies\n5. Enable adaptive authentication based on risk signals",
        "test_procedure": "1. Verify all critical applications are SSO-integrated\n2. Confirm local login is disabled\n3. Test session timeout behavior\n4. Review SSO audit logs",
        "automation_level": "automated",
        "variables": {"identity_provider": "Okta"},
        "requirement_codes": ["CC6.1"],
    },
    {
        "template_code": "AC-003",
        "title": "Role-Based Access Control (RBAC)",
        "domain": "Access Control",
        "description": "Implement role-based access control to enforce least privilege across all systems.",
        "implementation_guidance": "1. Define roles and permission matrices\n2. Implement RBAC in {cloud_provider} IAM\n3. Apply RBAC to application-level access\n4. Document role definitions and assignments\n5. Review and update roles quarterly",
        "test_procedure": "1. Review IAM policies for least privilege\n2. Verify no wildcard permissions exist\n3. Confirm role assignments match job functions\n4. Test that restricted resources are inaccessible to unauthorized roles",
        "automation_level": "semi_automated",
        "variables": {"cloud_provider": "AWS"},
        "requirement_codes": ["CC6.1", "CC6.2"],
    },
    {
        "template_code": "AC-004",
        "title": "User Provisioning and Deprovisioning",
        "domain": "Access Control",
        "description": "Establish automated user provisioning and deprovisioning processes tied to HR lifecycle events.",
        "implementation_guidance": "1. Integrate HR system with identity provider\n2. Automate account creation on hire\n3. Automate access revocation on termination (within 24 hours)\n4. Implement access modification workflow for role changes\n5. Log all provisioning events",
        "test_procedure": "1. Review recent terminations and verify access was revoked\n2. Check provisioning automation logs\n3. Verify no orphaned accounts exist\n4. Test deprovisioning workflow end-to-end",
        "automation_level": "automated",
        "variables": {},
        "requirement_codes": ["CC6.2", "CC6.3"],
    },
    {
        "template_code": "AC-005",
        "title": "Quarterly Access Reviews",
        "domain": "Access Control",
        "description": "Conduct quarterly reviews of user access rights to ensure appropriateness.",
        "implementation_guidance": "1. Generate access reports from identity provider\n2. Distribute reports to managers for review\n3. Managers confirm or revoke access for their reports\n4. IT processes revocations within 5 business days\n5. Document review results and retain evidence",
        "test_procedure": "1. Verify access review was completed last quarter\n2. Review evidence of manager approvals\n3. Confirm revocations were processed\n4. Check that review covers all critical systems",
        "automation_level": "semi_automated",
        "variables": {},
        "requirement_codes": ["CC6.3"],
    },
    {
        "template_code": "AC-006",
        "title": "Password Policy Enforcement",
        "domain": "Access Control",
        "description": "Enforce password complexity requirements and rotation policies across all systems.",
        "implementation_guidance": "1. Set minimum password length to 12 characters\n2. Require mix of uppercase, lowercase, numbers, special characters\n3. Implement password history (last 12 passwords)\n4. Set maximum password age to 90 days\n5. Enable account lockout after 5 failed attempts",
        "test_procedure": "1. Review password policy configuration\n2. Test password complexity enforcement\n3. Verify account lockout threshold\n4. Confirm password history is enforced",
        "automation_level": "automated",
        "variables": {},
        "requirement_codes": ["CC6.1"],
    },
    {
        "template_code": "AC-007",
        "title": "Privileged Access Management",
        "domain": "Access Control",
        "description": "Implement enhanced controls for privileged access accounts including just-in-time access and session recording.",
        "implementation_guidance": "1. Implement privileged access management (PAM) solution\n2. Require just-in-time access elevation\n3. Enable session recording for privileged sessions\n4. Implement break-glass procedures for emergency access\n5. Review privileged access monthly",
        "test_procedure": "1. Verify PAM solution is deployed\n2. Test just-in-time access workflow\n3. Review session recordings from last month\n4. Verify break-glass procedure is documented",
        "automation_level": "semi_automated",
        "variables": {},
        "requirement_codes": ["CC6.1", "CC6.2", "CC6.3"],
    },
    # Network Security (2)
    {
        "template_code": "NS-001",
        "title": "Firewall and Network Segmentation",
        "domain": "Network Security",
        "description": "Implement network firewalls and segmentation to restrict traffic between network zones.",
        "implementation_guidance": "1. Deploy {cloud_provider} network firewalls (Security Groups / NACLs)\n2. Implement network segmentation (production, staging, development)\n3. Restrict inbound access to necessary ports only\n4. Implement default-deny egress rules\n5. Review firewall rules quarterly",
        "test_procedure": "1. Review firewall rule configurations\n2. Verify network segmentation is enforced\n3. Scan for unintended open ports\n4. Confirm default-deny policy is in place",
        "automation_level": "automated",
        "variables": {"cloud_provider": "AWS"},
        "requirement_codes": ["CC6.6"],
    },
    {
        "template_code": "NS-002",
        "title": "Encryption in Transit (TLS)",
        "domain": "Network Security",
        "description": "Enforce TLS 1.2+ encryption for all data transmitted over networks.",
        "implementation_guidance": "1. Configure TLS 1.2+ on all public-facing endpoints\n2. Implement HTTPS redirect for all web traffic\n3. Use TLS for internal service-to-service communication\n4. Configure certificate auto-renewal\n5. Disable deprecated TLS versions and weak cipher suites",
        "test_procedure": "1. Run TLS scanner on all public endpoints\n2. Verify TLS 1.2+ is enforced\n3. Confirm no weak ciphers are enabled\n4. Check certificate expiration dates",
        "automation_level": "automated",
        "variables": {},
        "requirement_codes": ["CC6.7"],
    },
    # Data Protection (3)
    {
        "template_code": "DP-001",
        "title": "Encryption at Rest",
        "domain": "Data Protection",
        "description": "Encrypt all data at rest using AES-256 or equivalent encryption.",
        "implementation_guidance": "1. Enable default encryption on {cloud_provider} storage (S3, EBS, RDS)\n2. Use KMS-managed keys for encryption\n3. Implement key rotation (annual minimum)\n4. Encrypt database storage and backups\n5. Encrypt endpoint hard drives (BitLocker/FileVault)",
        "test_procedure": "1. Verify encryption is enabled on all storage services\n2. Confirm KMS key rotation is configured\n3. Check that database encryption is active\n4. Verify endpoint encryption compliance",
        "automation_level": "automated",
        "variables": {"cloud_provider": "AWS"},
        "requirement_codes": ["CC6.1", "CC6.7"],
    },
    {
        "template_code": "DP-002",
        "title": "Data Classification Policy",
        "domain": "Data Protection",
        "description": "Establish and enforce a data classification policy to categorize and protect data based on sensitivity.",
        "implementation_guidance": "1. Define classification levels (Public, Internal, Confidential, Restricted)\n2. Create classification criteria and examples\n3. Train employees on classification procedures\n4. Label data stores with classification levels\n5. Map handling requirements to each level",
        "test_procedure": "1. Review data classification policy document\n2. Verify employee training completion\n3. Spot-check data stores for proper classification\n4. Confirm handling procedures are followed",
        "automation_level": "manual",
        "variables": {},
        "requirement_codes": ["CC6.1", "CC6.5"],
    },
    {
        "template_code": "DP-003",
        "title": "Backup and Recovery",
        "domain": "Data Protection",
        "description": "Implement automated backup procedures with tested recovery capabilities.",
        "implementation_guidance": "1. Configure automated daily backups for all databases\n2. Store backups in geographically separate {cloud_provider} region\n3. Encrypt backups using KMS keys\n4. Implement backup retention policy (30 days minimum)\n5. Test restoration quarterly",
        "test_procedure": "1. Verify backup schedules are running\n2. Confirm backup encryption and cross-region storage\n3. Review most recent restoration test results\n4. Validate backup retention compliance",
        "automation_level": "automated",
        "variables": {"cloud_provider": "AWS"},
        "requirement_codes": ["CC7.5"],
    },
    # Change Management (3)
    {
        "template_code": "CM-001",
        "title": "Change Management Process",
        "domain": "Change Management",
        "description": "Implement a formal change management process for all production changes.",
        "implementation_guidance": "1. Define change request workflow (request, review, approve, implement, verify)\n2. Use ticketing system for all change requests\n3. Classify changes by risk level\n4. Require approval from change advisory board for high-risk changes\n5. Document rollback procedures for each change",
        "test_procedure": "1. Review recent production changes for process compliance\n2. Verify all changes have associated tickets\n3. Confirm approvals were obtained before implementation\n4. Check that rollback procedures are documented",
        "automation_level": "semi_automated",
        "variables": {},
        "requirement_codes": ["CC8.1"],
    },
    {
        "template_code": "CM-002",
        "title": "Code Review Requirements",
        "domain": "Change Management",
        "description": "Require peer code review for all production code changes before deployment.",
        "implementation_guidance": "1. Configure branch protection rules requiring reviews\n2. Require minimum one approving review before merge\n3. Enable CODEOWNERS for critical paths\n4. Prohibit self-approval of pull requests\n5. Require review re-approval after force push",
        "test_procedure": "1. Verify branch protection is enabled on main branches\n2. Review recent merges for approval compliance\n3. Confirm no self-approvals occurred\n4. Check CODEOWNERS file coverage",
        "automation_level": "automated",
        "variables": {},
        "requirement_codes": ["CC8.1"],
    },
    {
        "template_code": "CM-003",
        "title": "CI/CD Pipeline Security",
        "domain": "Change Management",
        "description": "Secure the CI/CD pipeline with automated testing, scanning, and deployment controls.",
        "implementation_guidance": "1. Implement automated unit and integration tests in pipeline\n2. Add static analysis (SAST) scanning\n3. Add dependency vulnerability scanning (SCA)\n4. Require all checks to pass before deployment\n5. Implement deployment approval gates for production",
        "test_procedure": "1. Review pipeline configuration for required checks\n2. Verify SAST and SCA scanning is active\n3. Confirm deployment gates are enforced\n4. Test that failed checks block deployment",
        "automation_level": "automated",
        "variables": {},
        "requirement_codes": ["CC8.1", "CC7.1"],
    },
    # Logging & Monitoring (4)
    {
        "template_code": "LM-001",
        "title": "Centralized Logging",
        "domain": "Logging & Monitoring",
        "description": "Implement centralized log collection and storage for all systems and applications.",
        "implementation_guidance": "1. Deploy centralized logging solution (e.g., {cloud_provider} CloudWatch, ELK)\n2. Configure all servers and applications to ship logs\n3. Implement log retention policy (1 year minimum)\n4. Protect logs from tampering with immutable storage\n5. Index logs for searchability and alerting",
        "test_procedure": "1. Verify all systems are shipping logs\n2. Confirm log retention meets policy requirements\n3. Test log search and query capabilities\n4. Verify log integrity controls",
        "automation_level": "automated",
        "variables": {"cloud_provider": "AWS"},
        "requirement_codes": ["CC7.2"],
    },
    {
        "template_code": "LM-002",
        "title": "Security Alerting",
        "domain": "Logging & Monitoring",
        "description": "Configure automated alerts for security-relevant events and anomalies.",
        "implementation_guidance": "1. Define alerting rules for critical security events\n2. Configure alerts for failed login attempts, privilege escalation, unusual access patterns\n3. Set up on-call rotation for alert response\n4. Implement alert escalation procedures\n5. Review and tune alerts monthly to reduce noise",
        "test_procedure": "1. Review configured alerting rules\n2. Verify alerts fire correctly for test scenarios\n3. Confirm on-call rotation is active\n4. Review alert response times from last month",
        "automation_level": "automated",
        "variables": {},
        "requirement_codes": ["CC7.2", "CC7.3"],
    },
    {
        "template_code": "LM-003",
        "title": "Intrusion Detection System",
        "domain": "Logging & Monitoring",
        "description": "Deploy intrusion detection to identify unauthorized access attempts and suspicious activity.",
        "implementation_guidance": "1. Deploy network-based IDS ({cloud_provider} GuardDuty or equivalent)\n2. Configure IDS rules for known attack patterns\n3. Integrate IDS alerts with SIEM\n4. Review IDS findings weekly\n5. Tune IDS to reduce false positives",
        "test_procedure": "1. Verify IDS is deployed and active\n2. Review recent IDS findings\n3. Confirm integration with alerting system\n4. Check tuning and false positive rates",
        "automation_level": "automated",
        "variables": {"cloud_provider": "AWS"},
        "requirement_codes": ["CC6.6", "CC7.2"],
    },
    {
        "template_code": "LM-004",
        "title": "Vulnerability Scanning",
        "domain": "Logging & Monitoring",
        "description": "Perform regular vulnerability scanning of infrastructure and applications.",
        "implementation_guidance": "1. Deploy automated vulnerability scanner\n2. Schedule weekly infrastructure scans\n3. Integrate scanning into CI/CD pipeline for application code\n4. Define remediation SLAs by severity (Critical: 7 days, High: 30 days)\n5. Track remediation progress and report monthly",
        "test_procedure": "1. Review latest vulnerability scan reports\n2. Verify scanning frequency meets policy\n3. Check remediation SLA compliance\n4. Confirm critical vulnerabilities are addressed within SLA",
        "automation_level": "automated",
        "variables": {},
        "requirement_codes": ["CC7.1", "CC4.1"],
    },
    # Incident Response (2)
    {
        "template_code": "IR-001",
        "title": "Incident Response Plan",
        "domain": "Incident Response",
        "description": "Develop and maintain a comprehensive incident response plan.",
        "implementation_guidance": "1. Document incident response plan covering identification, containment, eradication, recovery, and lessons learned\n2. Define incident severity levels and response procedures\n3. Establish incident response team and roles\n4. Conduct tabletop exercises annually\n5. Update plan based on lessons learned",
        "test_procedure": "1. Review incident response plan document\n2. Verify plan was updated within last 12 months\n3. Confirm tabletop exercise was conducted\n4. Review lessons learned from recent incidents",
        "automation_level": "manual",
        "variables": {},
        "requirement_codes": ["CC7.3", "CC7.4"],
    },
    {
        "template_code": "IR-002",
        "title": "Incident Response Runbooks",
        "domain": "Incident Response",
        "description": "Create specific runbooks for common incident types to enable consistent and rapid response.",
        "implementation_guidance": "1. Create runbooks for: data breach, ransomware, DDoS, insider threat, account compromise\n2. Include step-by-step response procedures\n3. Define communication templates and escalation paths\n4. Store runbooks in accessible, version-controlled location\n5. Review and update runbooks semi-annually",
        "test_procedure": "1. Verify runbooks exist for each incident type\n2. Confirm runbooks are version-controlled\n3. Check last review date\n4. Validate communication templates are current",
        "automation_level": "manual",
        "variables": {},
        "requirement_codes": ["CC7.4"],
    },
    # Endpoint Security (2)
    {
        "template_code": "ES-001",
        "title": "Endpoint Detection and Response (EDR)",
        "domain": "Endpoint Security",
        "description": "Deploy EDR solution on all endpoints to detect and respond to security threats.",
        "implementation_guidance": "1. Deploy EDR agent on all company endpoints\n2. Configure real-time threat detection\n3. Enable automated response for known threats\n4. Integrate EDR alerts with SIEM\n5. Monitor EDR coverage and health",
        "test_procedure": "1. Verify EDR coverage across all endpoints\n2. Confirm real-time detection is active\n3. Review recent threat detections and responses\n4. Check EDR agent health status",
        "automation_level": "automated",
        "variables": {},
        "requirement_codes": ["CC6.8"],
    },
    {
        "template_code": "ES-002",
        "title": "Patch Management",
        "domain": "Endpoint Security",
        "description": "Implement automated patch management for operating systems and applications.",
        "implementation_guidance": "1. Deploy patch management solution\n2. Configure automated patching schedule\n3. Define patching SLAs (Critical: 72 hours, High: 14 days, Medium: 30 days)\n4. Test patches before production deployment\n5. Report patch compliance monthly",
        "test_procedure": "1. Review patch compliance report\n2. Verify patching schedule is active\n3. Check SLA compliance for recent patches\n4. Confirm rollback procedures exist",
        "automation_level": "automated",
        "variables": {},
        "requirement_codes": ["CC7.1", "CC6.8"],
    },
    # HR Security (2)
    {
        "template_code": "HR-001",
        "title": "Background Checks",
        "domain": "HR Security",
        "description": "Conduct background checks on all new employees before granting system access.",
        "implementation_guidance": "1. Define background check requirements by role\n2. Conduct checks before start date\n3. Verify education and employment history\n4. Conduct criminal background check where legally permitted\n5. Document results and retain securely",
        "test_procedure": "1. Review recent hires for background check completion\n2. Verify checks were completed before access was granted\n3. Confirm documentation is securely stored\n4. Check policy compliance rates",
        "automation_level": "manual",
        "variables": {},
        "requirement_codes": ["CC1.4"],
    },
    {
        "template_code": "HR-002",
        "title": "Security Awareness Training",
        "domain": "HR Security",
        "description": "Conduct annual security awareness training for all employees.",
        "implementation_guidance": "1. Deploy security awareness training platform\n2. Create training modules covering phishing, data handling, password hygiene, incident reporting\n3. Require completion within 30 days of hire and annually thereafter\n4. Conduct periodic phishing simulations\n5. Track and report completion rates",
        "test_procedure": "1. Verify training platform is deployed\n2. Review completion rates (target: 95%+)\n3. Check phishing simulation results\n4. Confirm new hires complete training within 30 days",
        "automation_level": "semi_automated",
        "variables": {},
        "requirement_codes": ["CC1.4", "CC2.2"],
    },
]


async def seed_control_templates(db, framework=None):
    from app.models.control_template import ControlTemplate
    from app.models.control_template_framework_mapping import ControlTemplateFrameworkMapping
    from sqlalchemy import select

    # Check if already seeded
    existing = await db.execute(select(ControlTemplate).limit(1))
    if existing.scalar_one_or_none():
        print("Control templates already seeded, skipping.")
        return

    for tmpl_data in CONTROL_TEMPLATES:
        req_codes = tmpl_data.pop("requirement_codes", [])
        template = ControlTemplate(**tmpl_data)
        db.add(template)
        await db.flush()

        if framework:
            for code in req_codes:
                mapping = ControlTemplateFrameworkMapping(
                    control_template_id=template.id,
                    framework_id=framework.id,
                    requirement_code=code,
                )
                db.add(mapping)

    await db.commit()
    print(f"Seeded {len(CONTROL_TEMPLATES)} control templates.")
