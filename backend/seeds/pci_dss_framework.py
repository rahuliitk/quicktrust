"""PCI DSS v4.0 — framework seed data with 6 domains and 12 requirements."""

PCI_DSS_FRAMEWORK = {
    "name": "PCI DSS",
    "version": "4.0",
    "category": "Payment Card Security",
    "description": "Payment Card Industry Data Security Standard v4.0 — a set of security standards designed to ensure that all companies that accept, process, store, or transmit credit card information maintain a secure environment.",
    "domains": [
        {
            "code": "NET",
            "name": "Build and Maintain a Secure Network and Systems",
            "description": "Install and maintain network security controls and apply secure configurations to all system components to protect cardholder data environments.",
            "sort_order": 1,
            "requirements": [
                {
                    "code": "PCI-1",
                    "title": "Install and Maintain Network Security Controls",
                    "description": "Network security controls (NSCs) such as firewalls and other network security technologies are points of policy enforcement that control network traffic between two or more logical or physical network segments.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "PCI-1.2.1", "title": "Inbound and outbound traffic to the CDE is restricted to that which is necessary", "sort_order": 1},
                        {"code": "PCI-1.2.5", "title": "All services, protocols, and ports allowed are identified, approved, and have a defined business need", "sort_order": 2},
                        {"code": "PCI-1.3.1", "title": "Inbound traffic to the CDE is restricted", "sort_order": 3},
                    ],
                },
                {
                    "code": "PCI-2",
                    "title": "Apply Secure Configurations to All System Components",
                    "description": "Malicious individuals use default passwords and other vendor default settings to compromise systems. These defaults are well known and easily determined through public information.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "PCI-2.2.1", "title": "Vendor default accounts are managed and default passwords are changed", "sort_order": 1},
                        {"code": "PCI-2.2.2", "title": "System configuration standards are developed, implemented, and maintained", "sort_order": 2},
                        {"code": "PCI-2.2.7", "title": "All non-console administrative access is encrypted using strong cryptography", "sort_order": 3},
                    ],
                },
            ],
        },
        {
            "code": "CHD",
            "name": "Protect Cardholder Data",
            "description": "Protect stored account data and protect cardholder data with strong cryptography during transmission over open, public networks.",
            "sort_order": 2,
            "requirements": [
                {
                    "code": "PCI-3",
                    "title": "Protect Stored Account Data",
                    "description": "Protection methods such as encryption, truncation, masking, and hashing are critical components of cardholder data protection. Methods to minimize risk include not storing cardholder data unless absolutely necessary.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "PCI-3.1.1", "title": "Data retention and disposal policies and procedures are defined and implemented", "sort_order": 1},
                        {"code": "PCI-3.5.1", "title": "PAN is secured with strong cryptography wherever it is stored", "sort_order": 2},
                        {"code": "PCI-3.6.1", "title": "Cryptographic key management procedures are defined and implemented", "sort_order": 3},
                    ],
                },
                {
                    "code": "PCI-4",
                    "title": "Protect Cardholder Data with Strong Cryptography During Transmission",
                    "description": "Sensitive information must be encrypted during transmission over networks that are easily accessed by malicious individuals, including the internet, wireless technologies, cellular technologies, and satellite communications.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "PCI-4.2.1", "title": "Strong cryptography is used for PAN transmission over open, public networks", "sort_order": 1},
                        {"code": "PCI-4.2.2", "title": "PAN is secured with strong cryptography whenever sent via end-user messaging technologies", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "VUL",
            "name": "Maintain a Vulnerability Management Program",
            "description": "Protect all systems and networks from malicious software and maintain secure systems and software by regularly updating and patching.",
            "sort_order": 3,
            "requirements": [
                {
                    "code": "PCI-5",
                    "title": "Protect All Systems and Networks from Malicious Software",
                    "description": "Malicious software (malware) enters the network through numerous business-approved activities, including employee email, use of the internet, mobile computers, and storage devices, resulting in exploitation of system vulnerabilities.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "PCI-5.2.1", "title": "Anti-malware solution is deployed on all systems commonly affected by malware", "sort_order": 1},
                        {"code": "PCI-5.2.2", "title": "Anti-malware solution performs periodic scans and active monitoring", "sort_order": 2},
                        {"code": "PCI-5.3.1", "title": "Anti-malware mechanisms and definitions are kept current", "sort_order": 3},
                    ],
                },
                {
                    "code": "PCI-6",
                    "title": "Develop and Maintain Secure Systems and Software",
                    "description": "Security vulnerabilities in systems and software may allow criminals to access PAN and other cardholder data. Many vulnerabilities are eliminated by installing vendor-provided security patches and maintaining a secure development lifecycle.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "PCI-6.2.1", "title": "Bespoke and custom software are developed securely", "sort_order": 1},
                        {"code": "PCI-6.3.1", "title": "Security vulnerabilities are identified and managed through a defined process", "sort_order": 2},
                        {"code": "PCI-6.3.3", "title": "All applicable security patches and updates are installed within the defined timeframe", "sort_order": 3},
                    ],
                },
            ],
        },
        {
            "code": "IAC",
            "name": "Implement Strong Access Control Measures",
            "description": "Restrict and manage access to cardholder data and system components through business need-to-know, user identification, authentication, and physical access controls.",
            "sort_order": 4,
            "requirements": [
                {
                    "code": "PCI-7",
                    "title": "Restrict Access to System Components and Cardholder Data by Business Need to Know",
                    "description": "Unauthorized individuals may gain access to critical data or systems due to ineffective access control rules and definitions. Access to system components and cardholder data must be limited to only those individuals whose job requires such access.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "PCI-7.2.1", "title": "Access control model is defined and includes granting access based on job function and need-to-know", "sort_order": 1},
                        {"code": "PCI-7.2.2", "title": "Access is assigned to users based on job classification and function", "sort_order": 2},
                    ],
                },
                {
                    "code": "PCI-8",
                    "title": "Identify Users and Authenticate Access to System Components",
                    "description": "Two fundamental principles of identifying and authenticating users are: establishing identity of an individual or process on a computer system, and proving or verifying the user is who they claim to be.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "PCI-8.2.1", "title": "All users are assigned a unique ID before access to system components", "sort_order": 1},
                        {"code": "PCI-8.3.1", "title": "All user access to system components is authenticated via at least one factor", "sort_order": 2},
                        {"code": "PCI-8.3.6", "title": "Passwords or passphrases meet minimum complexity requirements", "sort_order": 3},
                    ],
                },
                {
                    "code": "PCI-9",
                    "title": "Restrict Physical Access to Cardholder Data",
                    "description": "Any physical access to cardholder data or systems that store, process, or transmit cardholder data provides the opportunity for individuals to access and remove devices, data, systems, or hardcopies, and should be appropriately restricted.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "PCI-9.2.1", "title": "Appropriate facility entry controls are in place to limit physical access to CDE systems", "sort_order": 1},
                        {"code": "PCI-9.4.1", "title": "All media with cardholder data is physically secured", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "MON",
            "name": "Regularly Monitor and Test Networks",
            "description": "Log and monitor all access to system components and cardholder data, and regularly test security systems and processes.",
            "sort_order": 5,
            "requirements": [
                {
                    "code": "PCI-10",
                    "title": "Log and Monitor All Access to System Components and Cardholder Data",
                    "description": "Logging mechanisms and the ability to track user activities are critical in preventing, detecting, and minimizing the impact of a data compromise. The presence of logs allows thorough tracking, alerting, and analysis when incidents occur.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "PCI-10.2.1", "title": "Audit logs capture all individual user access to cardholder data", "sort_order": 1},
                        {"code": "PCI-10.2.2", "title": "Audit logs capture all actions taken by any individual with administrative access", "sort_order": 2},
                        {"code": "PCI-10.4.1", "title": "Audit logs are reviewed at least once daily to identify anomalies or suspicious activity", "sort_order": 3},
                    ],
                },
                {
                    "code": "PCI-11",
                    "title": "Test Security of Systems and Networks Regularly",
                    "description": "Vulnerabilities are being discovered continually by malicious individuals and researchers, and being introduced by new software. System components, processes, and bespoke and custom software should be tested frequently.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "PCI-11.3.1", "title": "Internal vulnerability scans are performed at least once every three months", "sort_order": 1},
                        {"code": "PCI-11.3.2", "title": "External vulnerability scans are performed at least once every three months by an ASV", "sort_order": 2},
                        {"code": "PCI-11.4.1", "title": "Internal penetration testing is performed at least once every 12 months", "sort_order": 3},
                    ],
                },
            ],
        },
        {
            "code": "POL",
            "name": "Maintain an Information Security Policy",
            "description": "Support information security with organizational policies and programs that ensure all personnel are aware of and follow the sensitivity of cardholder data and their responsibilities for protecting it.",
            "sort_order": 6,
            "requirements": [
                {
                    "code": "PCI-12",
                    "title": "Support Information Security with Organizational Policies and Programs",
                    "description": "A strong security policy sets the tone for the whole entity and informs personnel what is expected of them. All personnel should be aware of the sensitivity of cardholder data and their responsibilities for protecting it.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "PCI-12.1.1", "title": "Information security policy is established, published, maintained, and disseminated", "sort_order": 1},
                        {"code": "PCI-12.3.1", "title": "Roles and responsibilities for performing activities in each requirement are documented and understood", "sort_order": 2},
                        {"code": "PCI-12.6.1", "title": "Security awareness program provides awareness to all personnel upon hire and at least once every 12 months", "sort_order": 3},
                    ],
                },
            ],
        },
    ],
}


async def seed_pci_dss_framework(db):
    """Seed the PCI DSS v4.0 framework."""
    from sqlalchemy import select
    from app.models.framework import Framework
    from app.models.framework_domain import FrameworkDomain
    from app.models.framework_requirement import FrameworkRequirement
    from app.models.control_objective import ControlObjective

    # Check if already seeded
    existing = await db.execute(
        select(Framework).where(Framework.name == "PCI DSS")
    )
    if existing.scalar_one_or_none():
        print("  -> PCI DSS framework already seeded, skipping.")
        return

    fw_data = PCI_DSS_FRAMEWORK
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
                    description=obj_data.get("description"),
                    sort_order=obj_data["sort_order"],
                )
                db.add(obj)
                obj_count += 1

    await db.commit()
    print(f"  Seeded PCI DSS v4.0: {req_count} requirements, {obj_count} objectives.")
    return framework
