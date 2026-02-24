"""SOX IT Controls (Sarbanes-Oxley Act) — framework seed data."""

SOX_FRAMEWORK = {
    "name": "SOX IT Controls",
    "version": "2002",
    "category": "Financial & Regulatory",
    "description": "Sarbanes-Oxley Act IT Controls — IT general controls, application controls, and entity-level controls required to support the integrity of financial reporting systems and compliance with SOX Section 404.",
    "domains": [
        {
            "code": "SOX.ITGC",
            "name": "IT General Controls",
            "description": "IT general controls that provide the foundation for reliance on IT-dependent financial reporting controls, including logical access, change management, computer operations, and program development.",
            "sort_order": 1,
            "requirements": [
                {
                    "code": "SOX.ITGC.1",
                    "title": "Logical Access to Programs and Data",
                    "description": "Controls to ensure that access to programs and data is restricted to authorized individuals based on job responsibilities, and that access is appropriately provisioned, reviewed, and revoked.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "SOX.ITGC.1a", "title": "Logical access to financial systems is restricted to authorized users", "sort_order": 1},
                        {"code": "SOX.ITGC.1b", "title": "Access provisioning requires documented approval", "sort_order": 2},
                    ],
                },
                {
                    "code": "SOX.ITGC.2",
                    "title": "Program Change Management",
                    "description": "Controls to ensure that changes to IT programs and infrastructure are authorized, tested, approved, and properly implemented to maintain the integrity of financial reporting systems.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "SOX.ITGC.2a", "title": "Program changes follow formal change management process", "sort_order": 1},
                        {"code": "SOX.ITGC.2b", "title": "Changes are tested and approved before production deployment", "sort_order": 2},
                    ],
                },
                {
                    "code": "SOX.ITGC.3",
                    "title": "Program Development",
                    "description": "Controls to ensure that new programs and systems are developed, tested, and implemented in a controlled manner with adequate documentation and authorization.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "SOX.ITGC.3a", "title": "New system development follows documented SDLC methodology", "sort_order": 1},
                        {"code": "SOX.ITGC.3b", "title": "User acceptance testing is completed before go-live", "sort_order": 2},
                    ],
                },
                {
                    "code": "SOX.ITGC.4",
                    "title": "Computer Operations",
                    "description": "Controls over IT operations to ensure that processing is complete, accurate, and authorized, including job scheduling, backup and recovery, and incident management.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "SOX.ITGC.4a", "title": "Batch job processing is monitored for completeness", "sort_order": 1},
                        {"code": "SOX.ITGC.4b", "title": "Backup and recovery procedures are tested regularly", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "SOX.AC",
            "name": "Application Controls",
            "description": "Automated controls embedded within business applications to ensure the completeness, accuracy, authorization, and validity of transaction processing for financial reporting.",
            "sort_order": 2,
            "requirements": [
                {
                    "code": "SOX.AC.1",
                    "title": "Input Controls",
                    "description": "Controls to ensure that data entered into financial applications is complete, accurate, authorized, and valid, including edit checks, validation rules, and authorization of input transactions.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "SOX.AC.1a", "title": "Input validation rules enforce data accuracy", "sort_order": 1},
                        {"code": "SOX.AC.1b", "title": "Transaction authorization is enforced at input", "sort_order": 2},
                    ],
                },
                {
                    "code": "SOX.AC.2",
                    "title": "Processing Controls",
                    "description": "Controls to ensure that transactions are processed completely and accurately by financial applications, including calculation verification, balancing controls, and exception handling.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "SOX.AC.2a", "title": "Automated calculations are verified for accuracy", "sort_order": 1},
                        {"code": "SOX.AC.2b", "title": "Processing exceptions are captured and resolved", "sort_order": 2},
                    ],
                },
                {
                    "code": "SOX.AC.3",
                    "title": "Output Controls",
                    "description": "Controls to ensure that outputs from financial applications are complete, accurate, and distributed only to authorized recipients, including report distribution controls and reconciliation procedures.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "SOX.AC.3a", "title": "Financial reports are distributed to authorized recipients only", "sort_order": 1},
                        {"code": "SOX.AC.3b", "title": "Output reconciliations are performed regularly", "sort_order": 2},
                    ],
                },
                {
                    "code": "SOX.AC.4",
                    "title": "Interface Controls",
                    "description": "Controls over data transferred between applications to ensure completeness and accuracy of data in transit, including reconciliation of records transferred and error handling procedures.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "SOX.AC.4a", "title": "Interface transfers are reconciled for completeness", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "SOX.ELC",
            "name": "Entity-Level Controls",
            "description": "Organization-wide controls that establish the tone at the top, control environment, risk assessment processes, and monitoring activities that impact the effectiveness of IT and financial reporting controls.",
            "sort_order": 3,
            "requirements": [
                {
                    "code": "SOX.ELC.1",
                    "title": "Control Environment and Tone at the Top",
                    "description": "Management demonstrates commitment to integrity and ethical values, and the board of directors exercises oversight responsibility for internal controls over financial reporting.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "SOX.ELC.1a", "title": "Code of conduct is established and enforced", "sort_order": 1},
                        {"code": "SOX.ELC.1b", "title": "Board audit committee oversight is active", "sort_order": 2},
                    ],
                },
                {
                    "code": "SOX.ELC.2",
                    "title": "IT Risk Assessment",
                    "description": "The organization performs IT risk assessments to identify and assess risks that may affect the integrity of financial reporting, including risks from IT systems, applications, and third-party service providers.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "SOX.ELC.2a", "title": "IT risk assessments are performed for financial reporting systems", "sort_order": 1},
                    ],
                },
                {
                    "code": "SOX.ELC.3",
                    "title": "IT Policies and Procedures",
                    "description": "IT policies and procedures are documented, communicated, and enforced to provide a framework for managing IT risks that could impact financial reporting.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "SOX.ELC.3a", "title": "IT policies supporting financial reporting are documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "SOX.ELC.4",
                    "title": "IT Monitoring and Self-Assessment",
                    "description": "Management monitors the effectiveness of IT controls through ongoing evaluations and separate evaluations, and deficiencies are identified and communicated in a timely manner.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "SOX.ELC.4a", "title": "IT control effectiveness is monitored and evaluated", "sort_order": 1},
                        {"code": "SOX.ELC.4b", "title": "IT control deficiencies are reported to management", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "SOX.AM",
            "name": "Access Management",
            "description": "Controls for managing user access to IT systems supporting financial reporting, including user provisioning, periodic access reviews, and privileged access management.",
            "sort_order": 4,
            "requirements": [
                {
                    "code": "SOX.AM.1",
                    "title": "User Provisioning and Deprovisioning",
                    "description": "User access to financial reporting systems is provisioned based on documented approval from authorized personnel, and access is promptly removed when no longer required.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "SOX.AM.1a", "title": "Access provisioning requires management approval", "sort_order": 1},
                        {"code": "SOX.AM.1b", "title": "Access is revoked within defined timeframe upon termination", "sort_order": 2},
                    ],
                },
                {
                    "code": "SOX.AM.2",
                    "title": "Periodic Access Reviews",
                    "description": "User access to financial reporting applications and infrastructure components is reviewed periodically by management to confirm that access remains appropriate and aligned with job responsibilities.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "SOX.AM.2a", "title": "Access reviews are conducted at least quarterly", "sort_order": 1},
                        {"code": "SOX.AM.2b", "title": "Inappropriate access identified in reviews is remediated", "sort_order": 2},
                    ],
                },
                {
                    "code": "SOX.AM.3",
                    "title": "Privileged Access Controls",
                    "description": "Access to privileged accounts (e.g., administrators, database owners) is restricted, monitored, and reviewed with enhanced scrutiny due to the elevated risk to financial reporting integrity.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "SOX.AM.3a", "title": "Privileged access is restricted to authorized administrators", "sort_order": 1},
                        {"code": "SOX.AM.3b", "title": "Privileged access activity is logged and reviewed", "sort_order": 2},
                    ],
                },
                {
                    "code": "SOX.AM.4",
                    "title": "Authentication Controls",
                    "description": "Authentication mechanisms for financial reporting systems enforce strong password policies, account lockout, session timeout, and multi-factor authentication where appropriate.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "SOX.AM.4a", "title": "Password policies enforce minimum complexity requirements", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "SOX.CM",
            "name": "Change Management",
            "description": "Controls governing changes to IT systems, applications, and infrastructure that support financial reporting, including change authorization, testing, and emergency change procedures.",
            "sort_order": 5,
            "requirements": [
                {
                    "code": "SOX.CM.1",
                    "title": "Change Authorization",
                    "description": "All changes to financial reporting systems are authorized by appropriate management before implementation, with documented approval and risk assessment.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "SOX.CM.1a", "title": "Changes are authorized by management before implementation", "sort_order": 1},
                    ],
                },
                {
                    "code": "SOX.CM.2",
                    "title": "Change Testing",
                    "description": "Changes to financial reporting systems are tested in a non-production environment to verify that the change functions as intended and does not adversely affect existing functionality.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "SOX.CM.2a", "title": "Changes are tested before production deployment", "sort_order": 1},
                        {"code": "SOX.CM.2b", "title": "Test results are documented and reviewed", "sort_order": 2},
                    ],
                },
                {
                    "code": "SOX.CM.3",
                    "title": "Emergency Change Procedures",
                    "description": "Emergency changes to production financial systems follow expedited but controlled procedures with after-the-fact documentation, review, and approval.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "SOX.CM.3a", "title": "Emergency changes are documented and reviewed after implementation", "sort_order": 1},
                    ],
                },
                {
                    "code": "SOX.CM.4",
                    "title": "Segregation of Development and Production",
                    "description": "Development and production environments are segregated, and developers do not have the ability to promote changes directly to production without independent review and approval.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "SOX.CM.4a", "title": "Development and production environments are segregated", "sort_order": 1},
                        {"code": "SOX.CM.4b", "title": "Production migration requires independent approval", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "SOX.OPS",
            "name": "IT Operations",
            "description": "Controls over IT operations including system availability, data backup and recovery, job scheduling, and incident management to support the continuity and integrity of financial reporting.",
            "sort_order": 6,
            "requirements": [
                {
                    "code": "SOX.OPS.1",
                    "title": "Data Backup and Recovery",
                    "description": "Regular backups of financial data and systems are performed, stored securely, and tested for recoverability to ensure financial reporting can continue in the event of system failure.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "SOX.OPS.1a", "title": "Financial data backups are performed on schedule", "sort_order": 1},
                        {"code": "SOX.OPS.1b", "title": "Backup restoration is tested at least annually", "sort_order": 2},
                    ],
                },
                {
                    "code": "SOX.OPS.2",
                    "title": "Job Scheduling and Monitoring",
                    "description": "Automated batch jobs that process financial transactions are scheduled, monitored for successful completion, and exceptions are investigated and resolved timely.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "SOX.OPS.2a", "title": "Batch job completion is monitored daily", "sort_order": 1},
                    ],
                },
                {
                    "code": "SOX.OPS.3",
                    "title": "Incident Management",
                    "description": "IT incidents affecting financial reporting systems are identified, logged, categorized, resolved, and reported to management, with root cause analysis for significant incidents.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "SOX.OPS.3a", "title": "Incidents affecting financial systems are tracked and resolved", "sort_order": 1},
                        {"code": "SOX.OPS.3b", "title": "Root cause analysis is performed for significant incidents", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "SOX.SOD",
            "name": "Segregation of Duties",
            "description": "Controls to ensure that conflicting duties are segregated within IT and business processes to prevent a single individual from having the ability to initiate, authorize, record, and reconcile financial transactions.",
            "sort_order": 7,
            "requirements": [
                {
                    "code": "SOX.SOD.1",
                    "title": "SOD Matrix and Analysis",
                    "description": "The organization defines and maintains a segregation of duties matrix identifying conflicting roles and responsibilities within financial reporting processes and IT systems.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "SOX.SOD.1a", "title": "SOD matrix is defined for financial processes", "sort_order": 1},
                        {"code": "SOX.SOD.1b", "title": "SOD conflicts are identified and documented", "sort_order": 2},
                    ],
                },
                {
                    "code": "SOX.SOD.2",
                    "title": "SOD Enforcement in Applications",
                    "description": "Financial applications enforce segregation of duties through role-based access controls that prevent users from holding conflicting roles (e.g., creating and approving purchase orders).",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "SOX.SOD.2a", "title": "Application role assignments enforce SOD requirements", "sort_order": 1},
                    ],
                },
                {
                    "code": "SOX.SOD.3",
                    "title": "Compensating Controls for SOD Violations",
                    "description": "Where segregation of duties conflicts cannot be eliminated, compensating controls such as management review, reconciliation, and monitoring are implemented and documented.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "SOX.SOD.3a", "title": "Compensating controls are documented for SOD exceptions", "sort_order": 1},
                        {"code": "SOX.SOD.3b", "title": "Management monitors and reviews SOD exceptions", "sort_order": 2},
                    ],
                },
            ],
        },
    ],
}


async def seed_sox_framework(db):
    """Seed the SOX IT Controls framework."""
    from sqlalchemy import select
    from app.models.framework import Framework
    from app.models.framework_domain import FrameworkDomain
    from app.models.framework_requirement import FrameworkRequirement
    from app.models.control_objective import ControlObjective

    # Check if already seeded
    existing = await db.execute(
        select(Framework).where(Framework.name == SOX_FRAMEWORK["name"])
    )
    if existing.scalar_one_or_none():
        print("  -> SOX IT Controls framework already seeded, skipping.")
        return

    fw_data = SOX_FRAMEWORK
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
    print(f"  Seeded SOX IT Controls: {req_count} requirements, {obj_count} objectives.")
    return framework
