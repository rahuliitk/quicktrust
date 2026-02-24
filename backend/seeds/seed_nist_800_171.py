"""NIST 800-171 Rev 3 — Protecting Controlled Unclassified Information (CUI) — framework seed data."""

NIST_800_171_FRAMEWORK = {
    "name": "NIST 800-171",
    "version": "Rev 3",
    "category": "Security & Compliance",
    "description": "NIST Special Publication 800-171 Revision 3 — Protecting Controlled Unclassified Information in Nonfederal Systems and Organizations. Provides recommended security requirements for protecting CUI.",
    "domains": [
        {
            "code": "3.1",
            "name": "Access Control",
            "description": "Limit system access to authorized users, processes acting on behalf of authorized users, and devices, and limit transactions and functions that authorized users are permitted to execute.",
            "sort_order": 1,
            "requirements": [
                {
                    "code": "3.1.1",
                    "title": "Authorized Access Control",
                    "description": "Limit system access to authorized users, processes acting on behalf of authorized users, and devices (including other systems).",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "3.1.1a", "title": "System access is limited to authorized users", "sort_order": 1},
                        {"code": "3.1.1b", "title": "Device access is controlled and authorized", "sort_order": 2},
                    ],
                },
                {
                    "code": "3.1.2",
                    "title": "Transaction and Function Control",
                    "description": "Limit system access to the types of transactions and functions that authorized users are permitted to execute.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "3.1.2a", "title": "Authorized transactions are defined and enforced", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.1.3",
                    "title": "CUI Flow Enforcement",
                    "description": "Control the flow of CUI in accordance with approved authorizations.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "3.1.3a", "title": "CUI flow controls are implemented and enforced", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.1.5",
                    "title": "Least Privilege",
                    "description": "Employ the principle of least privilege, including for specific security functions and privileged accounts.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "3.1.5a", "title": "Least privilege is enforced for all accounts", "sort_order": 1},
                        {"code": "3.1.5b", "title": "Privileged accounts are restricted to security functions", "sort_order": 2},
                    ],
                },
                {
                    "code": "3.1.7",
                    "title": "Unsuccessful Logon Attempts",
                    "description": "Limit unsuccessful logon attempts and enforce a defined delay or lockout after a defined number of consecutive invalid logon attempts.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "3.1.7a", "title": "Account lockout is enforced after failed logon attempts", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "3.2",
            "name": "Awareness and Training",
            "description": "Ensure that managers, systems administrators, and users of organizational systems are made aware of the security risks associated with their activities and of applicable policies.",
            "sort_order": 2,
            "requirements": [
                {
                    "code": "3.2.1",
                    "title": "Security Awareness",
                    "description": "Ensure that managers, systems administrators, and users of organizational systems are made aware of the security risks associated with their activities and of the applicable policies, standards, and procedures related to the security of those systems.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "3.2.1a", "title": "Security awareness training is provided to all personnel", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.2.2",
                    "title": "Role-Based Training",
                    "description": "Ensure that personnel are trained to carry out their assigned information security-related duties and responsibilities.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "3.2.2a", "title": "Role-based security training is provided", "sort_order": 1},
                        {"code": "3.2.2b", "title": "Training addresses CUI handling procedures", "sort_order": 2},
                    ],
                },
                {
                    "code": "3.2.3",
                    "title": "Insider Threat Awareness",
                    "description": "Provide security awareness training on recognizing and reporting potential indicators of insider threat.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "3.2.3a", "title": "Insider threat awareness training is delivered", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "3.3",
            "name": "Audit and Accountability",
            "description": "Create and retain system audit logs and records to the extent needed to enable the monitoring, analysis, investigation, and reporting of unlawful or unauthorized system activity.",
            "sort_order": 3,
            "requirements": [
                {
                    "code": "3.3.1",
                    "title": "System Auditing",
                    "description": "Create and retain system audit logs and records to the extent needed to enable the monitoring, analysis, investigation, and reporting of unlawful or unauthorized system activity.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "3.3.1a", "title": "Audit logs are created for defined events", "sort_order": 1},
                        {"code": "3.3.1b", "title": "Audit records are retained for defined period", "sort_order": 2},
                    ],
                },
                {
                    "code": "3.3.2",
                    "title": "User Accountability",
                    "description": "Ensure that the actions of individual system users can be uniquely traced to those users so they can be held accountable for their actions.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "3.3.2a", "title": "User actions are traceable to individual accounts", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.3.4",
                    "title": "Audit Logging Failure Alerts",
                    "description": "Alert designated personnel in the event of an audit logging process failure.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "3.3.4a", "title": "Alerts are generated on audit logging failures", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.3.5",
                    "title": "Audit Review and Analysis",
                    "description": "Correlate audit record review, analysis, and reporting processes for investigation and response to indications of unlawful, unauthorized, suspicious, or unusual activity.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "3.3.5a", "title": "Audit records are reviewed and correlated", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "3.4",
            "name": "Configuration Management",
            "description": "Establish and maintain baseline configurations and inventories of organizational systems (including hardware, software, firmware, and documentation) throughout the respective system development life cycles.",
            "sort_order": 4,
            "requirements": [
                {
                    "code": "3.4.1",
                    "title": "Baseline Configuration",
                    "description": "Establish and maintain baseline configurations and inventories of organizational systems throughout the respective system development life cycles.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "3.4.1a", "title": "Baseline configurations are established and maintained", "sort_order": 1},
                        {"code": "3.4.1b", "title": "System inventories are maintained", "sort_order": 2},
                    ],
                },
                {
                    "code": "3.4.2",
                    "title": "Security Configuration Enforcement",
                    "description": "Establish and enforce security configuration settings for information technology products employed in organizational systems.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "3.4.2a", "title": "Security configuration settings are documented and enforced", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.4.3",
                    "title": "System Change Tracking",
                    "description": "Track, review, approve or disapprove, and log changes to organizational systems.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "3.4.3a", "title": "System changes are tracked and approved", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.4.5",
                    "title": "Access Restrictions for Change",
                    "description": "Define, document, approve, and enforce physical and logical access restrictions associated with changes to organizational systems.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "3.4.5a", "title": "Access restrictions for system changes are enforced", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "3.5",
            "name": "Identification and Authentication",
            "description": "Identify system users, processes acting on behalf of users, and devices, and authenticate the identities of those users, processes, or devices before allowing access to organizational systems.",
            "sort_order": 5,
            "requirements": [
                {
                    "code": "3.5.1",
                    "title": "User Identification",
                    "description": "Identify system users, processes acting on behalf of users, and devices.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "3.5.1a", "title": "System users and devices are uniquely identified", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.5.2",
                    "title": "Authentication of Users",
                    "description": "Authenticate (or verify) the identities of users, processes, or devices, as a prerequisite to allowing access to organizational systems.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "3.5.2a", "title": "User authentication is required before system access", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.5.3",
                    "title": "Multi-Factor Authentication",
                    "description": "Use multi-factor authentication for local and network access to privileged accounts and for network access to non-privileged accounts.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "3.5.3a", "title": "MFA is enforced for privileged access", "sort_order": 1},
                        {"code": "3.5.3b", "title": "MFA is enforced for network access to non-privileged accounts", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "3.6",
            "name": "Incident Response",
            "description": "Establish an operational incident-handling capability for organizational systems that includes preparation, detection, analysis, containment, recovery, and user response activities.",
            "sort_order": 6,
            "requirements": [
                {
                    "code": "3.6.1",
                    "title": "Incident Handling",
                    "description": "Establish an operational incident-handling capability for organizational systems that includes preparation, detection, analysis, containment, recovery, and user response activities.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "3.6.1a", "title": "Incident handling capability is established", "sort_order": 1},
                        {"code": "3.6.1b", "title": "Incident handling procedures are documented", "sort_order": 2},
                    ],
                },
                {
                    "code": "3.6.2",
                    "title": "Incident Reporting",
                    "description": "Track, document, and report incidents to designated officials and/or authorities both internal and external to the organization.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "3.6.2a", "title": "Incidents are reported to designated officials", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.6.3",
                    "title": "Incident Response Testing",
                    "description": "Test the organizational incident response capability.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "3.6.3a", "title": "Incident response capability is tested regularly", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "3.7",
            "name": "Maintenance",
            "description": "Perform maintenance on organizational systems, provide controls for maintenance tools, and manage nonlocal maintenance.",
            "sort_order": 7,
            "requirements": [
                {
                    "code": "3.7.1",
                    "title": "System Maintenance",
                    "description": "Perform maintenance on organizational systems.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "3.7.1a", "title": "System maintenance is scheduled and documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.7.2",
                    "title": "Maintenance Tool Control",
                    "description": "Provide controls on the tools, techniques, mechanisms, and personnel used to conduct system maintenance.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "3.7.2a", "title": "Maintenance tools are controlled and inspected", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.7.5",
                    "title": "Nonlocal Maintenance",
                    "description": "Require multifactor authentication to establish nonlocal maintenance sessions via external network connections, and terminate such connections when nonlocal maintenance is complete.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "3.7.5a", "title": "Nonlocal maintenance requires MFA", "sort_order": 1},
                        {"code": "3.7.5b", "title": "Nonlocal maintenance sessions are terminated upon completion", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "3.8",
            "name": "Media Protection",
            "description": "Protect, limit access to, sanitize, and securely handle system media containing CUI, including both paper and digital media.",
            "sort_order": 8,
            "requirements": [
                {
                    "code": "3.8.1",
                    "title": "Media Protection",
                    "description": "Protect (i.e., physically control and securely store) system media containing CUI, both paper and digital.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "3.8.1a", "title": "CUI media is physically controlled and securely stored", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.8.3",
                    "title": "Media Sanitization",
                    "description": "Sanitize or destroy system media containing CUI before disposal or release for reuse.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "3.8.3a", "title": "CUI media is sanitized before disposal", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.8.5",
                    "title": "Media Marking",
                    "description": "Mark media with necessary CUI markings and distribution limitations.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "3.8.5a", "title": "CUI media is appropriately marked", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.8.6",
                    "title": "Portable Storage Encryption",
                    "description": "Implement cryptographic mechanisms to protect the confidentiality of CUI stored on portable storage devices.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "3.8.6a", "title": "CUI on portable storage is encrypted", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "3.9",
            "name": "Personnel Security",
            "description": "Screen individuals prior to authorizing access to systems containing CUI, and ensure that CUI is protected during and after personnel actions.",
            "sort_order": 9,
            "requirements": [
                {
                    "code": "3.9.1",
                    "title": "Personnel Screening",
                    "description": "Screen individuals prior to authorizing access to organizational systems containing CUI.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "3.9.1a", "title": "Personnel screening is conducted before CUI access", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.9.2",
                    "title": "Personnel Actions",
                    "description": "Ensure that organizational systems containing CUI are protected during and after personnel actions such as terminations and transfers.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "3.9.2a", "title": "CUI access is revoked upon termination", "sort_order": 1},
                        {"code": "3.9.2b", "title": "Access is reviewed and adjusted upon personnel transfer", "sort_order": 2},
                    ],
                },
                {
                    "code": "3.9.3",
                    "title": "Third-Party Personnel Security",
                    "description": "Ensure that third-party personnel (e.g., contractors) are subject to the same personnel security requirements as organizational personnel.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "3.9.3a", "title": "Third-party personnel meet screening requirements", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "3.10",
            "name": "Physical Protection",
            "description": "Limit physical access to systems, equipment, and the respective operating environments to authorized individuals.",
            "sort_order": 10,
            "requirements": [
                {
                    "code": "3.10.1",
                    "title": "Physical Access Limitation",
                    "description": "Limit physical access to organizational systems, equipment, and the respective operating environments to authorized individuals.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "3.10.1a", "title": "Physical access to systems is limited to authorized individuals", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.10.2",
                    "title": "Physical Access Protection and Monitoring",
                    "description": "Protect and monitor the physical facility and support infrastructure for organizational systems.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "3.10.2a", "title": "Physical facility is protected and monitored", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.10.4",
                    "title": "Physical Access Logs",
                    "description": "Maintain audit logs of physical access.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "3.10.4a", "title": "Physical access logs are maintained and reviewed", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.10.6",
                    "title": "Alternative Work Sites",
                    "description": "Enforce safeguarding measures for CUI at alternative work sites.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "3.10.6a", "title": "CUI safeguards are enforced at alternative work sites", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "3.11",
            "name": "Risk Assessment",
            "description": "Periodically assess the risk to organizational operations, assets, and individuals resulting from the operation of organizational systems and the associated processing, storage, or transmission of CUI.",
            "sort_order": 11,
            "requirements": [
                {
                    "code": "3.11.1",
                    "title": "Risk Assessment",
                    "description": "Periodically assess the risk to organizational operations (including mission, functions, image, or reputation), organizational assets, and individuals, resulting from the operation of organizational systems and the associated processing, storage, or transmission of CUI.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "3.11.1a", "title": "Risk assessments are conducted periodically", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.11.2",
                    "title": "Vulnerability Scanning",
                    "description": "Scan for vulnerabilities in organizational systems and applications periodically and when new vulnerabilities affecting those systems and applications are identified.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "3.11.2a", "title": "Vulnerability scanning is performed periodically", "sort_order": 1},
                        {"code": "3.11.2b", "title": "Identified vulnerabilities are remediated", "sort_order": 2},
                    ],
                },
                {
                    "code": "3.11.3",
                    "title": "Risk Response",
                    "description": "Remediate vulnerabilities in accordance with risk assessments.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "3.11.3a", "title": "Vulnerabilities are remediated based on risk priority", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "3.12",
            "name": "Security Assessment",
            "description": "Periodically assess the security controls in organizational systems to determine if the controls are effective in their application.",
            "sort_order": 12,
            "requirements": [
                {
                    "code": "3.12.1",
                    "title": "Security Control Assessment",
                    "description": "Periodically assess the security controls in organizational systems to determine if the controls are effective in their application.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "3.12.1a", "title": "Security controls are assessed periodically", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.12.2",
                    "title": "Plan of Action",
                    "description": "Develop and implement plans of action designed to correct deficiencies and reduce or eliminate vulnerabilities in organizational systems.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "3.12.2a", "title": "Plans of action address identified deficiencies", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.12.3",
                    "title": "Continuous Monitoring",
                    "description": "Monitor security controls on an ongoing basis to ensure the continued effectiveness of the controls.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "3.12.3a", "title": "Continuous monitoring of security controls is operational", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.12.4",
                    "title": "System Security Plan",
                    "description": "Develop, document, and periodically update system security plans that describe system boundaries, system environments of operation, how security requirements are implemented, and the relationships with or connections to other systems.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "3.12.4a", "title": "System security plan is documented and updated", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "3.13",
            "name": "System and Communications Protection",
            "description": "Monitor, control, and protect communications at the external boundaries and key internal boundaries of organizational systems.",
            "sort_order": 13,
            "requirements": [
                {
                    "code": "3.13.1",
                    "title": "Boundary Protection",
                    "description": "Monitor, control, and protect communications (i.e., information transmitted or received by organizational systems) at the external boundaries and key internal boundaries of organizational systems.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "3.13.1a", "title": "Boundary protection is implemented", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.13.2",
                    "title": "Security Architecture",
                    "description": "Employ architectural designs, software development techniques, and systems engineering principles that promote effective information security within organizational systems.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "3.13.2a", "title": "Security engineering principles are applied to system design", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.13.8",
                    "title": "CUI Transmission Confidentiality",
                    "description": "Implement cryptographic mechanisms to prevent unauthorized disclosure of CUI during transmission unless otherwise protected by alternative physical safeguards.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "3.13.8a", "title": "CUI is encrypted during transmission", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.13.11",
                    "title": "CUI Encryption at Rest",
                    "description": "Employ FIPS-validated cryptography when used to protect the confidentiality of CUI.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "3.13.11a", "title": "FIPS-validated cryptography protects CUI at rest", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.13.16",
                    "title": "CUI at Rest Protection",
                    "description": "Protect the confidentiality of CUI at rest.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "3.13.16a", "title": "CUI at rest is protected with appropriate controls", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "3.14",
            "name": "System and Information Integrity",
            "description": "Identify, report, and correct system flaws in a timely manner, provide protection from malicious code at designated locations, and monitor system security alerts and advisories.",
            "sort_order": 14,
            "requirements": [
                {
                    "code": "3.14.1",
                    "title": "Flaw Remediation",
                    "description": "Identify, report, and correct system flaws in a timely manner.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "3.14.1a", "title": "System flaws are identified and corrected timely", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.14.2",
                    "title": "Malicious Code Protection",
                    "description": "Provide protection from malicious code at designated locations within organizational systems.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "3.14.2a", "title": "Malicious code protection is deployed at designated locations", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.14.3",
                    "title": "Security Alerts and Advisories",
                    "description": "Monitor system security alerts and advisories and take action in response.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "3.14.3a", "title": "Security alerts are monitored and acted upon", "sort_order": 1},
                    ],
                },
                {
                    "code": "3.14.6",
                    "title": "System Monitoring",
                    "description": "Monitor organizational systems, including inbound and outbound communications traffic, to detect attacks and indicators of potential attacks.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "3.14.6a", "title": "System and network monitoring is operational", "sort_order": 1},
                        {"code": "3.14.6b", "title": "Indicators of potential attacks are detected", "sort_order": 2},
                    ],
                },
                {
                    "code": "3.14.7",
                    "title": "Advanced Persistent Threats",
                    "description": "Identify unauthorized use of organizational systems.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "3.14.7a", "title": "Unauthorized system use is identified", "sort_order": 1},
                    ],
                },
            ],
        },
    ],
}


async def seed_nist_800_171_framework(db):
    """Seed the NIST 800-171 Rev 3 framework."""
    from sqlalchemy import select
    from app.models.framework import Framework
    from app.models.framework_domain import FrameworkDomain
    from app.models.framework_requirement import FrameworkRequirement
    from app.models.control_objective import ControlObjective

    # Check if already seeded
    existing = await db.execute(
        select(Framework).where(Framework.name == NIST_800_171_FRAMEWORK["name"])
    )
    if existing.scalar_one_or_none():
        print("  -> NIST 800-171 framework already seeded, skipping.")
        return

    fw_data = NIST_800_171_FRAMEWORK
    framework = Framework(
        name=fw_data["name"],
        version=fw_data["version"],
        category=fw_data["category"],
        description=fw_data["description"],
    )
    db.add(framework)
    await db.flush()

    req_count = 0
    obj_count = 0

    for domain_data in fw_data["domains"]:
        domain = FrameworkDomain(
            framework_id=framework.id,
            code=domain_data["code"],
            name=domain_data["name"],
            description=domain_data["description"],
            sort_order=domain_data["sort_order"],
        )
        db.add(domain)
        await db.flush()

        for req_data in domain_data["requirements"]:
            req = FrameworkRequirement(
                domain_id=domain.id,
                code=req_data["code"],
                title=req_data["title"],
                description=req_data["description"],
                sort_order=req_data["sort_order"],
            )
            db.add(req)
            await db.flush()
            req_count += 1

            for obj_data in req_data.get("objectives", []):
                obj = ControlObjective(
                    requirement_id=req.id,
                    code=obj_data["code"],
                    title=obj_data["title"],
                    sort_order=obj_data["sort_order"],
                )
                db.add(obj)
                obj_count += 1

    await db.commit()
    print(f"  Seeded NIST 800-171: {req_count} requirements, {obj_count} objectives.")
    return framework
