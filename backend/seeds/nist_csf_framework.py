"""NIST Cybersecurity Framework (CSF) 2.0 — framework seed data with 6 functions."""

NIST_CSF_FRAMEWORK = {
    "name": "NIST CSF",
    "version": "2.0",
    "category": "Cybersecurity",
    "description": "NIST Cybersecurity Framework 2.0 — provides a taxonomy of high-level cybersecurity outcomes that can be used by any organization to better understand, assess, prioritize, and communicate its cybersecurity efforts. The framework comprises six core functions: Govern, Identify, Protect, Detect, Respond, and Recover.",
    "domains": [
        {
            "code": "GV",
            "name": "Govern",
            "description": "The organization's cybersecurity risk management strategy, expectations, and policy are established, communicated, and monitored. The GOVERN function provides outcomes to inform what an organization may do to achieve and prioritize the outcomes of the other five functions.",
            "sort_order": 1,
            "requirements": [
                {
                    "code": "GV.OC",
                    "title": "Organizational Context",
                    "description": "The circumstances — mission, stakeholder expectations, dependencies, and legal, regulatory, and contractual requirements — surrounding the organization's cybersecurity risk management decisions are understood.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "GV.OC-01", "title": "The organizational mission is understood and informs cybersecurity risk management", "sort_order": 1},
                        {"code": "GV.OC-02", "title": "Internal and external stakeholders are understood and their requirements and expectations are communicated", "sort_order": 2},
                        {"code": "GV.OC-03", "title": "Legal, regulatory, and contractual requirements regarding cybersecurity are understood and managed", "sort_order": 3},
                        {"code": "GV.OC-04", "title": "Critical objectives, capabilities, and services are understood and communicated", "sort_order": 4},
                        {"code": "GV.OC-05", "title": "Outcomes, capabilities, and services that depend on external parties are understood and managed", "sort_order": 5},
                    ],
                },
                {
                    "code": "GV.RM",
                    "title": "Risk Management Strategy",
                    "description": "The organization's priorities, constraints, risk tolerance, and appetite statements are established, communicated, and used to support operational risk decisions.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "GV.RM-01", "title": "Risk management objectives are established and agreed upon by organizational stakeholders", "sort_order": 1},
                        {"code": "GV.RM-02", "title": "Risk appetite and risk tolerance statements are established, communicated, and maintained", "sort_order": 2},
                        {"code": "GV.RM-03", "title": "Cybersecurity risk management activities and outcomes are included in enterprise risk management processes", "sort_order": 3},
                        {"code": "GV.RM-04", "title": "Strategic direction for how the organization will respond to risk is established and communicated", "sort_order": 4},
                    ],
                },
                {
                    "code": "GV.RR",
                    "title": "Roles, Responsibilities, and Authorities",
                    "description": "Cybersecurity roles, responsibilities, and authorities to foster accountability, performance assessment, and continuous improvement are established and communicated.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "GV.RR-01", "title": "Organizational leadership is responsible and accountable for cybersecurity risk", "sort_order": 1},
                        {"code": "GV.RR-02", "title": "Roles, responsibilities, and authorities related to cybersecurity are established, communicated, and enforced", "sort_order": 2},
                        {"code": "GV.RR-03", "title": "Adequate resources are allocated commensurate with cybersecurity risk strategy and priorities", "sort_order": 3},
                        {"code": "GV.RR-04", "title": "Cybersecurity is included in human resources practices", "sort_order": 4},
                    ],
                },
                {
                    "code": "GV.PO",
                    "title": "Policy",
                    "description": "Organizational cybersecurity policy is established, communicated, and enforced.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "GV.PO-01", "title": "A policy for managing cybersecurity risks is established based on organizational context and strategy", "sort_order": 1},
                        {"code": "GV.PO-02", "title": "Policy is reviewed, updated, and communicated to reflect changes in requirements and environment", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "ID",
            "name": "Identify",
            "description": "The organization's current cybersecurity risks are understood. Understanding assets, suppliers, vulnerabilities, threats, and their associated risks allows an organization to prioritize its efforts consistent with its risk management strategy.",
            "sort_order": 2,
            "requirements": [
                {
                    "code": "ID.AM",
                    "title": "Asset Management",
                    "description": "Assets (e.g., data, hardware, software, systems, facilities, services, people) that enable the organization to achieve business purposes are identified and managed consistent with their relative importance.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "ID.AM-01", "title": "Inventories of hardware managed by the organization are maintained", "sort_order": 1},
                        {"code": "ID.AM-02", "title": "Inventories of software, services, and systems managed by the organization are maintained", "sort_order": 2},
                        {"code": "ID.AM-03", "title": "Representations of authorized network communication and internal and external network data flows are maintained", "sort_order": 3},
                        {"code": "ID.AM-04", "title": "Inventories of services provided by suppliers are maintained", "sort_order": 4},
                        {"code": "ID.AM-05", "title": "Assets are prioritized based on classification, criticality, resources, and impact on the mission", "sort_order": 5},
                    ],
                },
                {
                    "code": "ID.RA",
                    "title": "Risk Assessment",
                    "description": "The cybersecurity risk to the organization, assets, and individuals is understood by the organization.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "ID.RA-01", "title": "Vulnerabilities in assets are identified, validated, and recorded", "sort_order": 1},
                        {"code": "ID.RA-02", "title": "Cyber threat intelligence is received from information sharing forums and sources", "sort_order": 2},
                        {"code": "ID.RA-03", "title": "Internal and external threats to the organization are identified and recorded", "sort_order": 3},
                        {"code": "ID.RA-04", "title": "Potential impacts and likelihoods of threats exploiting vulnerabilities are identified and recorded", "sort_order": 4},
                        {"code": "ID.RA-05", "title": "Threats, vulnerabilities, likelihoods, and impacts are used to understand inherent risk", "sort_order": 5},
                    ],
                },
                {
                    "code": "ID.IM",
                    "title": "Improvement",
                    "description": "Improvements to organizational cybersecurity risk management processes, procedures, and activities are identified across all CSF functions.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "ID.IM-01", "title": "Improvements are identified from evaluations", "sort_order": 1},
                        {"code": "ID.IM-02", "title": "Improvements are identified from security tests and exercises including those done in coordination with suppliers", "sort_order": 2},
                        {"code": "ID.IM-03", "title": "Improvements are identified from execution of operational processes, procedures, and activities", "sort_order": 3},
                    ],
                },
                {
                    "code": "ID.SC",
                    "title": "Supply Chain Risk Management",
                    "description": "Supply chain risks are identified, assessed, and managed.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "ID.SC-01", "title": "A cyber supply chain risk management program and strategy are established and agreed upon by stakeholders", "sort_order": 1},
                        {"code": "ID.SC-02", "title": "Suppliers and third-party partners of information systems are identified, prioritized, and assessed", "sort_order": 2},
                        {"code": "ID.SC-03", "title": "Supply chain risk management is integrated into cybersecurity and enterprise risk management", "sort_order": 3},
                    ],
                },
            ],
        },
        {
            "code": "PR",
            "name": "Protect",
            "description": "Safeguards to manage the organization's cybersecurity risks are used. The outcomes in this function support the ability to secure assets to prevent or lower the likelihood and impact of adverse cybersecurity events.",
            "sort_order": 3,
            "requirements": [
                {
                    "code": "PR.AA",
                    "title": "Identity Management, Authentication, and Access Control",
                    "description": "Access to physical and logical assets is limited to authorized users, services, and hardware and managed commensurate with the assessed risk of unauthorized access.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "PR.AA-01", "title": "Identities and credentials for authorized users, services, and hardware are managed", "sort_order": 1},
                        {"code": "PR.AA-02", "title": "Identities are proofed and bound to credentials based on the context of interactions", "sort_order": 2},
                        {"code": "PR.AA-03", "title": "Users, services, and hardware are authenticated", "sort_order": 3},
                        {"code": "PR.AA-04", "title": "Identity assertions are protected, conveyed, and verified", "sort_order": 4},
                        {"code": "PR.AA-05", "title": "Access permissions, entitlements, and authorizations are defined and managed", "sort_order": 5},
                    ],
                },
                {
                    "code": "PR.AT",
                    "title": "Awareness and Training",
                    "description": "The organization's personnel are provided cybersecurity awareness and training so that they can perform their cybersecurity-related tasks.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "PR.AT-01", "title": "Personnel are provided with awareness and training so that they possess the knowledge and skills to perform general tasks with cybersecurity risks in mind", "sort_order": 1},
                        {"code": "PR.AT-02", "title": "Individuals in specialized roles are provided with awareness and training so that they possess the knowledge and skills to perform relevant tasks", "sort_order": 2},
                    ],
                },
                {
                    "code": "PR.DS",
                    "title": "Data Security",
                    "description": "Data are managed consistent with the organization's risk strategy to protect the confidentiality, integrity, and availability of information.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "PR.DS-01", "title": "The confidentiality, integrity, and availability of data-at-rest are protected", "sort_order": 1},
                        {"code": "PR.DS-02", "title": "The confidentiality, integrity, and availability of data-in-transit are protected", "sort_order": 2},
                        {"code": "PR.DS-10", "title": "The confidentiality, integrity, and availability of data-in-use are protected", "sort_order": 3},
                        {"code": "PR.DS-11", "title": "Backups of data are created, protected, maintained, and tested", "sort_order": 4},
                    ],
                },
                {
                    "code": "PR.PS",
                    "title": "Platform Security",
                    "description": "The hardware, software, and services of physical and virtual platforms are managed consistent with the organization's risk strategy.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "PR.PS-01", "title": "Configuration management practices are established and applied", "sort_order": 1},
                        {"code": "PR.PS-02", "title": "Software is maintained, replaced, and removed commensurate with risk", "sort_order": 2},
                        {"code": "PR.PS-03", "title": "Hardware is maintained, replaced, and removed commensurate with risk", "sort_order": 3},
                        {"code": "PR.PS-04", "title": "Log records are generated and made available for continuous monitoring", "sort_order": 4},
                    ],
                },
                {
                    "code": "PR.IR",
                    "title": "Technology Infrastructure Resilience",
                    "description": "Security architectures are managed with the organization's risk strategy to protect asset confidentiality, integrity, and availability and organizational resilience.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "PR.IR-01", "title": "Networks and environments are protected from unauthorized logical access and usage", "sort_order": 1},
                        {"code": "PR.IR-02", "title": "The organization's technology assets are protected from environmental threats", "sort_order": 2},
                        {"code": "PR.IR-03", "title": "Mechanisms are implemented to achieve resilience requirements in normal and adverse situations", "sort_order": 3},
                        {"code": "PR.IR-04", "title": "Adequate resource capacity to ensure availability is maintained", "sort_order": 4},
                    ],
                },
            ],
        },
        {
            "code": "DE",
            "name": "Detect",
            "description": "Possible cybersecurity attacks and compromises are found and analyzed. The outcomes in this function enable timely discovery and analysis of anomalies, indicators of compromise, and other potentially adverse events.",
            "sort_order": 4,
            "requirements": [
                {
                    "code": "DE.CM",
                    "title": "Continuous Monitoring",
                    "description": "Assets are monitored to find anomalies, indicators of compromise, and other potentially adverse events.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "DE.CM-01", "title": "Networks and network services are monitored to find potentially adverse events", "sort_order": 1},
                        {"code": "DE.CM-02", "title": "The physical environment is monitored to find potentially adverse events", "sort_order": 2},
                        {"code": "DE.CM-03", "title": "Personnel activity and technology usage are monitored to find potentially adverse events", "sort_order": 3},
                        {"code": "DE.CM-06", "title": "External service provider activities and services are monitored to find potentially adverse events", "sort_order": 4},
                        {"code": "DE.CM-09", "title": "Computing hardware and software, runtime environments, and their data are monitored to find potentially adverse events", "sort_order": 5},
                    ],
                },
                {
                    "code": "DE.AE",
                    "title": "Adverse Event Analysis",
                    "description": "Anomalies, indicators of compromise, and other potentially adverse events are analyzed to characterize the events and detect cybersecurity incidents.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "DE.AE-02", "title": "Potentially adverse events are analyzed to better understand associated activities", "sort_order": 1},
                        {"code": "DE.AE-03", "title": "Information is correlated from multiple sources", "sort_order": 2},
                        {"code": "DE.AE-04", "title": "The estimated impact and scope of adverse events are understood", "sort_order": 3},
                        {"code": "DE.AE-06", "title": "Information on adverse events is provided to authorized staff and tools", "sort_order": 4},
                    ],
                },
                {
                    "code": "DE.DP",
                    "title": "Detection Processes",
                    "description": "Detection processes and procedures are maintained and tested to ensure awareness of anomalous events.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "DE.DP-01", "title": "Roles and responsibilities for detection are well defined to ensure accountability", "sort_order": 1},
                        {"code": "DE.DP-02", "title": "Detection activities comply with all applicable requirements", "sort_order": 2},
                        {"code": "DE.DP-04", "title": "Event detection information is communicated", "sort_order": 3},
                        {"code": "DE.DP-05", "title": "Detection processes are continuously improved", "sort_order": 4},
                    ],
                },
            ],
        },
        {
            "code": "RS",
            "name": "Respond",
            "description": "Actions regarding a detected cybersecurity incident are taken. The outcomes in this function support the ability to contain the impact of cybersecurity incidents.",
            "sort_order": 5,
            "requirements": [
                {
                    "code": "RS.MA",
                    "title": "Incident Management",
                    "description": "Responses to detected cybersecurity incidents are managed.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "RS.MA-01", "title": "The incident response plan is executed in coordination with relevant third parties once an incident is declared", "sort_order": 1},
                        {"code": "RS.MA-02", "title": "Incident reports are triaged and validated", "sort_order": 2},
                        {"code": "RS.MA-03", "title": "Incidents are categorized and prioritized", "sort_order": 3},
                        {"code": "RS.MA-04", "title": "Incidents are escalated or elevated as needed", "sort_order": 4},
                    ],
                },
                {
                    "code": "RS.AN",
                    "title": "Incident Analysis",
                    "description": "Investigations are conducted to ensure effective response and support forensics and recovery activities.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "RS.AN-03", "title": "Analysis is performed to establish what has taken place during an incident and root cause", "sort_order": 1},
                        {"code": "RS.AN-06", "title": "Actions performed during an investigation are recorded and the integrity of the investigation is preserved", "sort_order": 2},
                        {"code": "RS.AN-07", "title": "Incident data and metadata are collected and their integrity and provenance are preserved", "sort_order": 3},
                    ],
                },
                {
                    "code": "RS.CO",
                    "title": "Incident Response Reporting and Communication",
                    "description": "Response activities are coordinated with internal and external stakeholders as required by laws, regulations, or policies.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "RS.CO-02", "title": "Internal and external stakeholders are notified of incidents", "sort_order": 1},
                        {"code": "RS.CO-03", "title": "Information is shared with designated internal and external stakeholders", "sort_order": 2},
                    ],
                },
                {
                    "code": "RS.MI",
                    "title": "Incident Mitigation",
                    "description": "Activities are performed to prevent expansion of an event and to mitigate its effects.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "RS.MI-01", "title": "Incidents are contained", "sort_order": 1},
                        {"code": "RS.MI-02", "title": "Incidents are eradicated", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "RC",
            "name": "Recover",
            "description": "Assets and operations affected by a cybersecurity incident are restored. The outcomes in this function support timely restoration of normal operations to reduce the impact of cybersecurity incidents.",
            "sort_order": 6,
            "requirements": [
                {
                    "code": "RC.RP",
                    "title": "Incident Recovery Plan Execution",
                    "description": "Restoration activities are performed to ensure operational availability of systems and services affected by cybersecurity incidents.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "RC.RP-01", "title": "The recovery portion of the incident response plan is executed once initiated from the incident response process", "sort_order": 1},
                        {"code": "RC.RP-02", "title": "Recovery actions are selected, scoped, prioritized, and performed", "sort_order": 2},
                        {"code": "RC.RP-03", "title": "The integrity of backups and other restoration assets is verified before using them for restoration", "sort_order": 3},
                        {"code": "RC.RP-04", "title": "Critical mission functions and cybersecurity risk management are considered to establish post-incident operational norms", "sort_order": 4},
                    ],
                },
                {
                    "code": "RC.CO",
                    "title": "Incident Recovery Communication",
                    "description": "Restoration activities are coordinated with internal and external parties.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "RC.CO-03", "title": "Recovery activities and progress in restoring operational capabilities are communicated to designated internal and external stakeholders", "sort_order": 1},
                        {"code": "RC.CO-04", "title": "Public updates on incident recovery are shared using approved methods and messaging", "sort_order": 2},
                    ],
                },
                {
                    "code": "RC.IM",
                    "title": "Incident Recovery Improvements",
                    "description": "Recovery planning and processes are improved by incorporating lessons learned into future activities.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "RC.IM-01", "title": "Recovery plans incorporate lessons learned", "sort_order": 1},
                        {"code": "RC.IM-02", "title": "Recovery strategies are updated", "sort_order": 2},
                    ],
                },
            ],
        },
    ],
}


async def seed_nist_csf_framework(db):
    """Seed the NIST CSF 2.0 framework."""
    from sqlalchemy import select
    from app.models.framework import Framework
    from app.models.framework_domain import FrameworkDomain
    from app.models.framework_requirement import FrameworkRequirement
    from app.models.control_objective import ControlObjective

    # Check if already seeded
    existing = await db.execute(
        select(Framework).where(Framework.name == "NIST CSF")
    )
    if existing.scalar_one_or_none():
        print("  -> NIST CSF framework already seeded, skipping.")
        return

    fw_data = NIST_CSF_FRAMEWORK
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
    print(f"  Seeded NIST CSF 2.0: {req_count} requirements, {obj_count} objectives.")
    return framework
