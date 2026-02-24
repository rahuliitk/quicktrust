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
        print("\n[1/20] Seeding SOC 2 Framework...")
        from seeds.soc2_framework import seed_soc2_framework
        framework = await seed_soc2_framework(db)

        # 2. Seed ISO 27001 Framework
        print("\n[2/20] Seeding ISO 27001 Framework...")
        from seeds.iso27001_framework import seed_iso27001_framework
        await seed_iso27001_framework(db)

        # 3. Seed HIPAA Security Rule Framework
        print("\n[3/20] Seeding HIPAA Security Rule Framework...")
        from seeds.hipaa_framework import seed_hipaa_framework
        await seed_hipaa_framework(db)

        # 4. Seed GDPR Framework
        print("\n[4/20] Seeding GDPR Framework...")
        from seeds.gdpr_framework import seed_gdpr_framework
        await seed_gdpr_framework(db)

        # 5. Seed PCI DSS Framework
        print("\n[5/20] Seeding PCI DSS v4.0 Framework...")
        from seeds.pci_dss_framework import seed_pci_dss_framework
        await seed_pci_dss_framework(db)

        # 6. Seed NIST CSF Framework
        print("\n[6/20] Seeding NIST CSF 2.0 Framework...")
        from seeds.nist_csf_framework import seed_nist_csf_framework
        await seed_nist_csf_framework(db)

        # 7. Seed Control Templates
        print("\n[7/20] Seeding Control Templates...")
        from seeds.control_templates import seed_control_templates
        await seed_control_templates(db, framework)

        # 8. Seed Extended Control Templates
        print("\n[8/20] Seeding Extended Control Templates...")
        from seeds.extended_control_templates import seed_extended_control_templates
        await seed_extended_control_templates(db)

        # 9. Seed Evidence Templates
        print("\n[9/20] Seeding Evidence Templates...")
        from seeds.evidence_templates import seed_evidence_templates
        await seed_evidence_templates(db)

        # 10. Seed Extended Evidence Templates
        print("\n[10/20] Seeding Extended Evidence Templates...")
        from seeds.extended_evidence_templates import seed_extended_evidence_templates
        await seed_extended_evidence_templates(db)

        # 11. Seed Policy Templates
        print("\n[11/20] Seeding Policy Templates...")
        from seeds.policy_templates import seed_policy_templates
        await seed_policy_templates(db)

        # 12. Seed ISO 27701 Framework
        print("\n[12/20] Seeding ISO 27701 Privacy Information Management Framework...")
        from seeds.seed_iso27701 import seed_iso27701_framework
        await seed_iso27701_framework(db)

        # 13. Seed NIST 800-53 Framework
        print("\n[13/20] Seeding NIST 800-53 Rev 5 Framework...")
        from seeds.seed_nist_800_53 import seed_nist_800_53_framework
        await seed_nist_800_53_framework(db)

        # 14. Seed NIST 800-171 Framework
        print("\n[14/20] Seeding NIST 800-171 Rev 3 Framework...")
        from seeds.seed_nist_800_171 import seed_nist_800_171_framework
        await seed_nist_800_171_framework(db)

        # 15. Seed FedRAMP Framework
        print("\n[15/20] Seeding FedRAMP Framework...")
        from seeds.seed_fedramp import seed_fedramp_framework
        await seed_fedramp_framework(db)

        # 16. Seed CCPA/CPRA Framework
        print("\n[16/20] Seeding CCPA/CPRA Framework...")
        from seeds.seed_ccpa import seed_ccpa_framework
        await seed_ccpa_framework(db)

        # 17. Seed SOX IT Controls Framework
        print("\n[17/20] Seeding SOX IT Controls Framework...")
        from seeds.seed_sox import seed_sox_framework
        await seed_sox_framework(db)

        # 18. Seed CIS Controls v8 Framework
        print("\n[18/20] Seeding CIS Controls v8 Framework...")
        from seeds.seed_cis import seed_cis_framework
        await seed_cis_framework(db)

        # 19. Seed CSA STAR (CCM) Framework
        print("\n[19/20] Seeding CSA STAR (CCM) v4 Framework...")
        from seeds.seed_csa_star import seed_csa_star_framework
        await seed_csa_star_framework(db)

        # 20. Seed CMMC 2.0 Framework
        print("\n[20/20] Seeding CMMC 2.0 Framework...")
        from seeds.seed_cmmc import seed_cmmc_framework
        await seed_cmmc_framework(db)

        print("\n" + "=" * 50)
        print("Seeding complete!")
        print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
