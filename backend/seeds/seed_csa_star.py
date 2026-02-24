"""CSA STAR / Cloud Controls Matrix (CCM) v4 — framework seed data."""

CSA_STAR_FRAMEWORK = {
    "name": "CSA STAR (CCM)",
    "version": "v4",
    "category": "Cloud Security",
    "description": "Cloud Security Alliance (CSA) Security, Trust, Assurance and Risk (STAR) program based on the Cloud Controls Matrix (CCM) v4 — a cybersecurity control framework for cloud computing, providing a detailed understanding of security concepts and principles aligned to CSA guidance.",
    "domains": [
        {
            "code": "AIS",
            "name": "Application and Interface Security",
            "description": "Controls for securing applications and programming interfaces (APIs) in cloud environments, including secure development, data integrity, and application security testing.",
            "sort_order": 1,
            "requirements": [
                {
                    "code": "AIS-01",
                    "title": "Application and Interface Security Policy",
                    "description": "Establish, document, approve, communicate, apply, evaluate, and maintain policies and procedures for application security to provide guidance to the appropriate planning, delivery, and support of application security capabilities.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "AIS-01a", "title": "Application security policy is established and maintained", "sort_order": 1},
                    ],
                },
                {
                    "code": "AIS-02",
                    "title": "Application Security Baseline Requirements",
                    "description": "Establish, document, and maintain baseline requirements for securing different applications.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "AIS-02a", "title": "Application security baselines are defined", "sort_order": 1},
                    ],
                },
                {
                    "code": "AIS-04",
                    "title": "Secure Application Design and Development",
                    "description": "Define and implement a SDLC process for application design, development, deployment, and operation in accordance with security requirements defined by the organization.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "AIS-04a", "title": "SDLC process includes security requirements", "sort_order": 1},
                        {"code": "AIS-04b", "title": "Security testing is part of the development lifecycle", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "AAC",
            "name": "Audit Assurance and Compliance",
            "description": "Controls for planning, conducting, and managing audit activities, ensuring regulatory compliance, and providing assurance to stakeholders regarding cloud security controls.",
            "sort_order": 2,
            "requirements": [
                {
                    "code": "AAC-01",
                    "title": "Audit and Assurance Policy",
                    "description": "Establish, document, approve, communicate, apply, evaluate, and maintain audit and assurance policies and procedures.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "AAC-01a", "title": "Audit and assurance policy is established", "sort_order": 1},
                    ],
                },
                {
                    "code": "AAC-02",
                    "title": "Independent Assessments",
                    "description": "Conduct independent audit and assurance assessments according to relevant standards at least annually.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "AAC-02a", "title": "Independent assessments are conducted annually", "sort_order": 1},
                    ],
                },
                {
                    "code": "AAC-03",
                    "title": "Risk-Based Planning Assessment",
                    "description": "Perform risk-based planning to determine the scope, timing, and frequency of audit and assurance activities.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "AAC-03a", "title": "Audit scope is risk-based", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "BCR",
            "name": "Business Continuity and Operational Resilience",
            "description": "Controls for establishing business continuity, disaster recovery, and operational resilience capabilities to ensure critical cloud services can continue or be rapidly restored.",
            "sort_order": 3,
            "requirements": [
                {
                    "code": "BCR-01",
                    "title": "Business Continuity Management Policy",
                    "description": "Establish, document, approve, communicate, apply, evaluate, and maintain a business continuity management policy aligned with the organization's risk appetite.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "BCR-01a", "title": "Business continuity policy is established", "sort_order": 1},
                    ],
                },
                {
                    "code": "BCR-02",
                    "title": "Risk Assessment and Impact Analysis",
                    "description": "Determine the impact of business disruptions and risks to establish priorities and objectives for business continuity, including BIA and risk assessment.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "BCR-02a", "title": "Business impact analysis is performed", "sort_order": 1},
                    ],
                },
                {
                    "code": "BCR-03",
                    "title": "Business Continuity Strategy",
                    "description": "Establish a strategy for business continuity and disaster recovery that considers both prevention and recovery measures.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "BCR-03a", "title": "BC/DR strategy addresses prevention and recovery", "sort_order": 1},
                    ],
                },
                {
                    "code": "BCR-09",
                    "title": "Backup",
                    "description": "Establish, document, and implement backup and recovery procedures to ensure the protection of and continued access to critical data and systems.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "BCR-09a", "title": "Backup and recovery procedures are implemented", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CCC",
            "name": "Change Control and Configuration Management",
            "description": "Controls for managing changes to cloud infrastructure, applications, and configurations to ensure stability, security, and compliance.",
            "sort_order": 4,
            "requirements": [
                {
                    "code": "CCC-01",
                    "title": "Change Management Policy",
                    "description": "Establish, document, approve, communicate, apply, evaluate, and maintain policies and procedures for managing the risks associated with applying changes to cloud environments.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CCC-01a", "title": "Change management policy for cloud environments exists", "sort_order": 1},
                    ],
                },
                {
                    "code": "CCC-02",
                    "title": "Quality Testing",
                    "description": "Follow a defined quality change control, approval, and testing process before promoting changes to production.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CCC-02a", "title": "Changes undergo quality testing before production", "sort_order": 1},
                    ],
                },
                {
                    "code": "CCC-05",
                    "title": "Change Agreements",
                    "description": "Include provisions limiting changes to cloud environments in tenant-to-provider service agreements, ensuring customers are informed of impactful changes.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CCC-05a", "title": "Service agreements address change notification", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "DSP",
            "name": "Data Security and Privacy Lifecycle Management",
            "description": "Controls for classifying, protecting, and managing data through its lifecycle in cloud environments, including privacy, data integrity, and secure deletion.",
            "sort_order": 5,
            "requirements": [
                {
                    "code": "DSP-01",
                    "title": "Data Security and Privacy Policy",
                    "description": "Establish, document, approve, communicate, apply, evaluate, and maintain policies and procedures for data security and privacy throughout the data lifecycle.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "DSP-01a", "title": "Data security and privacy policy exists", "sort_order": 1},
                    ],
                },
                {
                    "code": "DSP-02",
                    "title": "Secure Disposal",
                    "description": "Define, implement, and evaluate processes, procedures, and technical measures to securely dispose of data stored in the cloud.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "DSP-02a", "title": "Secure data disposal procedures are implemented", "sort_order": 1},
                    ],
                },
                {
                    "code": "DSP-04",
                    "title": "Data Classification",
                    "description": "Classify data according to its type and sensitivity level to determine the appropriate protection controls.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "DSP-04a", "title": "Data classification scheme is applied", "sort_order": 1},
                    ],
                },
                {
                    "code": "DSP-07",
                    "title": "Data Protection by Design and Default",
                    "description": "Develop systems, products, and business practices based upon a principle of privacy by design and by default.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "DSP-07a", "title": "Privacy by design principles are applied", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "DCS",
            "name": "Datacenter Security",
            "description": "Controls for the physical security of datacenters housing cloud infrastructure, including environmental controls, physical access, and equipment protection.",
            "sort_order": 6,
            "requirements": [
                {
                    "code": "DCS-01",
                    "title": "Datacenter Security Policy",
                    "description": "Establish, document, approve, communicate, apply, evaluate, and maintain policies and procedures for the secure operation of datacenters.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "DCS-01a", "title": "Datacenter security policy is established", "sort_order": 1},
                    ],
                },
                {
                    "code": "DCS-03",
                    "title": "Controlled Access Points",
                    "description": "Implement physical security perimeters with controlled access points to restrict and monitor physical access to datacenter facilities.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "DCS-03a", "title": "Physical access to datacenters is controlled and monitored", "sort_order": 1},
                    ],
                },
                {
                    "code": "DCS-06",
                    "title": "Equipment Power and Environmental Controls",
                    "description": "Protect datacenter equipment from environmental hazards and maintain appropriate power and environmental conditions.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "DCS-06a", "title": "Environmental controls protect datacenter equipment", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "EKM",
            "name": "Encryption and Key Management",
            "description": "Controls for implementing encryption and managing cryptographic keys to protect data in cloud environments, including key generation, distribution, storage, and destruction.",
            "sort_order": 7,
            "requirements": [
                {
                    "code": "EKM-01",
                    "title": "Encryption and Key Management Policy",
                    "description": "Establish, document, approve, communicate, apply, evaluate, and maintain policies and procedures for encryption and key management.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "EKM-01a", "title": "Encryption and key management policy exists", "sort_order": 1},
                    ],
                },
                {
                    "code": "EKM-02",
                    "title": "Key Generation",
                    "description": "Generate cryptographic keys using industry-accepted algorithms, key sizes, and cryptographic random number generators.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "EKM-02a", "title": "Key generation follows industry standards", "sort_order": 1},
                    ],
                },
                {
                    "code": "EKM-03",
                    "title": "Sensitive Data Protection",
                    "description": "Define, implement, and evaluate processes to protect sensitive data at rest and in transit using encryption.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "EKM-03a", "title": "Encryption protects data at rest and in transit", "sort_order": 1},
                    ],
                },
                {
                    "code": "EKM-04",
                    "title": "Key Management Lifecycle",
                    "description": "Manage encryption keys throughout their lifecycle including generation, use, storage, archival, recovery, rotation, revocation, and destruction.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "EKM-04a", "title": "Key lifecycle management is implemented", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "GRM",
            "name": "Governance, Risk, and Compliance",
            "description": "Controls for establishing governance structures, risk management programs, and compliance frameworks to ensure cloud security objectives are met.",
            "sort_order": 8,
            "requirements": [
                {
                    "code": "GRM-01",
                    "title": "Governance Program",
                    "description": "Establish, document, approve, communicate, apply, evaluate, and maintain a governance program with defined leadership, organizational structures, and information security roles.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "GRM-01a", "title": "Governance program is established with defined roles", "sort_order": 1},
                    ],
                },
                {
                    "code": "GRM-02",
                    "title": "Risk Management Program",
                    "description": "Establish a formal risk management program that defines risk tolerance, risk assessment methodologies, and risk treatment options.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "GRM-02a", "title": "Formal risk management program exists", "sort_order": 1},
                    ],
                },
                {
                    "code": "GRM-06",
                    "title": "Policy Reviews",
                    "description": "Review all relevant organizational policies at planned intervals and adapt them to changes in applicable law, regulation, and contractual or business needs.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "GRM-06a", "title": "Policies are reviewed at planned intervals", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "HRS",
            "name": "Human Resources Security",
            "description": "Controls for ensuring personnel security throughout the employment lifecycle, including background checks, training, and termination procedures in cloud service provider organizations.",
            "sort_order": 9,
            "requirements": [
                {
                    "code": "HRS-01",
                    "title": "Background Screening Policy",
                    "description": "Establish, document, approve, communicate, apply, evaluate, and maintain policies and procedures for background screening of all personnel.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "HRS-01a", "title": "Background screening policy is established", "sort_order": 1},
                    ],
                },
                {
                    "code": "HRS-04",
                    "title": "Training and Awareness",
                    "description": "Establish, document, and maintain a security and privacy awareness training program for all relevant personnel.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "HRS-04a", "title": "Security and privacy awareness training is maintained", "sort_order": 1},
                    ],
                },
                {
                    "code": "HRS-07",
                    "title": "Workforce Termination",
                    "description": "Establish and maintain a process to revoke timely access to systems and data upon workforce departure or role change.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "HRS-07a", "title": "Access is revoked promptly upon termination", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "IAM",
            "name": "Identity and Access Management",
            "description": "Controls for managing identities and access in cloud environments, including authentication, authorization, privileged access, and multi-tenancy isolation.",
            "sort_order": 10,
            "requirements": [
                {
                    "code": "IAM-01",
                    "title": "Identity and Access Management Policy",
                    "description": "Establish, document, approve, communicate, apply, evaluate, and maintain policies and procedures for identity and access management.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "IAM-01a", "title": "IAM policy is established and maintained", "sort_order": 1},
                    ],
                },
                {
                    "code": "IAM-02",
                    "title": "Strong Password Policy",
                    "description": "Establish, document, and enforce a password policy meeting industry-accepted standards for complexity, expiration, and reuse prevention.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "IAM-02a", "title": "Password policy meets industry standards", "sort_order": 1},
                    ],
                },
                {
                    "code": "IAM-04",
                    "title": "Separation of Duties",
                    "description": "Restrict and manage privileged access rights, ensuring that functions requiring separation of duties are identified and enforced.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "IAM-04a", "title": "Separation of duties is enforced for privileged functions", "sort_order": 1},
                    ],
                },
                {
                    "code": "IAM-07",
                    "title": "User Access Review",
                    "description": "Review and revalidate user access at a defined frequency to ensure appropriateness and alignment with business needs.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "IAM-07a", "title": "User access reviews are conducted regularly", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "IVS",
            "name": "Infrastructure and Virtualization Security",
            "description": "Controls for securing cloud infrastructure and virtualization platforms, including network security, hardening, and segmentation between tenants.",
            "sort_order": 11,
            "requirements": [
                {
                    "code": "IVS-01",
                    "title": "Infrastructure and Virtualization Security Policy",
                    "description": "Establish, document, approve, communicate, apply, evaluate, and maintain policies and procedures for infrastructure and virtualization security.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "IVS-01a", "title": "Infrastructure security policy is established", "sort_order": 1},
                    ],
                },
                {
                    "code": "IVS-03",
                    "title": "Network Security",
                    "description": "Define, implement, and evaluate processes, procedures, and defense-in-depth techniques for network security and protection.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "IVS-03a", "title": "Defense-in-depth network security is implemented", "sort_order": 1},
                    ],
                },
                {
                    "code": "IVS-05",
                    "title": "Segmentation and Segregation",
                    "description": "Design and implement segmentation and segregation of networks to separate tenants and isolate sensitive environments.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "IVS-05a", "title": "Multi-tenant network segmentation is enforced", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "IPY",
            "name": "Interoperability and Portability",
            "description": "Controls for ensuring data portability and interoperability between cloud services, including the ability to migrate data and applications between providers.",
            "sort_order": 12,
            "requirements": [
                {
                    "code": "IPY-01",
                    "title": "Interoperability and Portability Policy",
                    "description": "Establish, document, approve, communicate, apply, evaluate, and maintain policies and procedures for interoperability and portability, including data portability and application migration.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "IPY-01a", "title": "Interoperability and portability policy exists", "sort_order": 1},
                    ],
                },
                {
                    "code": "IPY-02",
                    "title": "Data Portability",
                    "description": "Implement mechanisms that support the portability of data, using standards-based formats and documented methods for data export.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "IPY-02a", "title": "Data export in standard formats is supported", "sort_order": 1},
                    ],
                },
                {
                    "code": "IPY-04",
                    "title": "Data Portability Contractual Obligations",
                    "description": "Include provisions in service agreements that guarantee the ability to retrieve data in a standard format upon contract termination.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "IPY-04a", "title": "Service agreements guarantee data retrieval on termination", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "SEF",
            "name": "Security Incident Management, E-Discovery, and Cloud Forensics",
            "description": "Controls for managing security incidents, supporting e-discovery requests, and conducting forensic investigations in cloud environments.",
            "sort_order": 13,
            "requirements": [
                {
                    "code": "SEF-01",
                    "title": "Security Incident Management Policy",
                    "description": "Establish, document, approve, communicate, apply, evaluate, and maintain policies and procedures for security incident management, e-discovery, and cloud forensics.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "SEF-01a", "title": "Incident management policy is established", "sort_order": 1},
                    ],
                },
                {
                    "code": "SEF-02",
                    "title": "Service Management Policy",
                    "description": "Establish and maintain a clear incident management service management plan that defines roles, responsibilities, and communication procedures.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "SEF-02a", "title": "Incident management plan defines roles and procedures", "sort_order": 1},
                    ],
                },
                {
                    "code": "SEF-03",
                    "title": "Incident Response Plans",
                    "description": "Establish and maintain incident response plans that include detection, triage, containment, investigation, and remediation activities.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "SEF-03a", "title": "Incident response plans cover full lifecycle", "sort_order": 1},
                    ],
                },
                {
                    "code": "SEF-05",
                    "title": "Incident Response Testing",
                    "description": "Test incident response plans at planned intervals to determine effectiveness and update plans based on test findings.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "SEF-05a", "title": "Incident response plans are tested periodically", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "STA",
            "name": "Supply Chain Management, Transparency, and Accountability",
            "description": "Controls for managing supply chain risks, ensuring transparency in cloud operations, and maintaining accountability across the cloud service delivery chain.",
            "sort_order": 14,
            "requirements": [
                {
                    "code": "STA-01",
                    "title": "Supply Chain Management Policy",
                    "description": "Establish, document, approve, communicate, apply, evaluate, and maintain policies and procedures for supply chain management and transparency.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "STA-01a", "title": "Supply chain management policy is established", "sort_order": 1},
                    ],
                },
                {
                    "code": "STA-03",
                    "title": "Supply Chain Agreements",
                    "description": "Include security and privacy requirements, responsibilities, and assurance levels in supply chain agreements.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "STA-03a", "title": "Supply chain agreements include security requirements", "sort_order": 1},
                    ],
                },
                {
                    "code": "STA-05",
                    "title": "Supply Chain Risk Management",
                    "description": "Identify, assess, and manage risks associated with the supply chain for cloud services.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "STA-05a", "title": "Supply chain risks are assessed and managed", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "TVM",
            "name": "Threat and Vulnerability Management",
            "description": "Controls for identifying, evaluating, treating, and managing threats and vulnerabilities in cloud environments to reduce the risk of exploitation.",
            "sort_order": 15,
            "requirements": [
                {
                    "code": "TVM-01",
                    "title": "Threat and Vulnerability Management Policy",
                    "description": "Establish, document, approve, communicate, apply, evaluate, and maintain policies and procedures for threat and vulnerability management.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "TVM-01a", "title": "Threat and vulnerability management policy exists", "sort_order": 1},
                    ],
                },
                {
                    "code": "TVM-02",
                    "title": "Vulnerability Management",
                    "description": "Define, implement, and evaluate processes for vulnerability identification, classification, remediation, and mitigation in cloud environments.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "TVM-02a", "title": "Vulnerability management processes are operational", "sort_order": 1},
                    ],
                },
                {
                    "code": "TVM-04",
                    "title": "Vulnerability Remediation Schedule",
                    "description": "Establish, document, and maintain a vulnerability remediation schedule based on risk ratings and severity of identified vulnerabilities.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "TVM-04a", "title": "Vulnerability remediation follows risk-based schedule", "sort_order": 1},
                    ],
                },
                {
                    "code": "TVM-07",
                    "title": "Penetration Testing",
                    "description": "Perform penetration testing at planned intervals and after significant changes to evaluate cloud security controls effectiveness.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "TVM-07a", "title": "Penetration testing is conducted at planned intervals", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "UEM",
            "name": "Universal Endpoint Management",
            "description": "Controls for securing and managing all endpoint devices that connect to cloud services, including mobile devices, laptops, and IoT devices.",
            "sort_order": 16,
            "requirements": [
                {
                    "code": "UEM-01",
                    "title": "Endpoint Devices Policy",
                    "description": "Establish, document, approve, communicate, apply, evaluate, and maintain policies and procedures for managing and securing all endpoint devices that access cloud services.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "UEM-01a", "title": "Endpoint device management policy exists", "sort_order": 1},
                    ],
                },
                {
                    "code": "UEM-03",
                    "title": "Endpoint Security Configuration",
                    "description": "Define, implement, and evaluate secure configuration baselines for all endpoint devices accessing cloud resources.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "UEM-03a", "title": "Endpoint security baselines are configured and enforced", "sort_order": 1},
                    ],
                },
                {
                    "code": "UEM-06",
                    "title": "Anti-Malware Detection and Prevention",
                    "description": "Configure and enforce anti-malware detection and prevention on all endpoint devices to protect against malicious software.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "UEM-06a", "title": "Endpoint anti-malware is deployed and updated", "sort_order": 1},
                    ],
                },
            ],
        },
    ],
}


async def seed_csa_star_framework(db):
    """Seed the CSA STAR (CCM) framework."""
    from sqlalchemy import select
    from app.models.framework import Framework
    from app.models.framework_domain import FrameworkDomain
    from app.models.framework_requirement import FrameworkRequirement
    from app.models.control_objective import ControlObjective

    # Check if already seeded
    existing = await db.execute(
        select(Framework).where(Framework.name == CSA_STAR_FRAMEWORK["name"])
    )
    if existing.scalar_one_or_none():
        print("  -> CSA STAR (CCM) framework already seeded, skipping.")
        return

    fw_data = CSA_STAR_FRAMEWORK
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
    print(f"  Seeded CSA STAR (CCM): {req_count} requirements, {obj_count} objectives.")
    return framework
