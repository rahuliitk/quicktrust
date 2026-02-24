"""CCPA/CPRA (California Consumer Privacy Act / California Privacy Rights Act) — framework seed data."""

CCPA_FRAMEWORK = {
    "name": "CCPA/CPRA",
    "version": "2023",
    "category": "Privacy & Data Protection",
    "description": "California Consumer Privacy Act (CCPA) as amended by the California Privacy Rights Act (CPRA) — comprehensive consumer privacy law granting California residents rights over their personal information and imposing obligations on businesses that collect, process, or sell personal information.",
    "domains": [
        {
            "code": "CCPA.1",
            "name": "Consumer Rights",
            "description": "Rights granted to California consumers under the CCPA/CPRA including the right to know, delete, correct, opt-out, and limit the use of sensitive personal information.",
            "sort_order": 1,
            "requirements": [
                {
                    "code": "CCPA.1.1",
                    "title": "Right to Know",
                    "description": "Consumers have the right to request that a business disclose the categories and specific pieces of personal information it has collected about them, the categories of sources, the business or commercial purpose, and the categories of third parties with whom the business shares personal information.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CCPA.1.1a", "title": "Process exists to respond to consumer right-to-know requests", "sort_order": 1},
                        {"code": "CCPA.1.1b", "title": "Responses are provided within 45 days of request", "sort_order": 2},
                    ],
                },
                {
                    "code": "CCPA.1.2",
                    "title": "Right to Delete",
                    "description": "Consumers have the right to request deletion of personal information collected from them, subject to specified exceptions, and the business must direct service providers and contractors to delete the information.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CCPA.1.2a", "title": "Deletion request process is implemented", "sort_order": 1},
                        {"code": "CCPA.1.2b", "title": "Service providers are notified to delete consumer data", "sort_order": 2},
                    ],
                },
                {
                    "code": "CCPA.1.3",
                    "title": "Right to Correct",
                    "description": "Consumers have the right to request that a business correct inaccurate personal information that it maintains about the consumer.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CCPA.1.3a", "title": "Correction request process is implemented", "sort_order": 1},
                    ],
                },
                {
                    "code": "CCPA.1.4",
                    "title": "Right to Opt-Out of Sale or Sharing",
                    "description": "Consumers have the right to direct a business that sells or shares their personal information to stop selling or sharing their personal information (Do Not Sell or Share My Personal Information).",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CCPA.1.4a", "title": "Opt-out mechanism is provided (Do Not Sell or Share link)", "sort_order": 1},
                        {"code": "CCPA.1.4b", "title": "Opt-out preferences are honored and propagated", "sort_order": 2},
                    ],
                },
                {
                    "code": "CCPA.1.5",
                    "title": "Right to Limit Use of Sensitive Personal Information",
                    "description": "Consumers have the right to limit a business's use of their sensitive personal information to that which is necessary to perform the services or provide the goods reasonably expected.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "CCPA.1.5a", "title": "Limit Use link is provided for sensitive PI", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CCPA.2",
            "name": "Data Collection",
            "description": "Requirements governing how businesses collect personal information, including purpose limitation, data minimization, and notice at collection.",
            "sort_order": 2,
            "requirements": [
                {
                    "code": "CCPA.2.1",
                    "title": "Notice at Collection",
                    "description": "At or before the point of collection, businesses must inform consumers of the categories of personal information to be collected, the purposes for which the categories will be used, and whether that information is sold or shared.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CCPA.2.1a", "title": "Notice at collection is provided before data collection", "sort_order": 1},
                        {"code": "CCPA.2.1b", "title": "Notice includes categories and purposes of collection", "sort_order": 2},
                    ],
                },
                {
                    "code": "CCPA.2.2",
                    "title": "Purpose Limitation",
                    "description": "Businesses shall not collect, use, retain, or share personal information for purposes that are incompatible with the disclosed purposes for which the personal information was collected.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CCPA.2.2a", "title": "Personal information use is limited to disclosed purposes", "sort_order": 1},
                    ],
                },
                {
                    "code": "CCPA.2.3",
                    "title": "Data Minimization",
                    "description": "The collection, use, retention, and sharing of a consumer's personal information shall be reasonably necessary and proportionate to achieve the purposes for which the personal information was collected.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CCPA.2.3a", "title": "Data collection is limited to what is necessary", "sort_order": 1},
                    ],
                },
                {
                    "code": "CCPA.2.4",
                    "title": "Retention Limitation",
                    "description": "Businesses shall not retain consumers' personal information for longer than is reasonably necessary for the disclosed purpose for which it was collected.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CCPA.2.4a", "title": "Retention periods are defined and enforced", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CCPA.3",
            "name": "Data Sharing and Sale",
            "description": "Requirements governing the sale and sharing of personal information, including opt-out rights, cross-context behavioral advertising, and obligations to honor consumer preferences.",
            "sort_order": 3,
            "requirements": [
                {
                    "code": "CCPA.3.1",
                    "title": "Sale of Personal Information",
                    "description": "Businesses that sell personal information must provide a clear and conspicuous link titled 'Do Not Sell My Personal Information' on their website and must not sell the personal information of consumers who have opted out.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CCPA.3.1a", "title": "Do Not Sell link is conspicuously displayed", "sort_order": 1},
                        {"code": "CCPA.3.1b", "title": "Opt-out requests are processed within 15 business days", "sort_order": 2},
                    ],
                },
                {
                    "code": "CCPA.3.2",
                    "title": "Sharing for Cross-Context Behavioral Advertising",
                    "description": "Businesses that share personal information for cross-context behavioral advertising must provide consumers with the right to opt out and must honor the Global Privacy Control signal.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CCPA.3.2a", "title": "Global Privacy Control signals are recognized and honored", "sort_order": 1},
                    ],
                },
                {
                    "code": "CCPA.3.3",
                    "title": "Third-Party Obligations",
                    "description": "Third parties that receive personal information from a business must comply with the CCPA/CPRA and must not sell or share the information beyond what was specified at the point of collection.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CCPA.3.3a", "title": "Third-party data use agreements are in place", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CCPA.4",
            "name": "Privacy Notices",
            "description": "Requirements for privacy notices and disclosures including the privacy policy, financial incentive notices, and notice of right to opt-out.",
            "sort_order": 4,
            "requirements": [
                {
                    "code": "CCPA.4.1",
                    "title": "Privacy Policy",
                    "description": "Businesses must make available to consumers a privacy policy that is updated at least every 12 months and includes all categories of personal information collected, purposes, consumer rights, and how to exercise those rights.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CCPA.4.1a", "title": "Privacy policy is published and updated annually", "sort_order": 1},
                        {"code": "CCPA.4.1b", "title": "Privacy policy includes all CCPA-required disclosures", "sort_order": 2},
                    ],
                },
                {
                    "code": "CCPA.4.2",
                    "title": "Financial Incentive Notice",
                    "description": "Businesses offering financial incentives for the collection, sale, or deletion of personal information must provide a notice describing the material terms of the financial incentive program.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CCPA.4.2a", "title": "Financial incentive programs are disclosed with material terms", "sort_order": 1},
                    ],
                },
                {
                    "code": "CCPA.4.3",
                    "title": "Accessibility of Notices",
                    "description": "All privacy notices, disclosures, and request mechanisms must be accessible to consumers with disabilities and available in the languages in which the business provides services.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CCPA.4.3a", "title": "Privacy notices are accessible and available in supported languages", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CCPA.5",
            "name": "Data Security",
            "description": "Requirements for implementing and maintaining reasonable security procedures and practices to protect consumers' personal information.",
            "sort_order": 5,
            "requirements": [
                {
                    "code": "CCPA.5.1",
                    "title": "Reasonable Security Measures",
                    "description": "Businesses shall implement and maintain reasonable security procedures and practices appropriate to the nature of the personal information to protect it from unauthorized or illegal access, destruction, use, modification, or disclosure.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CCPA.5.1a", "title": "Reasonable security procedures are implemented", "sort_order": 1},
                        {"code": "CCPA.5.1b", "title": "Security measures are appropriate to the data sensitivity", "sort_order": 2},
                    ],
                },
                {
                    "code": "CCPA.5.2",
                    "title": "Risk Assessments for High-Risk Processing",
                    "description": "Businesses whose processing of consumers' personal information presents significant risk to consumers' privacy or security shall perform regular cybersecurity audits and risk assessments.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CCPA.5.2a", "title": "Risk assessments are conducted for high-risk processing", "sort_order": 1},
                        {"code": "CCPA.5.2b", "title": "Cybersecurity audits are performed regularly", "sort_order": 2},
                    ],
                },
                {
                    "code": "CCPA.5.3",
                    "title": "Breach Notification",
                    "description": "Businesses experiencing a data breach involving personal information shall provide notification to affected consumers as required by California's data breach notification law (Cal. Civ. Code 1798.82).",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CCPA.5.3a", "title": "Breach notification procedures are established", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CCPA.6",
            "name": "Service Providers and Contractors",
            "description": "Requirements governing the relationship between businesses and their service providers and contractors, including contractual obligations and restrictions on use of personal information.",
            "sort_order": 6,
            "requirements": [
                {
                    "code": "CCPA.6.1",
                    "title": "Service Provider Agreements",
                    "description": "Businesses must enter into written contracts with service providers that prohibit the service provider from selling or sharing the personal information, retaining, using, or disclosing it for any purpose other than performing the services.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CCPA.6.1a", "title": "Service provider contracts include CCPA-required restrictions", "sort_order": 1},
                        {"code": "CCPA.6.1b", "title": "Service provider compliance is monitored", "sort_order": 2},
                    ],
                },
                {
                    "code": "CCPA.6.2",
                    "title": "Contractor Agreements",
                    "description": "Businesses must enter into written contracts with contractors that include CCPA/CPRA-required clauses, including certification that the contractor understands and will comply with the restrictions.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CCPA.6.2a", "title": "Contractor agreements include CCPA-required provisions", "sort_order": 1},
                    ],
                },
                {
                    "code": "CCPA.6.3",
                    "title": "Sub-Service Provider Management",
                    "description": "Service providers and contractors engaging sub-service providers must notify the business and ensure that subcontractors are contractually bound by the same restrictions.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CCPA.6.3a", "title": "Sub-service provider engagements are disclosed and contractually bound", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CCPA.7",
            "name": "Minors",
            "description": "Special protections for the personal information of minors under 16 years of age, including opt-in consent requirements for the sale or sharing of their data.",
            "sort_order": 7,
            "requirements": [
                {
                    "code": "CCPA.7.1",
                    "title": "Minors Under 16 — Opt-In Required",
                    "description": "Businesses shall not sell or share the personal information of consumers under 16 years of age unless the consumer has affirmatively authorized the sale or sharing (opt-in consent for ages 13-16, parental consent for under 13).",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CCPA.7.1a", "title": "Opt-in consent is obtained before selling minors' data", "sort_order": 1},
                        {"code": "CCPA.7.1b", "title": "Age verification mechanisms are implemented where applicable", "sort_order": 2},
                    ],
                },
                {
                    "code": "CCPA.7.2",
                    "title": "Parental Consent for Under 13",
                    "description": "For consumers under 13 years of age, a parent or guardian must affirmatively authorize the sale or sharing of the minor's personal information.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CCPA.7.2a", "title": "Parental consent mechanisms are implemented for under-13 data", "sort_order": 1},
                    ],
                },
                {
                    "code": "CCPA.7.3",
                    "title": "Enhanced Penalties for Minors",
                    "description": "Businesses that willfully disregard the opt-in requirements for minors' data may be subject to treble penalties under the CCPA enforcement provisions.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CCPA.7.3a", "title": "Compliance with minors' data requirements is regularly audited", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CCPA.8",
            "name": "Enforcement and Compliance",
            "description": "Enforcement mechanisms, penalties, private right of action for data breaches, and organizational compliance program requirements under the CCPA/CPRA.",
            "sort_order": 8,
            "requirements": [
                {
                    "code": "CCPA.8.1",
                    "title": "Consumer Request Verification",
                    "description": "Businesses must establish methods for verifying the identity of consumers making requests to exercise their rights, using a degree of verification proportional to the sensitivity of the personal information involved.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CCPA.8.1a", "title": "Consumer identity verification procedures are established", "sort_order": 1},
                    ],
                },
                {
                    "code": "CCPA.8.2",
                    "title": "Non-Discrimination",
                    "description": "Businesses shall not discriminate against consumers who exercise their CCPA rights, including by denying goods or services, charging different prices, or providing a different level of service.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CCPA.8.2a", "title": "Non-discrimination policies are enforced for privacy rights", "sort_order": 1},
                    ],
                },
                {
                    "code": "CCPA.8.3",
                    "title": "Record Keeping",
                    "description": "Businesses shall maintain records of consumer requests and how the business responded to those requests for at least 24 months to demonstrate compliance.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CCPA.8.3a", "title": "Consumer request records are retained for 24 months", "sort_order": 1},
                    ],
                },
                {
                    "code": "CCPA.8.4",
                    "title": "Private Right of Action — Data Breaches",
                    "description": "Consumers whose nonencrypted and nonredacted personal information is subject to unauthorized access and exfiltration, theft, or disclosure as a result of the business's failure to implement and maintain reasonable security may institute a civil action.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CCPA.8.4a", "title": "Security controls are sufficient to defend against private action claims", "sort_order": 1},
                    ],
                },
            ],
        },
    ],
}


async def seed_ccpa_framework(db):
    """Seed the CCPA/CPRA framework."""
    from sqlalchemy import select
    from app.models.framework import Framework
    from app.models.framework_domain import FrameworkDomain
    from app.models.framework_requirement import FrameworkRequirement
    from app.models.control_objective import ControlObjective

    # Check if already seeded
    existing = await db.execute(
        select(Framework).where(Framework.name == CCPA_FRAMEWORK["name"])
    )
    if existing.scalar_one_or_none():
        print("  -> CCPA/CPRA framework already seeded, skipping.")
        return

    fw_data = CCPA_FRAMEWORK
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
    print(f"  Seeded CCPA/CPRA: {req_count} requirements, {obj_count} objectives.")
    return framework
