"""GDPR (General Data Protection Regulation) — framework seed data with 3 domains."""

GDPR_FRAMEWORK = {
    "name": "GDPR",
    "version": "2016/679",
    "category": "Privacy & Data Protection",
    "description": "EU General Data Protection Regulation (Regulation 2016/679) — comprehensive data protection law governing the collection, processing, and storage of personal data of individuals in the European Union.",
    "domains": [
        {
            "code": "DSR",
            "name": "Data Subject Rights",
            "description": "Rights granted to data subjects under GDPR including the right to access, erasure, rectification, and to be informed about the processing of their personal data.",
            "sort_order": 1,
            "requirements": [
                {
                    "code": "Art.13-14",
                    "title": "Transparency — Right to be Informed",
                    "description": "Controllers must provide data subjects with clear, transparent information about data processing activities at the time personal data is obtained (Art 13 — collected from the data subject; Art 14 — obtained from other sources).",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "Art.13.1", "title": "Identity and contact details of the controller are communicated", "sort_order": 1},
                        {"code": "Art.13.2", "title": "Purpose and legal basis for processing are disclosed", "sort_order": 2},
                        {"code": "Art.14.1", "title": "Categories of personal data obtained indirectly are disclosed", "sort_order": 3},
                        {"code": "Art.14.2", "title": "Source of personal data not collected directly is communicated", "sort_order": 4},
                    ],
                },
                {
                    "code": "Art.15",
                    "title": "Right of Access",
                    "description": "Data subjects have the right to obtain confirmation as to whether their personal data is being processed, and where that is the case, access to the personal data and supplementary information.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "Art.15.1", "title": "Process exists to confirm whether personal data is being processed", "sort_order": 1},
                        {"code": "Art.15.2", "title": "Copy of personal data is provided upon request", "sort_order": 2},
                        {"code": "Art.15.3", "title": "Response to access requests is provided within one month", "sort_order": 3},
                    ],
                },
                {
                    "code": "Art.17",
                    "title": "Right to Erasure (Right to be Forgotten)",
                    "description": "Data subjects have the right to request the erasure of personal data without undue delay where certain grounds apply, including when data is no longer necessary for the purpose for which it was collected.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "Art.17.1", "title": "Process exists to erase personal data upon valid request", "sort_order": 1},
                        {"code": "Art.17.2", "title": "Third parties are notified of erasure obligations", "sort_order": 2},
                        {"code": "Art.17.3", "title": "Exceptions to erasure right are documented and applied correctly", "sort_order": 3},
                    ],
                },
            ],
        },
        {
            "code": "CTR",
            "name": "Controller Obligations",
            "description": "Obligations placed on data controllers under GDPR, including ensuring lawful processing, data protection by design, data protection impact assessments, processor management, and designation of a Data Protection Officer.",
            "sort_order": 2,
            "requirements": [
                {
                    "code": "Art.5",
                    "title": "Principles Relating to Processing of Personal Data",
                    "description": "Personal data must be processed lawfully, fairly, and transparently; collected for specified, explicit, and legitimate purposes; adequate, relevant, and limited; accurate; kept for no longer than necessary; and processed with appropriate security (integrity and confidentiality).",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "Art.5.1a", "title": "Processing is lawful, fair, and transparent", "sort_order": 1},
                        {"code": "Art.5.1b", "title": "Data is collected for specified, explicit, and legitimate purposes", "sort_order": 2},
                        {"code": "Art.5.1c", "title": "Data is adequate, relevant, and limited to what is necessary", "sort_order": 3},
                        {"code": "Art.5.1d", "title": "Data is accurate and kept up to date", "sort_order": 4},
                        {"code": "Art.5.1e", "title": "Data is retained only as long as necessary", "sort_order": 5},
                        {"code": "Art.5.1f", "title": "Data is processed with appropriate security measures", "sort_order": 6},
                        {"code": "Art.5.2", "title": "Controller can demonstrate compliance (accountability)", "sort_order": 7},
                    ],
                },
                {
                    "code": "Art.6",
                    "title": "Lawfulness of Processing",
                    "description": "Processing is lawful only if and to the extent that at least one of six legal bases applies: consent, contractual necessity, legal obligation, vital interests, public task, or legitimate interests.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "Art.6.1a", "title": "Consent is obtained and documented where used as legal basis", "sort_order": 1},
                        {"code": "Art.6.1b", "title": "Processing necessary for contract performance is identified", "sort_order": 2},
                        {"code": "Art.6.1c", "title": "Processing necessary for legal obligations is documented", "sort_order": 3},
                        {"code": "Art.6.1f", "title": "Legitimate interest assessments are performed and recorded", "sort_order": 4},
                    ],
                },
                {
                    "code": "Art.25",
                    "title": "Data Protection by Design and by Default",
                    "description": "Controllers must implement appropriate technical and organisational measures designed to implement data protection principles and integrate safeguards into processing, both at the time of determination and during processing itself.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "Art.25.1", "title": "Data protection measures are integrated into system design", "sort_order": 1},
                        {"code": "Art.25.2", "title": "Default settings ensure only necessary data is processed", "sort_order": 2},
                        {"code": "Art.25.3", "title": "Privacy-enhancing technologies are evaluated and implemented", "sort_order": 3},
                    ],
                },
                {
                    "code": "Art.28",
                    "title": "Processor Obligations",
                    "description": "Controllers must only use processors that provide sufficient guarantees to implement appropriate technical and organisational measures. Processing by a processor must be governed by a contract or legal act.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "Art.28.1", "title": "Processors provide sufficient guarantees for data protection", "sort_order": 1},
                        {"code": "Art.28.3", "title": "Data processing agreements are in place with all processors", "sort_order": 2},
                        {"code": "Art.28.4", "title": "Sub-processor engagements are authorized and documented", "sort_order": 3},
                    ],
                },
                {
                    "code": "Art.35",
                    "title": "Data Protection Impact Assessment (DPIA)",
                    "description": "Where processing is likely to result in a high risk to the rights and freedoms of natural persons, the controller must carry out an assessment of the impact of the envisaged processing operations on the protection of personal data.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "Art.35.1", "title": "DPIAs are conducted for high-risk processing activities", "sort_order": 1},
                        {"code": "Art.35.7a", "title": "DPIA includes systematic description of processing operations", "sort_order": 2},
                        {"code": "Art.35.7b", "title": "DPIA assesses necessity and proportionality of processing", "sort_order": 3},
                        {"code": "Art.35.7c", "title": "DPIA assesses risks to rights and freedoms of data subjects", "sort_order": 4},
                        {"code": "Art.35.7d", "title": "DPIA documents measures to address identified risks", "sort_order": 5},
                    ],
                },
                {
                    "code": "Art.37-39",
                    "title": "Data Protection Officer (DPO)",
                    "description": "Controllers and processors must designate a Data Protection Officer where required. The DPO must have expert knowledge of data protection law, operate independently, and perform defined tasks including monitoring compliance and cooperating with the supervisory authority.",
                    "sort_order": 6,
                    "objectives": [
                        {"code": "Art.37.1", "title": "DPO is designated where required by regulation", "sort_order": 1},
                        {"code": "Art.38.3", "title": "DPO operates independently without conflicts of interest", "sort_order": 2},
                        {"code": "Art.39.1", "title": "DPO monitors compliance and provides advice on data protection", "sort_order": 3},
                        {"code": "Art.39.2", "title": "DPO cooperates with the supervisory authority", "sort_order": 4},
                    ],
                },
            ],
        },
        {
            "code": "SBR",
            "name": "Security & Breach",
            "description": "Requirements for securing personal data processing and notifying authorities and data subjects in the event of a personal data breach.",
            "sort_order": 3,
            "requirements": [
                {
                    "code": "Art.32",
                    "title": "Security of Processing",
                    "description": "Controllers and processors must implement appropriate technical and organisational measures to ensure a level of security appropriate to the risk, including pseudonymisation, encryption, confidentiality, integrity, availability, resilience, and regular testing.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "Art.32.1a", "title": "Pseudonymisation and encryption of personal data are implemented", "sort_order": 1},
                        {"code": "Art.32.1b", "title": "Confidentiality, integrity, availability, and resilience of processing systems are ensured", "sort_order": 2},
                        {"code": "Art.32.1c", "title": "Ability to restore availability and access to personal data in a timely manner", "sort_order": 3},
                        {"code": "Art.32.1d", "title": "Regular testing, assessing, and evaluating effectiveness of security measures", "sort_order": 4},
                        {"code": "Art.32.4", "title": "Persons acting under authority of the controller process data only on instruction", "sort_order": 5},
                    ],
                },
                {
                    "code": "Art.33",
                    "title": "Notification of a Personal Data Breach to the Supervisory Authority",
                    "description": "In the case of a personal data breach, the controller must notify the competent supervisory authority without undue delay and, where feasible, not later than 72 hours after becoming aware of it.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "Art.33.1", "title": "Breach is notified to supervisory authority within 72 hours", "sort_order": 1},
                        {"code": "Art.33.3", "title": "Notification includes nature of breach, categories and number of data subjects affected", "sort_order": 2},
                        {"code": "Art.33.5", "title": "Breach documentation is maintained for all personal data breaches", "sort_order": 3},
                    ],
                },
                {
                    "code": "Art.34",
                    "title": "Communication of a Personal Data Breach to the Data Subject",
                    "description": "When a personal data breach is likely to result in a high risk to the rights and freedoms of natural persons, the controller must communicate the breach to the data subject without undue delay.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "Art.34.1", "title": "Data subjects are notified without undue delay for high-risk breaches", "sort_order": 1},
                        {"code": "Art.34.2", "title": "Communication describes nature of breach and recommended mitigation measures", "sort_order": 2},
                        {"code": "Art.34.3", "title": "Exceptions to direct communication are documented and justified", "sort_order": 3},
                    ],
                },
            ],
        },
    ],
}


async def seed_gdpr_framework(db):
    """Seed the GDPR framework."""
    from sqlalchemy import select
    from app.models.framework import Framework
    from app.models.framework_domain import FrameworkDomain
    from app.models.framework_requirement import FrameworkRequirement
    from app.models.control_objective import ControlObjective

    # Check if already seeded
    existing = await db.execute(
        select(Framework).where(Framework.name == "GDPR")
    )
    if existing.scalar_one_or_none():
        print("  -> GDPR framework already seeded, skipping.")
        return

    fw_data = GDPR_FRAMEWORK
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
    print(f"  Seeded GDPR: {req_count} requirements, {obj_count} objectives.")
    return framework
