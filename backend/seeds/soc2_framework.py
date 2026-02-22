"""SOC 2 Type II Trust Services Criteria (2017) — full framework seed data."""

SOC2_FRAMEWORK = {
    "name": "SOC 2 Type II",
    "version": "2017",
    "category": "Security & Compliance",
    "description": "SOC 2 Trust Services Criteria — evaluates controls relevant to security, availability, processing integrity, confidentiality, and privacy.",
    "domains": [
        {
            "code": "CC1",
            "name": "Control Environment",
            "description": "The set of standards, processes, and structures that provide the basis for carrying out internal control across the organization.",
            "sort_order": 1,
            "requirements": [
                {
                    "code": "CC1.1",
                    "title": "COSO Principle 1: Demonstrates Commitment to Integrity and Ethical Values",
                    "description": "The entity demonstrates a commitment to integrity and ethical values.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CC1.1.1", "title": "Code of conduct is established and communicated", "sort_order": 1},
                        {"code": "CC1.1.2", "title": "Deviations from expected behavior are addressed", "sort_order": 2},
                    ],
                },
                {
                    "code": "CC1.2",
                    "title": "COSO Principle 2: Board Exercises Oversight Responsibility",
                    "description": "The board of directors demonstrates independence from management and exercises oversight.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CC1.2.1", "title": "Board oversight of internal controls is established", "sort_order": 1},
                    ],
                },
                {
                    "code": "CC1.3",
                    "title": "COSO Principle 3: Establishes Structure, Authority, and Responsibility",
                    "description": "Management establishes structures, reporting lines, and appropriate authorities and responsibilities.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CC1.3.1", "title": "Organizational structure supports internal control", "sort_order": 1},
                    ],
                },
                {
                    "code": "CC1.4",
                    "title": "COSO Principle 4: Demonstrates Commitment to Competence",
                    "description": "The entity demonstrates a commitment to attract, develop, and retain competent individuals.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CC1.4.1", "title": "Competency requirements are defined and evaluated", "sort_order": 1},
                    ],
                },
                {
                    "code": "CC1.5",
                    "title": "COSO Principle 5: Enforces Accountability",
                    "description": "The entity holds individuals accountable for their internal control responsibilities.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "CC1.5.1", "title": "Accountability for control responsibilities is enforced", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CC2",
            "name": "Communication and Information",
            "description": "Information necessary for the entity to carry out internal control responsibilities.",
            "sort_order": 2,
            "requirements": [
                {
                    "code": "CC2.1",
                    "title": "COSO Principle 13: Uses Relevant Information",
                    "description": "The entity obtains or generates and uses relevant, quality information to support the functioning of internal control.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CC2.1.1", "title": "Information systems produce quality data for controls", "sort_order": 1},
                    ],
                },
                {
                    "code": "CC2.2",
                    "title": "COSO Principle 14: Communicates Internally",
                    "description": "The entity internally communicates information necessary to support the functioning of internal control.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CC2.2.1", "title": "Internal communications support control objectives", "sort_order": 1},
                    ],
                },
                {
                    "code": "CC2.3",
                    "title": "COSO Principle 15: Communicates Externally",
                    "description": "The entity communicates with external parties regarding matters affecting internal control.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CC2.3.1", "title": "External communication processes are established", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CC3",
            "name": "Risk Assessment",
            "description": "The process for identifying and assessing risks to the achievement of objectives.",
            "sort_order": 3,
            "requirements": [
                {
                    "code": "CC3.1",
                    "title": "COSO Principle 6: Specifies Suitable Objectives",
                    "description": "The entity specifies objectives with sufficient clarity to enable the identification and assessment of risks.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CC3.1.1", "title": "Security objectives are defined and documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "CC3.2",
                    "title": "COSO Principle 7: Identifies and Analyzes Risk",
                    "description": "The entity identifies risks and analyzes risks as a basis for determining how risks should be managed.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CC3.2.1", "title": "Risk identification and analysis process is documented", "sort_order": 1},
                        {"code": "CC3.2.2", "title": "Risk register is maintained and reviewed", "sort_order": 2},
                    ],
                },
                {
                    "code": "CC3.3",
                    "title": "COSO Principle 8: Assesses Fraud Risk",
                    "description": "The entity considers the potential for fraud in assessing risks.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CC3.3.1", "title": "Fraud risk assessment is performed periodically", "sort_order": 1},
                    ],
                },
                {
                    "code": "CC3.4",
                    "title": "COSO Principle 9: Identifies and Analyzes Significant Change",
                    "description": "The entity identifies and assesses changes that could significantly impact the system of internal control.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CC3.4.1", "title": "Change impact on controls is assessed", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CC4",
            "name": "Monitoring Activities",
            "description": "Activities to ascertain whether the components of internal control are present and functioning.",
            "sort_order": 4,
            "requirements": [
                {
                    "code": "CC4.1",
                    "title": "COSO Principle 16: Selects, Develops, and Performs Ongoing Evaluations",
                    "description": "The entity selects, develops, and performs ongoing evaluations to ascertain whether controls are present and functioning.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CC4.1.1", "title": "Ongoing monitoring of controls is performed", "sort_order": 1},
                    ],
                },
                {
                    "code": "CC4.2",
                    "title": "COSO Principle 17: Evaluates and Communicates Deficiencies",
                    "description": "The entity evaluates and communicates internal control deficiencies in a timely manner.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CC4.2.1", "title": "Control deficiencies are reported and remediated", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CC5",
            "name": "Control Activities",
            "description": "Actions established through policies and procedures that help ensure management directives are carried out.",
            "sort_order": 5,
            "requirements": [
                {
                    "code": "CC5.1",
                    "title": "COSO Principle 10: Selects and Develops Control Activities",
                    "description": "The entity selects and develops control activities that mitigate risks to acceptable levels.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CC5.1.1", "title": "Control activities are mapped to identified risks", "sort_order": 1},
                    ],
                },
                {
                    "code": "CC5.2",
                    "title": "COSO Principle 11: Selects and Develops General Controls over Technology",
                    "description": "The entity selects and develops general control activities over technology.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CC5.2.1", "title": "IT general controls are implemented", "sort_order": 1},
                        {"code": "CC5.2.2", "title": "Technology infrastructure is secured", "sort_order": 2},
                    ],
                },
                {
                    "code": "CC5.3",
                    "title": "COSO Principle 12: Deploys Through Policies and Procedures",
                    "description": "The entity deploys control activities through policies and procedures.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CC5.3.1", "title": "Security policies are documented and distributed", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CC6",
            "name": "Logical and Physical Access Controls",
            "description": "Controls to restrict logical and physical access to protect assets.",
            "sort_order": 6,
            "requirements": [
                {
                    "code": "CC6.1",
                    "title": "Logical Access Security Software, Infrastructure, and Architectures",
                    "description": "The entity implements logical access security over protected information assets.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CC6.1.1", "title": "Access control mechanisms are implemented", "sort_order": 1},
                        {"code": "CC6.1.2", "title": "Authentication mechanisms are enforced", "sort_order": 2},
                    ],
                },
                {
                    "code": "CC6.2",
                    "title": "User Registration and Authorization",
                    "description": "Prior to granting access, registered and authorized users are identified.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CC6.2.1", "title": "User provisioning process is documented", "sort_order": 1},
                        {"code": "CC6.2.2", "title": "Access authorization is role-based", "sort_order": 2},
                    ],
                },
                {
                    "code": "CC6.3",
                    "title": "Access Removal and Modification",
                    "description": "The entity removes access to protected information assets when appropriate.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CC6.3.1", "title": "Deprovisioning procedures are implemented", "sort_order": 1},
                        {"code": "CC6.3.2", "title": "Periodic access reviews are conducted", "sort_order": 2},
                    ],
                },
                {
                    "code": "CC6.4",
                    "title": "Restriction of Physical Access",
                    "description": "The entity restricts physical access to facilities and protected information assets.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CC6.4.1", "title": "Physical access controls are implemented", "sort_order": 1},
                    ],
                },
                {
                    "code": "CC6.5",
                    "title": "Disposal of Assets",
                    "description": "The entity disposes of protected information assets in a secure manner.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "CC6.5.1", "title": "Secure disposal procedures are implemented", "sort_order": 1},
                    ],
                },
                {
                    "code": "CC6.6",
                    "title": "Logical Access Controls Against External Threats",
                    "description": "The entity implements controls to prevent or detect unauthorized access from outside the system boundaries.",
                    "sort_order": 6,
                    "objectives": [
                        {"code": "CC6.6.1", "title": "Network perimeter defenses are deployed", "sort_order": 1},
                        {"code": "CC6.6.2", "title": "Intrusion detection is operational", "sort_order": 2},
                    ],
                },
                {
                    "code": "CC6.7",
                    "title": "Data Transmission Controls",
                    "description": "The entity restricts the transmission of data to authorized parties.",
                    "sort_order": 7,
                    "objectives": [
                        {"code": "CC6.7.1", "title": "Encryption in transit is enforced", "sort_order": 1},
                    ],
                },
                {
                    "code": "CC6.8",
                    "title": "Controls Against Malicious Software",
                    "description": "The entity implements controls to prevent introduction of unauthorized or malicious software.",
                    "sort_order": 8,
                    "objectives": [
                        {"code": "CC6.8.1", "title": "Endpoint protection is deployed and monitored", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CC7",
            "name": "System Operations",
            "description": "Controls over system operations to detect and mitigate processing deviations.",
            "sort_order": 7,
            "requirements": [
                {
                    "code": "CC7.1",
                    "title": "Detection of Changes to Infrastructure and Software",
                    "description": "The entity detects unauthorized changes to infrastructure and software.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CC7.1.1", "title": "Change detection mechanisms are operational", "sort_order": 1},
                    ],
                },
                {
                    "code": "CC7.2",
                    "title": "Monitoring System Components for Anomalies",
                    "description": "The entity monitors system components for anomalies indicative of malicious acts or system failures.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CC7.2.1", "title": "System monitoring and alerting is configured", "sort_order": 1},
                        {"code": "CC7.2.2", "title": "Log analysis is performed regularly", "sort_order": 2},
                    ],
                },
                {
                    "code": "CC7.3",
                    "title": "Evaluation of Security Events",
                    "description": "The entity evaluates identified events to determine whether they represent security incidents.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CC7.3.1", "title": "Security event triage process is defined", "sort_order": 1},
                    ],
                },
                {
                    "code": "CC7.4",
                    "title": "Incident Response",
                    "description": "The entity responds to identified security incidents.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CC7.4.1", "title": "Incident response plan is documented and tested", "sort_order": 1},
                        {"code": "CC7.4.2", "title": "Incident communication procedures are established", "sort_order": 2},
                    ],
                },
                {
                    "code": "CC7.5",
                    "title": "Recovery from Incidents",
                    "description": "The entity identifies, develops, and implements activities to recover from identified security incidents.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "CC7.5.1", "title": "Recovery procedures are documented and tested", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CC8",
            "name": "Change Management",
            "description": "Controls over changes to infrastructure, data, software, and procedures.",
            "sort_order": 8,
            "requirements": [
                {
                    "code": "CC8.1",
                    "title": "Changes to Infrastructure, Data, Software, and Procedures",
                    "description": "The entity authorizes, designs, develops, configures, documents, tests, approves, and implements changes.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CC8.1.1", "title": "Change management process is documented and followed", "sort_order": 1},
                        {"code": "CC8.1.2", "title": "Changes are tested before deployment", "sort_order": 2},
                        {"code": "CC8.1.3", "title": "Emergency change procedures are defined", "sort_order": 3},
                    ],
                },
            ],
        },
        {
            "code": "CC9",
            "name": "Risk Mitigation",
            "description": "Controls for risk mitigation through business processes and activities.",
            "sort_order": 9,
            "requirements": [
                {
                    "code": "CC9.1",
                    "title": "Risk Mitigation Activities",
                    "description": "The entity identifies, selects, and develops risk mitigation activities.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CC9.1.1", "title": "Risk treatment plans are documented and tracked", "sort_order": 1},
                    ],
                },
                {
                    "code": "CC9.2",
                    "title": "Vendor and Business Partner Risk Management",
                    "description": "The entity assesses and manages risks associated with vendors and business partners.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CC9.2.1", "title": "Vendor risk assessment process is established", "sort_order": 1},
                        {"code": "CC9.2.2", "title": "Vendor agreements include security requirements", "sort_order": 2},
                    ],
                },
            ],
        },
    ],
}


async def seed_soc2_framework(db):
    from app.models.framework import Framework
    from app.models.framework_domain import FrameworkDomain
    from app.models.framework_requirement import FrameworkRequirement
    from app.models.control_objective import ControlObjective
    from sqlalchemy import select

    # Check if already seeded
    existing = await db.execute(
        select(Framework).where(Framework.name == SOC2_FRAMEWORK["name"])
    )
    if existing.scalar_one_or_none():
        print("SOC 2 framework already seeded, skipping.")
        return None

    framework = Framework(
        name=SOC2_FRAMEWORK["name"],
        version=SOC2_FRAMEWORK["version"],
        category=SOC2_FRAMEWORK["category"],
        description=SOC2_FRAMEWORK["description"],
    )
    db.add(framework)
    await db.flush()

    for domain_data in SOC2_FRAMEWORK["domains"]:
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

            for obj_data in req_data.get("objectives", []):
                obj = ControlObjective(
                    requirement_id=req.id,
                    code=obj_data["code"],
                    title=obj_data["title"],
                    sort_order=obj_data["sort_order"],
                )
                db.add(obj)

    await db.commit()
    print(f"Seeded SOC 2 framework with {len(SOC2_FRAMEWORK['domains'])} domains.")
    return framework
