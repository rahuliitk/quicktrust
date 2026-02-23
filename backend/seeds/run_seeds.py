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
        print("\n[1/6] Seeding SOC 2 Framework...")
        from seeds.soc2_framework import seed_soc2_framework
        framework = await seed_soc2_framework(db)

        # 2. Seed ISO 27001 Framework
        print("\n[2/6] Seeding ISO 27001 Framework...")
        from seeds.iso27001_framework import seed_iso27001_framework
        await seed_iso27001_framework(db)

        # 3. Seed HIPAA Security Rule Framework
        print("\n[3/6] Seeding HIPAA Security Rule Framework...")
        from seeds.hipaa_framework import seed_hipaa_framework
        await seed_hipaa_framework(db)

        # 4. Seed Control Templates
        print("\n[4/6] Seeding Control Templates...")
        from seeds.control_templates import seed_control_templates
        await seed_control_templates(db, framework)

        # 5. Seed Evidence Templates
        print("\n[5/6] Seeding Evidence Templates...")
        from seeds.evidence_templates import seed_evidence_templates
        await seed_evidence_templates(db)

        # 6. Seed Policy Templates
        print("\n[6/6] Seeding Policy Templates...")
        from seeds.policy_templates import seed_policy_templates
        await seed_policy_templates(db)

        print("\n" + "=" * 50)
        print("Seeding complete!")
        print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
