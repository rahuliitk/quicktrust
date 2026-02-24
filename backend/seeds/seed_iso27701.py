"""ISO 27701:2019 Privacy Information Management System — framework seed data."""

ISO27701_FRAMEWORK = {
    "name": "ISO 27701",
    "version": "2019",
    "category": "Privacy & Data Protection",
    "description": "ISO/IEC 27701:2019 — Privacy Information Management System (PIMS) extension to ISO 27001 and ISO 27002 for privacy management, providing guidance for PII controllers and processors.",
    "domains": [
        {
            "code": "27701.5",
            "name": "Context of the Organization",
            "description": "Understanding the organization, its context, the needs and expectations of interested parties, and determining the scope of the PIMS.",
            "sort_order": 1,
            "requirements": [
                {
                    "code": "27701.5.1",
                    "title": "Understanding the Organization and Its Context",
                    "description": "The organization shall determine external and internal issues relevant to its purpose that affect its ability to achieve the intended outcomes of the PIMS, including applicable privacy legislation and regulations.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "27701.5.1.1", "title": "Privacy-related external and internal issues are identified", "sort_order": 1},
                        {"code": "27701.5.1.2", "title": "Applicable privacy legislation is documented", "sort_order": 2},
                    ],
                },
                {
                    "code": "27701.5.2",
                    "title": "Understanding the Needs and Expectations of Interested Parties",
                    "description": "The organization shall determine interested parties relevant to the PIMS, their requirements, and which of those requirements will be addressed through the PIMS.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "27701.5.2.1", "title": "Interested parties and their privacy requirements are identified", "sort_order": 1},
                        {"code": "27701.5.2.2", "title": "PII principals and their expectations are documented", "sort_order": 2},
                    ],
                },
                {
                    "code": "27701.5.3",
                    "title": "Determining the Scope of the PIMS",
                    "description": "The organization shall determine the boundaries and applicability of the PIMS, including the types of PII processed and the roles (controller/processor) the organization fulfills.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "27701.5.3.1", "title": "PIMS scope includes PII processing activities", "sort_order": 1},
                        {"code": "27701.5.3.2", "title": "Organization roles as PII controller or processor are defined", "sort_order": 2},
                    ],
                },
                {
                    "code": "27701.5.4",
                    "title": "Privacy Information Management System",
                    "description": "The organization shall establish, implement, maintain, and continually improve a privacy information management system in accordance with the requirements of this standard.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "27701.5.4.1", "title": "PIMS is established and integrated with the ISMS", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "27701.6",
            "name": "Leadership",
            "description": "Leadership commitment, privacy policy establishment, and assignment of organizational roles, responsibilities, and authorities for the PIMS.",
            "sort_order": 2,
            "requirements": [
                {
                    "code": "27701.6.1",
                    "title": "Leadership and Commitment",
                    "description": "Top management shall demonstrate leadership and commitment with respect to the PIMS by ensuring the privacy policy and objectives are established and compatible with the strategic direction of the organization.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "27701.6.1.1", "title": "Top management demonstrates commitment to privacy management", "sort_order": 1},
                    ],
                },
                {
                    "code": "27701.6.2",
                    "title": "Privacy Policy",
                    "description": "Top management shall establish a privacy policy that is appropriate to the purpose of the organization, provides a framework for setting privacy objectives, and includes a commitment to satisfy applicable privacy requirements.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "27701.6.2.1", "title": "Privacy policy is established and communicated", "sort_order": 1},
                        {"code": "27701.6.2.2", "title": "Privacy policy is reviewed at planned intervals", "sort_order": 2},
                    ],
                },
                {
                    "code": "27701.6.3",
                    "title": "Organizational Roles, Responsibilities, and Authorities",
                    "description": "Top management shall ensure that responsibilities and authorities for roles relevant to privacy information management are assigned and communicated within the organization.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "27701.6.3.1", "title": "Privacy roles and responsibilities are assigned", "sort_order": 1},
                        {"code": "27701.6.3.2", "title": "A point of contact for PII processing is designated", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "27701.7",
            "name": "Planning",
            "description": "Actions to address privacy risks and opportunities, and planning to achieve privacy objectives.",
            "sort_order": 3,
            "requirements": [
                {
                    "code": "27701.7.1",
                    "title": "Actions to Address Privacy Risks and Opportunities",
                    "description": "When planning for the PIMS, the organization shall consider privacy-specific issues and determine the risks and opportunities that need to be addressed to ensure the PIMS achieves its intended outcomes.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "27701.7.1.1", "title": "Privacy risks and opportunities are identified and assessed", "sort_order": 1},
                        {"code": "27701.7.1.2", "title": "Risk treatment plans address privacy-specific risks", "sort_order": 2},
                    ],
                },
                {
                    "code": "27701.7.2",
                    "title": "Privacy Objectives and Planning to Achieve Them",
                    "description": "The organization shall establish privacy objectives at relevant functions and levels, ensuring they are consistent with the privacy policy and measurable.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "27701.7.2.1", "title": "Privacy objectives are defined and documented", "sort_order": 1},
                        {"code": "27701.7.2.2", "title": "Plans to achieve privacy objectives are established", "sort_order": 2},
                    ],
                },
                {
                    "code": "27701.7.3",
                    "title": "Privacy Impact Assessment",
                    "description": "The organization shall conduct privacy impact assessments where processing of PII may have a significant impact on individuals, and document the results.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "27701.7.3.1", "title": "Privacy impact assessments are conducted for high-risk processing", "sort_order": 1},
                        {"code": "27701.7.3.2", "title": "PIA results are documented and reviewed", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "27701.8",
            "name": "Support",
            "description": "Resources, competence, awareness, communication, and documented information to support the PIMS.",
            "sort_order": 4,
            "requirements": [
                {
                    "code": "27701.8.1",
                    "title": "Resources",
                    "description": "The organization shall determine and provide the resources needed for the establishment, implementation, maintenance, and continual improvement of the PIMS.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "27701.8.1.1", "title": "Adequate resources are allocated for PIMS", "sort_order": 1},
                    ],
                },
                {
                    "code": "27701.8.2",
                    "title": "Competence and Awareness",
                    "description": "The organization shall determine the necessary competence of persons doing work that affects privacy performance and ensure persons are aware of the privacy policy and their contribution to the PIMS.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "27701.8.2.1", "title": "Privacy competence requirements are defined", "sort_order": 1},
                        {"code": "27701.8.2.2", "title": "Privacy awareness training is provided to relevant personnel", "sort_order": 2},
                    ],
                },
                {
                    "code": "27701.8.3",
                    "title": "Communication",
                    "description": "The organization shall determine the need for internal and external communications relevant to the PIMS, including what, when, with whom, and how to communicate.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "27701.8.3.1", "title": "Privacy communication plan is established", "sort_order": 1},
                    ],
                },
                {
                    "code": "27701.8.4",
                    "title": "Documented Information",
                    "description": "The PIMS shall include documented information required by this standard and determined by the organization as being necessary for the effectiveness of the PIMS.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "27701.8.4.1", "title": "PIMS documentation is maintained and controlled", "sort_order": 1},
                        {"code": "27701.8.4.2", "title": "Records of PII processing activities are maintained", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "27701.9",
            "name": "Operation",
            "description": "Operational planning, control, and execution of processes needed to meet PIMS requirements, including PII controller and processor-specific guidance.",
            "sort_order": 5,
            "requirements": [
                {
                    "code": "27701.9.1",
                    "title": "Operational Planning and Control",
                    "description": "The organization shall plan, implement, and control the processes needed to meet PIMS requirements, including managing PII processing operations.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "27701.9.1.1", "title": "PII processing operations are planned and controlled", "sort_order": 1},
                    ],
                },
                {
                    "code": "27701.9.2",
                    "title": "PII Controller Guidance — Conditions for Collection and Processing",
                    "description": "The organization acting as a PII controller shall determine and document the lawful basis for PII processing, obtain and record consent where required, and conduct privacy impact assessments.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "27701.9.2.1", "title": "Lawful basis for PII processing is determined and documented", "sort_order": 1},
                        {"code": "27701.9.2.2", "title": "Consent is obtained and recorded where applicable", "sort_order": 2},
                        {"code": "27701.9.2.3", "title": "Purpose limitation is enforced for all PII processing", "sort_order": 3},
                    ],
                },
                {
                    "code": "27701.9.3",
                    "title": "PII Controller Guidance — Obligations to PII Principals",
                    "description": "The organization acting as a PII controller shall provide mechanisms for PII principals to exercise their rights, including access, correction, erasure, and data portability.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "27701.9.3.1", "title": "Data subject rights mechanisms are implemented", "sort_order": 1},
                        {"code": "27701.9.3.2", "title": "Privacy notices are provided to PII principals", "sort_order": 2},
                    ],
                },
                {
                    "code": "27701.9.4",
                    "title": "PII Processor Guidance",
                    "description": "The organization acting as a PII processor shall process PII only on documented instructions from the controller and implement appropriate technical and organizational measures.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "27701.9.4.1", "title": "PII is processed only on documented controller instructions", "sort_order": 1},
                        {"code": "27701.9.4.2", "title": "Sub-processor engagements are authorized by the controller", "sort_order": 2},
                    ],
                },
                {
                    "code": "27701.9.5",
                    "title": "PII Transfer and Disclosure",
                    "description": "The organization shall identify and document the basis for transfers of PII to other jurisdictions and ensure appropriate safeguards are in place.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "27701.9.5.1", "title": "Cross-border PII transfers are documented with safeguards", "sort_order": 1},
                        {"code": "27701.9.5.2", "title": "Third-party PII disclosures are recorded", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "27701.10",
            "name": "Performance Evaluation",
            "description": "Monitoring, measurement, analysis, evaluation, internal audit, and management review of the PIMS.",
            "sort_order": 6,
            "requirements": [
                {
                    "code": "27701.10.1",
                    "title": "Monitoring, Measurement, Analysis, and Evaluation",
                    "description": "The organization shall determine what needs to be monitored and measured regarding privacy performance, the methods for monitoring and measurement, and when results shall be analyzed and evaluated.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "27701.10.1.1", "title": "Privacy performance metrics are defined and monitored", "sort_order": 1},
                        {"code": "27701.10.1.2", "title": "PII processing compliance is regularly evaluated", "sort_order": 2},
                    ],
                },
                {
                    "code": "27701.10.2",
                    "title": "Internal Audit",
                    "description": "The organization shall conduct internal audits at planned intervals to provide information on whether the PIMS conforms to the organization's own requirements and the requirements of this standard.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "27701.10.2.1", "title": "PIMS internal audits are planned and conducted", "sort_order": 1},
                        {"code": "27701.10.2.2", "title": "Audit findings are reported to management", "sort_order": 2},
                    ],
                },
                {
                    "code": "27701.10.3",
                    "title": "Management Review",
                    "description": "Top management shall review the PIMS at planned intervals to ensure its continuing suitability, adequacy, and effectiveness, including the status of privacy incidents and corrective actions.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "27701.10.3.1", "title": "Management reviews of PIMS are conducted periodically", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "27701.11",
            "name": "Improvement",
            "description": "Nonconformity management, corrective action, and continual improvement of the PIMS.",
            "sort_order": 7,
            "requirements": [
                {
                    "code": "27701.11.1",
                    "title": "Nonconformity and Corrective Action",
                    "description": "When a nonconformity occurs, the organization shall react to the nonconformity, evaluate the need for corrective action, implement any action needed, and review the effectiveness of corrective actions taken.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "27701.11.1.1", "title": "Privacy nonconformities are identified and corrected", "sort_order": 1},
                        {"code": "27701.11.1.2", "title": "Corrective actions for privacy issues are tracked to closure", "sort_order": 2},
                    ],
                },
                {
                    "code": "27701.11.2",
                    "title": "Continual Improvement",
                    "description": "The organization shall continually improve the suitability, adequacy, and effectiveness of the PIMS, incorporating lessons learned from privacy incidents and changes in privacy regulations.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "27701.11.2.1", "title": "PIMS improvement opportunities are identified and acted upon", "sort_order": 1},
                        {"code": "27701.11.2.2", "title": "Changes in privacy regulations are incorporated into the PIMS", "sort_order": 2},
                    ],
                },
                {
                    "code": "27701.11.3",
                    "title": "Privacy Breach Management",
                    "description": "The organization shall establish procedures for identifying, reporting, and managing privacy breaches, including notification to supervisory authorities and affected PII principals where required.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "27701.11.3.1", "title": "Privacy breach procedures are established and tested", "sort_order": 1},
                        {"code": "27701.11.3.2", "title": "Breach notifications are made within required timeframes", "sort_order": 2},
                    ],
                },
            ],
        },
    ],
}


async def seed_iso27701_framework(db):
    """Seed the ISO 27701 framework."""
    from sqlalchemy import select
    from app.models.framework import Framework
    from app.models.framework_domain import FrameworkDomain
    from app.models.framework_requirement import FrameworkRequirement
    from app.models.control_objective import ControlObjective

    # Check if already seeded
    existing = await db.execute(
        select(Framework).where(Framework.name == ISO27701_FRAMEWORK["name"])
    )
    if existing.scalar_one_or_none():
        print("  -> ISO 27701 framework already seeded, skipping.")
        return

    fw_data = ISO27701_FRAMEWORK
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
    print(f"  Seeded ISO 27701: {req_count} requirements, {obj_count} objectives.")
    return framework
