"""Seed runner — orchestrates all seed scripts."""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all models at module level so Base.metadata knows about them
import app.models  # noqa: F401


async def main():
    from app.core.database import async_session, engine, Base

    # Create tables if they don't exist (for dev convenience)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        print("=" * 50)
        print("QuickTrust Seed Runner")
        print("=" * 50)

        # 1. Seed SOC 2 Framework
        print("\n[1/11] Seeding SOC 2 Framework...")
        from seeds.soc2_framework import seed_soc2_framework
        framework = await seed_soc2_framework(db)

        # 2. Seed ISO 27001 Framework
        print("\n[2/11] Seeding ISO 27001 Framework...")
        from seeds.iso27001_framework import seed_iso27001_framework
        await seed_iso27001_framework(db)

        # 3. Seed HIPAA Security Rule Framework
        print("\n[3/11] Seeding HIPAA Security Rule Framework...")
        from seeds.hipaa_framework import seed_hipaa_framework
        await seed_hipaa_framework(db)

        # 4. Seed GDPR Framework
        print("\n[4/11] Seeding GDPR Framework...")
        from seeds.gdpr_framework import seed_gdpr_framework
        await seed_gdpr_framework(db)

        # 5. Seed PCI DSS Framework
        print("\n[5/11] Seeding PCI DSS v4.0 Framework...")
        from seeds.pci_dss_framework import seed_pci_dss_framework
        await seed_pci_dss_framework(db)

        # 6. Seed NIST CSF Framework
        print("\n[6/11] Seeding NIST CSF 2.0 Framework...")
        from seeds.nist_csf_framework import seed_nist_csf_framework
        await seed_nist_csf_framework(db)

        # 7. Seed Control Templates
        print("\n[7/11] Seeding Control Templates...")
        from seeds.control_templates import seed_control_templates
        await seed_control_templates(db, framework)

        # 8. Seed Extended Control Templates
        print("\n[8/11] Seeding Extended Control Templates...")
        from seeds.extended_control_templates import seed_extended_control_templates
        await seed_extended_control_templates(db)

        # 9. Seed Evidence Templates
        print("\n[9/11] Seeding Evidence Templates...")
        from seeds.evidence_templates import seed_evidence_templates
        await seed_evidence_templates(db)

        # 10. Seed Extended Evidence Templates
        print("\n[10/11] Seeding Extended Evidence Templates...")
        from seeds.extended_evidence_templates import seed_extended_evidence_templates
        await seed_extended_evidence_templates(db)

        # 11. Seed Policy Templates
        print("\n[11/11] Seeding Policy Templates...")
        from seeds.policy_templates import seed_policy_templates
        await seed_policy_templates(db)

        print("\n" + "=" * 50)
        print("Seeding complete!")
        print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
