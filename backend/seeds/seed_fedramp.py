"""FedRAMP (Federal Risk and Authorization Management Program) — framework seed data."""

FEDRAMP_FRAMEWORK = {
    "name": "FedRAMP",
    "version": "Rev 5",
    "category": "Government & Federal",
    "description": "Federal Risk and Authorization Management Program (FedRAMP) — a government-wide program that provides a standardized approach to security assessment, authorization, and continuous monitoring for cloud products and services used by federal agencies.",
    "domains": [
        {
            "code": "AC",
            "name": "Access Control",
            "description": "FedRAMP access control requirements for cloud service providers, including account management, access enforcement, information flow enforcement, and remote access controls.",
            "sort_order": 1,
            "requirements": [
                {
                    "code": "FedRAMP-AC-1",
                    "title": "Access Control Policy and Procedures",
                    "description": "Develop, document, and disseminate an access control policy specific to the cloud service offering that addresses purpose, scope, roles, responsibilities, and compliance with FedRAMP requirements.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "FedRAMP-AC-1a", "title": "CSP access control policy is FedRAMP-compliant", "sort_order": 1},
                    ],
                },
                {
                    "code": "FedRAMP-AC-2",
                    "title": "Account Management",
                    "description": "Manage information system accounts including identifying account types, establishing conditions for group membership, assigning account managers, and requiring approval for account requests with FedRAMP-specific parameters.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "FedRAMP-AC-2a", "title": "CSP account management meets FedRAMP baseline requirements", "sort_order": 1},
                        {"code": "FedRAMP-AC-2b", "title": "Customer-managed accounts are segregated from CSP accounts", "sort_order": 2},
                    ],
                },
                {
                    "code": "FedRAMP-AC-4",
                    "title": "Information Flow Enforcement",
                    "description": "Enforce approved authorizations for controlling the flow of information within the system and between interconnected systems based on FedRAMP-defined flow control policies.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "FedRAMP-AC-4a", "title": "Information flow between tenants is controlled", "sort_order": 1},
                    ],
                },
                {
                    "code": "FedRAMP-AC-17",
                    "title": "Remote Access",
                    "description": "Establish and document usage restrictions, configuration requirements, and implementation guidance for each type of remote access allowed, and authorize remote access prior to allowing connections.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "FedRAMP-AC-17a", "title": "Remote access is authorized and encrypted", "sort_order": 1},
                        {"code": "FedRAMP-AC-17b", "title": "Remote access sessions are monitored and controlled", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "AU",
            "name": "Audit and Accountability",
            "description": "FedRAMP audit requirements for cloud environments including event logging, audit record content, audit storage, and audit record generation.",
            "sort_order": 2,
            "requirements": [
                {
                    "code": "FedRAMP-AU-2",
                    "title": "Event Logging",
                    "description": "Identify the types of events that the cloud system is capable of logging, including FedRAMP-required event types such as successful and unsuccessful logon attempts, privileged function use, and security-relevant configuration changes.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "FedRAMP-AU-2a", "title": "FedRAMP-required event types are logged", "sort_order": 1},
                        {"code": "FedRAMP-AU-2b", "title": "Customer audit events are captured and available", "sort_order": 2},
                    ],
                },
                {
                    "code": "FedRAMP-AU-6",
                    "title": "Audit Record Review, Analysis, and Reporting",
                    "description": "Review and analyze audit records at least weekly for indications of inappropriate or unusual activity, and report findings to the organization's ISSO and FedRAMP PMO as required.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "FedRAMP-AU-6a", "title": "Audit records are reviewed weekly at minimum", "sort_order": 1},
                    ],
                },
                {
                    "code": "FedRAMP-AU-9",
                    "title": "Protection of Audit Information",
                    "description": "Protect audit information and audit logging tools from unauthorized access, modification, and deletion in the cloud environment.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "FedRAMP-AU-9a", "title": "Audit data integrity is protected in the cloud environment", "sort_order": 1},
                    ],
                },
                {
                    "code": "FedRAMP-AU-11",
                    "title": "Audit Record Retention",
                    "description": "Retain audit records for at least one year to provide support for after-the-fact investigations of security incidents and to meet FedRAMP retention requirements.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "FedRAMP-AU-11a", "title": "Audit records are retained for at least one year", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CM",
            "name": "Configuration Management",
            "description": "FedRAMP configuration management requirements including baseline configuration, change control, and configuration settings for cloud service offerings.",
            "sort_order": 3,
            "requirements": [
                {
                    "code": "FedRAMP-CM-2",
                    "title": "Baseline Configuration",
                    "description": "Develop, document, and maintain a current baseline configuration of the cloud information system that is reviewed and updated at least annually and as an integral part of system component installations and upgrades.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "FedRAMP-CM-2a", "title": "CSO baseline configuration is documented and maintained", "sort_order": 1},
                    ],
                },
                {
                    "code": "FedRAMP-CM-3",
                    "title": "Configuration Change Control",
                    "description": "Determine the types of changes that are configuration-controlled, employ a configuration change control process, and document changes to the cloud environment per FedRAMP requirements.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "FedRAMP-CM-3a", "title": "Configuration changes follow FedRAMP change control process", "sort_order": 1},
                        {"code": "FedRAMP-CM-3b", "title": "Significant changes trigger FedRAMP reassessment", "sort_order": 2},
                    ],
                },
                {
                    "code": "FedRAMP-CM-6",
                    "title": "Configuration Settings",
                    "description": "Establish and document mandatory configuration settings for IT products employed in the cloud environment using USGCB or CIS benchmarks.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "FedRAMP-CM-6a", "title": "Configuration settings align with USGCB or CIS benchmarks", "sort_order": 1},
                    ],
                },
                {
                    "code": "FedRAMP-CM-8",
                    "title": "System Component Inventory",
                    "description": "Develop and maintain an accurate, up-to-date inventory of all system components for the cloud service offering, including hardware, software, and firmware.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "FedRAMP-CM-8a", "title": "CSO component inventory is accurate and up-to-date", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CP",
            "name": "Contingency Planning",
            "description": "FedRAMP contingency planning requirements for cloud service providers including contingency plans, testing, alternate processing sites, and system backups.",
            "sort_order": 4,
            "requirements": [
                {
                    "code": "FedRAMP-CP-2",
                    "title": "Contingency Plan",
                    "description": "Develop a contingency plan for the cloud service offering that identifies essential missions and business functions, provides recovery objectives, and addresses reconstitution to original state.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "FedRAMP-CP-2a", "title": "CSO contingency plan is developed and approved", "sort_order": 1},
                        {"code": "FedRAMP-CP-2b", "title": "Contingency plan addresses multi-tenant recovery", "sort_order": 2},
                    ],
                },
                {
                    "code": "FedRAMP-CP-4",
                    "title": "Contingency Plan Testing",
                    "description": "Test the contingency plan at least annually using tabletop exercises or functional tests to determine the plan's effectiveness and the organization's readiness to execute the plan.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "FedRAMP-CP-4a", "title": "Contingency plan is tested annually", "sort_order": 1},
                    ],
                },
                {
                    "code": "FedRAMP-CP-9",
                    "title": "System Backup",
                    "description": "Conduct backups of user-level and system-level information, protect backup confidentiality, integrity, and availability, and test backup integrity at defined intervals.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "FedRAMP-CP-9a", "title": "System and data backups are performed per FedRAMP requirements", "sort_order": 1},
                        {"code": "FedRAMP-CP-9b", "title": "Backup restoration is tested regularly", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "IA",
            "name": "Identification and Authentication",
            "description": "FedRAMP identification and authentication requirements including multi-factor authentication, identifier management, and authenticator management for cloud environments.",
            "sort_order": 5,
            "requirements": [
                {
                    "code": "FedRAMP-IA-2",
                    "title": "Identification and Authentication (Organizational Users)",
                    "description": "Uniquely identify and authenticate organizational users and implement multi-factor authentication for all privileged and non-privileged network access to the cloud service offering.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "FedRAMP-IA-2a", "title": "MFA is required for all privileged access", "sort_order": 1},
                        {"code": "FedRAMP-IA-2b", "title": "MFA is required for non-privileged network access", "sort_order": 2},
                    ],
                },
                {
                    "code": "FedRAMP-IA-5",
                    "title": "Authenticator Management",
                    "description": "Manage cloud system authenticators by verifying identity, establishing initial authenticator content, ensuring sufficient strength of mechanism, and changing default authenticators prior to deployment.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "FedRAMP-IA-5a", "title": "Authenticator strength meets FedRAMP minimums", "sort_order": 1},
                    ],
                },
                {
                    "code": "FedRAMP-IA-8",
                    "title": "Identification and Authentication (Non-Organizational Users)",
                    "description": "Uniquely identify and authenticate non-organizational users or processes acting on behalf of non-organizational users accessing the cloud service.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "FedRAMP-IA-8a", "title": "Non-organizational users are uniquely identified and authenticated", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "IR",
            "name": "Incident Response",
            "description": "FedRAMP incident response requirements for cloud service providers including incident handling, reporting to US-CERT, and incident monitoring.",
            "sort_order": 6,
            "requirements": [
                {
                    "code": "FedRAMP-IR-4",
                    "title": "Incident Handling",
                    "description": "Implement an incident handling capability that includes preparation, detection and analysis, containment, eradication, and recovery, with FedRAMP-specific reporting requirements.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "FedRAMP-IR-4a", "title": "Incident handling covers full lifecycle with FedRAMP reporting", "sort_order": 1},
                    ],
                },
                {
                    "code": "FedRAMP-IR-6",
                    "title": "Incident Reporting",
                    "description": "Report security incidents to US-CERT within required timeframes and notify affected federal agencies and the FedRAMP PMO of incidents affecting the confidentiality, integrity, or availability of federal data.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "FedRAMP-IR-6a", "title": "Incidents are reported to US-CERT within required timeframes", "sort_order": 1},
                        {"code": "FedRAMP-IR-6b", "title": "Affected federal agencies are notified", "sort_order": 2},
                    ],
                },
                {
                    "code": "FedRAMP-IR-8",
                    "title": "Incident Response Plan",
                    "description": "Develop an incident response plan that provides the organization with a roadmap for implementing its incident response capability, is reviewed and approved by designated officials, and is distributed to incident response personnel.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "FedRAMP-IR-8a", "title": "Incident response plan is FedRAMP-compliant", "sort_order": 1},
                    ],
                },
                {
                    "code": "FedRAMP-IR-9",
                    "title": "Information Spillage Response",
                    "description": "Respond to information spills involving federal data by identifying contaminated systems, isolating affected components, and reporting to the appropriate federal agencies.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "FedRAMP-IR-9a", "title": "Information spillage response procedures are documented", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "RA",
            "name": "Risk Assessment",
            "description": "FedRAMP risk assessment requirements including vulnerability scanning, risk assessment methodology, and continuous monitoring of the cloud service offering.",
            "sort_order": 7,
            "requirements": [
                {
                    "code": "FedRAMP-RA-3",
                    "title": "Risk Assessment",
                    "description": "Conduct risk assessments of the cloud service offering at least annually, or whenever there are significant changes to the system, and provide results to designated officials.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "FedRAMP-RA-3a", "title": "Annual risk assessment is conducted for the CSO", "sort_order": 1},
                    ],
                },
                {
                    "code": "FedRAMP-RA-5",
                    "title": "Vulnerability Monitoring and Scanning",
                    "description": "Scan for vulnerabilities in the cloud environment monthly for operating systems, databases, and web applications, and when new vulnerabilities are identified. Submit scan results to FedRAMP as required.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "FedRAMP-RA-5a", "title": "Monthly vulnerability scans are performed", "sort_order": 1},
                        {"code": "FedRAMP-RA-5b", "title": "Scan results are submitted per FedRAMP ConMon requirements", "sort_order": 2},
                        {"code": "FedRAMP-RA-5c", "title": "High vulnerabilities are remediated within 30 days", "sort_order": 3},
                    ],
                },
            ],
        },
        {
            "code": "SC",
            "name": "System and Communications Protection",
            "description": "FedRAMP system and communications protection requirements including boundary protection, transmission confidentiality, cryptographic protection, and multi-tenant isolation.",
            "sort_order": 8,
            "requirements": [
                {
                    "code": "FedRAMP-SC-7",
                    "title": "Boundary Protection",
                    "description": "Monitor and control communications at the external managed interfaces to the cloud system and at key internal managed interfaces, implementing subnetworks for publicly accessible system components.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "FedRAMP-SC-7a", "title": "Boundary protection isolates CSO from other services", "sort_order": 1},
                        {"code": "FedRAMP-SC-7b", "title": "Multi-tenant isolation is implemented", "sort_order": 2},
                    ],
                },
                {
                    "code": "FedRAMP-SC-8",
                    "title": "Transmission Confidentiality and Integrity",
                    "description": "Protect the confidentiality and integrity of transmitted federal data using FIPS 140-2/140-3 validated cryptographic mechanisms.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "FedRAMP-SC-8a", "title": "FIPS-validated encryption protects data in transit", "sort_order": 1},
                    ],
                },
                {
                    "code": "FedRAMP-SC-12",
                    "title": "Cryptographic Key Establishment and Management",
                    "description": "Establish and manage cryptographic keys using NIST-approved key management technology and processes, with FIPS 140-2/140-3 validated cryptographic modules.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "FedRAMP-SC-12a", "title": "FIPS-validated cryptographic modules are used", "sort_order": 1},
                    ],
                },
                {
                    "code": "FedRAMP-SC-28",
                    "title": "Protection of Information at Rest",
                    "description": "Protect the confidentiality and integrity of federal information at rest using FIPS-validated cryptographic mechanisms.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "FedRAMP-SC-28a", "title": "Federal data at rest is encrypted with FIPS-validated cryptography", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "SI",
            "name": "System and Information Integrity",
            "description": "FedRAMP system and information integrity requirements including flaw remediation, malicious code protection, system monitoring, and security alerts for cloud environments.",
            "sort_order": 9,
            "requirements": [
                {
                    "code": "FedRAMP-SI-2",
                    "title": "Flaw Remediation",
                    "description": "Identify, report, and correct cloud system flaws, test software updates for effectiveness, and install security-relevant updates within FedRAMP-defined timeframes based on severity.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "FedRAMP-SI-2a", "title": "Critical patches are applied within FedRAMP timeframes", "sort_order": 1},
                        {"code": "FedRAMP-SI-2b", "title": "Patch status is included in monthly ConMon reporting", "sort_order": 2},
                    ],
                },
                {
                    "code": "FedRAMP-SI-3",
                    "title": "Malicious Code Protection",
                    "description": "Implement malicious code protection at cloud system entry and exit points, and update malicious code protection mechanisms as new releases are available per FedRAMP requirements.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "FedRAMP-SI-3a", "title": "Malware protection is deployed and updated in the CSO", "sort_order": 1},
                    ],
                },
                {
                    "code": "FedRAMP-SI-4",
                    "title": "System Monitoring",
                    "description": "Monitor the cloud system to detect attacks, indicators of potential attacks, unauthorized local, network, and remote connections, and provide monitoring output to FedRAMP as required.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "FedRAMP-SI-4a", "title": "Continuous monitoring detects attacks and anomalies", "sort_order": 1},
                        {"code": "FedRAMP-SI-4b", "title": "Monitoring data supports FedRAMP ConMon requirements", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "CA",
            "name": "Security Assessment and Authorization",
            "description": "FedRAMP-specific security assessment and authorization requirements including 3PAO assessment, POA&M management, continuous monitoring, and authorization boundary definition.",
            "sort_order": 10,
            "requirements": [
                {
                    "code": "FedRAMP-CA-2",
                    "title": "3PAO Security Assessment",
                    "description": "Engage a FedRAMP-approved Third Party Assessment Organization (3PAO) to conduct an independent assessment of security controls, produce a Security Assessment Report (SAR), and identify vulnerabilities.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "FedRAMP-CA-2a", "title": "3PAO assessment is conducted by approved assessor", "sort_order": 1},
                        {"code": "FedRAMP-CA-2b", "title": "Security Assessment Report (SAR) is produced", "sort_order": 2},
                    ],
                },
                {
                    "code": "FedRAMP-CA-5",
                    "title": "Plan of Action and Milestones (POA&M)",
                    "description": "Develop and maintain a POA&M that documents planned remediation actions to correct weaknesses, track progress, and submit monthly updates to the FedRAMP PMO.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "FedRAMP-CA-5a", "title": "POA&M is maintained with monthly updates", "sort_order": 1},
                        {"code": "FedRAMP-CA-5b", "title": "POA&M remediation timelines meet FedRAMP requirements", "sort_order": 2},
                    ],
                },
                {
                    "code": "FedRAMP-CA-7",
                    "title": "Continuous Monitoring (ConMon)",
                    "description": "Implement the FedRAMP continuous monitoring program including monthly vulnerability scanning, annual assessments, POA&M management, and significant change reporting.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "FedRAMP-CA-7a", "title": "FedRAMP ConMon deliverables are submitted monthly", "sort_order": 1},
                        {"code": "FedRAMP-CA-7b", "title": "Annual assessment is conducted by 3PAO", "sort_order": 2},
                        {"code": "FedRAMP-CA-7c", "title": "Significant changes are reported and assessed", "sort_order": 3},
                    ],
                },
                {
                    "code": "FedRAMP-CA-9",
                    "title": "Internal System Connections",
                    "description": "Authorize internal connections of information system components and document for each connection the interface characteristics, security requirements, and the nature of the information communicated.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "FedRAMP-CA-9a", "title": "Internal system connections are authorized and documented", "sort_order": 1},
                    ],
                },
            ],
        },
    ],
}


async def seed_fedramp_framework(db):
    """Seed the FedRAMP framework."""
    from sqlalchemy import select
    from app.models.framework import Framework
    from app.models.framework_domain import FrameworkDomain
    from app.models.framework_requirement import FrameworkRequirement
    from app.models.control_objective import ControlObjective

    # Check if already seeded
    existing = await db.execute(
        select(Framework).where(Framework.name == FEDRAMP_FRAMEWORK["name"])
    )
    if existing.scalar_one_or_none():
        print("  -> FedRAMP framework already seeded, skipping.")
        return

    fw_data = FEDRAMP_FRAMEWORK
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
    print(f"  Seeded FedRAMP: {req_count} requirements, {obj_count} objectives.")
    return framework
