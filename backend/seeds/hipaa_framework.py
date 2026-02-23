"""HIPAA Security Rule — framework seed data with 6 domains."""

HIPAA_FRAMEWORK = {
    "name": "HIPAA Security Rule",
    "version": "2024",
    "category": "Healthcare",
    "description": "HIPAA Security Rule (45 CFR Parts 160 & 164) — Administrative, Physical, and Technical safeguards for protecting electronic protected health information (ePHI).",
    "domains": [
        {
            "code": "ADM",
            "name": "Administrative Safeguards",
            "description": "Administrative actions, policies, and procedures to manage the selection, development, implementation, and maintenance of security measures to protect ePHI (§164.308).",
            "sort_order": 1,
            "requirements": [
                {
                    "code": "§164.308(a)(1)",
                    "title": "Security Management Process",
                    "description": "Implement policies and procedures to prevent, detect, contain, and correct security violations.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "§164.308(a)(1)(ii)(A)", "title": "Risk analysis is conducted", "sort_order": 1},
                        {"code": "§164.308(a)(1)(ii)(B)", "title": "Risk management program is implemented", "sort_order": 2},
                        {"code": "§164.308(a)(1)(ii)(C)", "title": "Sanction policy is applied to workforce members", "sort_order": 3},
                        {"code": "§164.308(a)(1)(ii)(D)", "title": "Information system activity is reviewed", "sort_order": 4},
                    ],
                },
                {
                    "code": "§164.308(a)(2)",
                    "title": "Assigned Security Responsibility",
                    "description": "Identify the security official responsible for developing and implementing security policies.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "§164.308(a)(2).1", "title": "Security officer is designated", "sort_order": 1},
                    ],
                },
                {
                    "code": "§164.308(a)(3)",
                    "title": "Workforce Security",
                    "description": "Implement policies to ensure workforce members have appropriate access to ePHI.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "§164.308(a)(3)(ii)(A)", "title": "Authorization and supervision procedures exist", "sort_order": 1},
                        {"code": "§164.308(a)(3)(ii)(B)", "title": "Workforce clearance procedure is implemented", "sort_order": 2},
                        {"code": "§164.308(a)(3)(ii)(C)", "title": "Termination procedures revoke access", "sort_order": 3},
                    ],
                },
                {
                    "code": "§164.308(a)(4)",
                    "title": "Information Access Management",
                    "description": "Implement policies for authorizing access to ePHI.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "§164.308(a)(4)(ii)(A)", "title": "Isolating healthcare clearinghouse functions", "sort_order": 1},
                        {"code": "§164.308(a)(4)(ii)(B)", "title": "Access authorization policies are defined", "sort_order": 2},
                        {"code": "§164.308(a)(4)(ii)(C)", "title": "Access establishment and modification procedures exist", "sort_order": 3},
                    ],
                },
                {
                    "code": "§164.308(a)(5)",
                    "title": "Security Awareness and Training",
                    "description": "Implement a security awareness and training program for all workforce members.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "§164.308(a)(5)(ii)(A)", "title": "Security reminders are provided", "sort_order": 1},
                        {"code": "§164.308(a)(5)(ii)(B)", "title": "Protection from malicious software", "sort_order": 2},
                        {"code": "§164.308(a)(5)(ii)(C)", "title": "Log-in monitoring procedures are implemented", "sort_order": 3},
                        {"code": "§164.308(a)(5)(ii)(D)", "title": "Password management procedures exist", "sort_order": 4},
                    ],
                },
                {
                    "code": "§164.308(a)(6)",
                    "title": "Security Incident Procedures",
                    "description": "Implement policies and procedures to address security incidents.",
                    "sort_order": 6,
                    "objectives": [
                        {"code": "§164.308(a)(6)(ii)", "title": "Response and reporting procedures exist", "sort_order": 1},
                    ],
                },
                {
                    "code": "§164.308(a)(7)",
                    "title": "Contingency Plan",
                    "description": "Establish policies and procedures for responding to an emergency that damages systems containing ePHI.",
                    "sort_order": 7,
                    "objectives": [
                        {"code": "§164.308(a)(7)(ii)(A)", "title": "Data backup plan is established", "sort_order": 1},
                        {"code": "§164.308(a)(7)(ii)(B)", "title": "Disaster recovery plan is established", "sort_order": 2},
                        {"code": "§164.308(a)(7)(ii)(C)", "title": "Emergency mode operation plan exists", "sort_order": 3},
                        {"code": "§164.308(a)(7)(ii)(D)", "title": "Testing and revision procedures exist", "sort_order": 4},
                        {"code": "§164.308(a)(7)(ii)(E)", "title": "Application and data criticality analysis is performed", "sort_order": 5},
                    ],
                },
                {
                    "code": "§164.308(a)(8)",
                    "title": "Evaluation",
                    "description": "Perform periodic technical and nontechnical evaluation to ensure security policies meet requirements.",
                    "sort_order": 8,
                    "objectives": [
                        {"code": "§164.308(a)(8).1", "title": "Periodic security evaluations are conducted", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "PHY",
            "name": "Physical Safeguards",
            "description": "Physical measures, policies, and procedures to protect electronic information systems and related buildings and equipment from natural and environmental hazards and unauthorized intrusion (§164.310).",
            "sort_order": 2,
            "requirements": [
                {
                    "code": "§164.310(a)",
                    "title": "Facility Access Controls",
                    "description": "Implement policies to limit physical access to electronic information systems.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "§164.310(a)(2)(i)", "title": "Contingency operations facility access procedures exist", "sort_order": 1},
                        {"code": "§164.310(a)(2)(ii)", "title": "Facility security plan is implemented", "sort_order": 2},
                        {"code": "§164.310(a)(2)(iii)", "title": "Access control and validation procedures exist", "sort_order": 3},
                        {"code": "§164.310(a)(2)(iv)", "title": "Maintenance records are documented", "sort_order": 4},
                    ],
                },
                {
                    "code": "§164.310(b)",
                    "title": "Workstation Use",
                    "description": "Implement policies specifying proper functions and physical attributes of workstations accessing ePHI.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "§164.310(b).1", "title": "Workstation use policies are documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "§164.310(c)",
                    "title": "Workstation Security",
                    "description": "Implement physical safeguards for all workstations that access ePHI.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "§164.310(c).1", "title": "Workstation physical safeguards are implemented", "sort_order": 1},
                    ],
                },
                {
                    "code": "§164.310(d)",
                    "title": "Device and Media Controls",
                    "description": "Implement policies governing the receipt and removal of hardware and electronic media containing ePHI.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "§164.310(d)(2)(i)", "title": "Disposal procedures exist for ePHI media", "sort_order": 1},
                        {"code": "§164.310(d)(2)(ii)", "title": "Media re-use procedures remove ePHI", "sort_order": 2},
                        {"code": "§164.310(d)(2)(iii)", "title": "Accountability records track hardware and media", "sort_order": 3},
                        {"code": "§164.310(d)(2)(iv)", "title": "Data backup and storage procedures exist", "sort_order": 4},
                    ],
                },
            ],
        },
        {
            "code": "TEC",
            "name": "Technical Safeguards",
            "description": "Technology and related policies and procedures to protect ePHI and control access to it (§164.312).",
            "sort_order": 3,
            "requirements": [
                {
                    "code": "§164.312(a)",
                    "title": "Access Control",
                    "description": "Implement technical policies to allow access only to authorized persons or software programs.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "§164.312(a)(2)(i)", "title": "Unique user identification is assigned", "sort_order": 1},
                        {"code": "§164.312(a)(2)(ii)", "title": "Emergency access procedure exists", "sort_order": 2},
                        {"code": "§164.312(a)(2)(iii)", "title": "Automatic logoff is implemented", "sort_order": 3},
                        {"code": "§164.312(a)(2)(iv)", "title": "Encryption and decryption mechanisms are used", "sort_order": 4},
                    ],
                },
                {
                    "code": "§164.312(b)",
                    "title": "Audit Controls",
                    "description": "Implement mechanisms to record and examine activity in systems containing ePHI.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "§164.312(b).1", "title": "Audit logging is enabled on ePHI systems", "sort_order": 1},
                    ],
                },
                {
                    "code": "§164.312(c)",
                    "title": "Integrity",
                    "description": "Implement policies to protect ePHI from improper alteration or destruction.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "§164.312(c)(2)", "title": "Mechanism to authenticate ePHI exists", "sort_order": 1},
                    ],
                },
                {
                    "code": "§164.312(d)",
                    "title": "Person or Entity Authentication",
                    "description": "Implement procedures to verify the identity of persons or entities seeking access to ePHI.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "§164.312(d).1", "title": "Authentication mechanisms are implemented", "sort_order": 1},
                    ],
                },
                {
                    "code": "§164.312(e)",
                    "title": "Transmission Security",
                    "description": "Implement technical security measures to guard against unauthorized access to ePHI during electronic transmission.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "§164.312(e)(2)(i)", "title": "Integrity controls for ePHI in transit exist", "sort_order": 1},
                        {"code": "§164.312(e)(2)(ii)", "title": "Encryption is used for ePHI transmission", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "ORG",
            "name": "Organizational Requirements",
            "description": "Organizational requirements for business associate contracts and group health plan administration (§164.314).",
            "sort_order": 4,
            "requirements": [
                {
                    "code": "§164.314(a)",
                    "title": "Business Associate Contracts",
                    "description": "Business associate contracts or other arrangements must include satisfactory assurances regarding ePHI safeguards.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "§164.314(a)(2)(i)", "title": "BAA contracts include required security provisions", "sort_order": 1},
                        {"code": "§164.314(a)(2)(ii)", "title": "Other arrangements meet BAA requirements", "sort_order": 2},
                    ],
                },
                {
                    "code": "§164.314(b)",
                    "title": "Requirements for Group Health Plans",
                    "description": "Group health plans must ensure adequate safeguards for ePHI received from or created on behalf of the plan sponsor.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "§164.314(b)(2)(i)", "title": "Plan documents include required security provisions", "sort_order": 1},
                        {"code": "§164.314(b)(2)(ii)", "title": "Adequate separation between plan and sponsor is ensured", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "PNP",
            "name": "Policies & Documentation",
            "description": "Requirements for maintaining policies, procedures, and documentation (§164.316).",
            "sort_order": 5,
            "requirements": [
                {
                    "code": "§164.316(a)",
                    "title": "Policies and Procedures",
                    "description": "Implement reasonable and appropriate policies and procedures to comply with the Security Rule.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "§164.316(a).1", "title": "Security policies and procedures are documented", "sort_order": 1},
                        {"code": "§164.316(a).2", "title": "Policies are reviewed and updated regularly", "sort_order": 2},
                    ],
                },
                {
                    "code": "§164.316(b)",
                    "title": "Documentation",
                    "description": "Maintain written documentation of policies, procedures, actions, activities, or assessments required by the Security Rule.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "§164.316(b)(2)(i)", "title": "Documentation is retained for 6 years", "sort_order": 1},
                        {"code": "§164.316(b)(2)(ii)", "title": "Documentation is available to authorized persons", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "BNR",
            "name": "Breach Notification Rule",
            "description": "Requirements for notification following a breach of unsecured PHI (§164.400-414).",
            "sort_order": 6,
            "requirements": [
                {
                    "code": "§164.404",
                    "title": "Notification to Individuals",
                    "description": "Covered entities must notify affected individuals following discovery of a breach of unsecured PHI.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "§164.404(a)", "title": "Individual notification is provided within 60 days", "sort_order": 1},
                        {"code": "§164.404(d)", "title": "Notification content includes required elements", "sort_order": 2},
                    ],
                },
                {
                    "code": "§164.406",
                    "title": "Notification to Media",
                    "description": "For breaches affecting 500+ residents of a state, prominent media outlets must be notified.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "§164.406(a)", "title": "Media notification occurs for large breaches", "sort_order": 1},
                    ],
                },
                {
                    "code": "§164.408",
                    "title": "Notification to HHS Secretary",
                    "description": "Covered entities must notify the HHS Secretary of breaches of unsecured PHI.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "§164.408(a)", "title": "HHS notification is submitted for breaches of 500+", "sort_order": 1},
                        {"code": "§164.408(c)", "title": "Annual log of smaller breaches is submitted", "sort_order": 2},
                    ],
                },
            ],
        },
    ],
}


async def seed_hipaa_framework(db):
    """Seed the HIPAA Security Rule framework."""
    from sqlalchemy import select
    from app.models.framework import Framework
    from app.models.framework_domain import FrameworkDomain
    from app.models.framework_requirement import FrameworkRequirement
    from app.models.control_objective import ControlObjective

    # Check if already seeded
    existing = await db.execute(
        select(Framework).where(Framework.name == "HIPAA Security Rule")
    )
    if existing.scalar_one_or_none():
        print("HIPAA Security Rule already seeded, skipping.")
        return

    fw_data = HIPAA_FRAMEWORK
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
    print(f"Seeded HIPAA Security Rule: {req_count} requirements, {obj_count} objectives.")
    return framework
