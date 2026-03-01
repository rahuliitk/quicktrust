-- ============================================================================
-- QuickTrust GRC Platform - Sample Data for Testing
-- ============================================================================
-- This script populates all core tables with realistic test data.
-- Compatible with PostgreSQL 16+. Run after Alembic migrations.
--
-- Usage:
--   psql -U quicktrust -d quicktrust -f samplesql.sql
-- ============================================================================

-- Enable UUID extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

BEGIN;

-- ============================================================================
-- 1. ORGANIZATIONS
-- ============================================================================
INSERT INTO organizations (id, name, slug, industry, company_size, cloud_providers, tech_stack, settings, created_at, updated_at)
VALUES
  ('11111111-1111-1111-1111-111111111111', 'Acme Corp', 'acme-corp', 'SaaS', '51-200', '["aws","gcp"]', '["python","react","postgresql"]', '{}', NOW(), NOW()),
  ('22222222-2222-2222-2222-222222222222', 'HealthFirst Inc', 'healthfirst', 'Healthcare', '201-500', '["aws"]', '["java","angular","mysql"]', '{}', NOW(), NOW()),
  ('33333333-3333-3333-3333-333333333333', 'FinSecure Ltd', 'finsecure', 'Fintech', '11-50', '["aws","azure"]', '["node","react","mongodb"]', '{}', NOW(), NOW());

-- ============================================================================
-- 2. USERS
-- ============================================================================
-- Acme Corp Users
INSERT INTO users (id, org_id, keycloak_id, email, full_name, role, department, is_active, created_at, updated_at)
VALUES
  ('aaaa0001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'kc-admin-001', 'admin@acme.com', 'Alice Admin', 'admin', 'IT', true, NOW(), NOW()),
  ('aaaa0001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'kc-cm-001', 'compliance@acme.com', 'Charlie Compliance', 'compliance_manager', 'Compliance', true, NOW(), NOW()),
  ('aaaa0001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', 'kc-co-001', 'devops@acme.com', 'Dave DevOps', 'control_owner', 'Engineering', true, NOW(), NOW()),
  ('aaaa0001-0001-0001-0001-000000000004', '11111111-1111-1111-1111-111111111111', 'kc-emp-001', 'employee@acme.com', 'Eve Employee', 'employee', 'Engineering', true, NOW(), NOW()),
  ('aaaa0001-0001-0001-0001-000000000005', '11111111-1111-1111-1111-111111111111', 'kc-exec-001', 'ciso@acme.com', 'Frank CISO', 'executive', 'Leadership', true, NOW(), NOW()),
  ('aaaa0001-0001-0001-0001-000000000006', '11111111-1111-1111-1111-111111111111', 'kc-audint-001', 'internal.audit@acme.com', 'Grace Auditor', 'auditor_internal', 'Audit', true, NOW(), NOW());

-- HealthFirst Users
INSERT INTO users (id, org_id, keycloak_id, email, full_name, role, department, is_active, created_at, updated_at)
VALUES
  ('bbbb0001-0001-0001-0001-000000000001', '22222222-2222-2222-2222-222222222222', 'kc-admin-002', 'admin@healthfirst.com', 'Hannah Admin', 'admin', 'IT', true, NOW(), NOW()),
  ('bbbb0001-0001-0001-0001-000000000002', '22222222-2222-2222-2222-222222222222', 'kc-cm-002', 'hipaa@healthfirst.com', 'Ian HIPAA', 'compliance_manager', 'Compliance', true, NOW(), NOW());

-- FinSecure Users
INSERT INTO users (id, org_id, keycloak_id, email, full_name, role, department, is_active, created_at, updated_at)
VALUES
  ('cccc0001-0001-0001-0001-000000000001', '33333333-3333-3333-3333-333333333333', 'kc-admin-003', 'admin@finsecure.com', 'Jack Admin', 'admin', 'IT', true, NOW(), NOW()),
  ('cccc0001-0001-0001-0001-000000000002', '33333333-3333-3333-3333-333333333333', 'kc-cm-003', 'pci@finsecure.com', 'Karen PCI', 'compliance_manager', 'Security', true, NOW(), NOW());

-- ============================================================================
-- 3. FRAMEWORKS
-- ============================================================================
INSERT INTO frameworks (id, name, version, category, description, is_active, created_at, updated_at)
VALUES
  ('ff000001-0001-0001-0001-000000000001', 'SOC 2 Type II', '2017', 'security', 'Service Organization Control 2 - Trust Services Criteria for Security, Availability, Processing Integrity, Confidentiality, and Privacy', true, NOW(), NOW()),
  ('ff000001-0001-0001-0001-000000000002', 'ISO 27001', '2022', 'security', 'Information Security Management System (ISMS) international standard', true, NOW(), NOW()),
  ('ff000001-0001-0001-0001-000000000003', 'HIPAA', '2013', 'healthcare', 'Health Insurance Portability and Accountability Act - Security and Privacy Rules', true, NOW(), NOW()),
  ('ff000001-0001-0001-0001-000000000004', 'PCI DSS', '4.0', 'payment', 'Payment Card Industry Data Security Standard', true, NOW(), NOW()),
  ('ff000001-0001-0001-0001-000000000005', 'GDPR', '2018', 'privacy', 'General Data Protection Regulation - EU data privacy regulation', true, NOW(), NOW()),
  ('ff000001-0001-0001-0001-000000000006', 'NIST CSF', '2.0', 'security', 'NIST Cybersecurity Framework for improving critical infrastructure security', true, NOW(), NOW());

-- ============================================================================
-- 4. FRAMEWORK DOMAINS
-- ============================================================================
-- SOC 2 Domains
INSERT INTO framework_domains (id, framework_id, code, name, description, sort_order, created_at, updated_at)
VALUES
  ('fd000001-0001-0001-0001-000000000001', 'ff000001-0001-0001-0001-000000000001', 'CC1', 'Control Environment', 'COSO Principle: The entity demonstrates commitment to integrity and ethical values', 1, NOW(), NOW()),
  ('fd000001-0001-0001-0001-000000000002', 'ff000001-0001-0001-0001-000000000001', 'CC2', 'Communication and Information', 'COSO Principle: The entity uses relevant information to support functioning of controls', 2, NOW(), NOW()),
  ('fd000001-0001-0001-0001-000000000003', 'ff000001-0001-0001-0001-000000000001', 'CC3', 'Risk Assessment', 'COSO Principle: The entity specifies objectives and identifies/analyzes risks', 3, NOW(), NOW()),
  ('fd000001-0001-0001-0001-000000000004', 'ff000001-0001-0001-0001-000000000001', 'CC6', 'Logical and Physical Access Controls', 'Restricts logical and physical access to assets', 4, NOW(), NOW()),
  ('fd000001-0001-0001-0001-000000000005', 'ff000001-0001-0001-0001-000000000001', 'CC7', 'System Operations', 'Detects and monitors events that could affect the entity', 5, NOW(), NOW()),
  ('fd000001-0001-0001-0001-000000000006', 'ff000001-0001-0001-0001-000000000001', 'CC8', 'Change Management', 'Controls changes to infrastructure and software', 6, NOW(), NOW()),
  ('fd000001-0001-0001-0001-000000000007', 'ff000001-0001-0001-0001-000000000001', 'CC9', 'Risk Mitigation', 'Identifies, selects, and develops risk mitigation activities', 7, NOW(), NOW());

-- ISO 27001 Domains
INSERT INTO framework_domains (id, framework_id, code, name, description, sort_order, created_at, updated_at)
VALUES
  ('fd000002-0001-0001-0001-000000000001', 'ff000001-0001-0001-0001-000000000002', 'A.5', 'Information Security Policies', 'Management direction for information security', 1, NOW(), NOW()),
  ('fd000002-0001-0001-0001-000000000002', 'ff000001-0001-0001-0001-000000000002', 'A.6', 'Organization of Information Security', 'Internal organization and mobile devices', 2, NOW(), NOW()),
  ('fd000002-0001-0001-0001-000000000003', 'ff000001-0001-0001-0001-000000000002', 'A.8', 'Asset Management', 'Responsibility and classification of assets', 3, NOW(), NOW()),
  ('fd000002-0001-0001-0001-000000000004', 'ff000001-0001-0001-0001-000000000002', 'A.9', 'Access Control', 'Business requirements and user access management', 4, NOW(), NOW());

-- HIPAA Domains
INSERT INTO framework_domains (id, framework_id, code, name, description, sort_order, created_at, updated_at)
VALUES
  ('fd000003-0001-0001-0001-000000000001', 'ff000001-0001-0001-0001-000000000003', '164.308', 'Administrative Safeguards', 'Administrative actions and policies to manage security measures', 1, NOW(), NOW()),
  ('fd000003-0001-0001-0001-000000000002', 'ff000001-0001-0001-0001-000000000003', '164.310', 'Physical Safeguards', 'Physical measures and policies to protect electronic information systems', 2, NOW(), NOW()),
  ('fd000003-0001-0001-0001-000000000003', 'ff000001-0001-0001-0001-000000000003', '164.312', 'Technical Safeguards', 'Technology and policies for protecting ePHI', 3, NOW(), NOW());

-- ============================================================================
-- 5. FRAMEWORK REQUIREMENTS
-- ============================================================================
-- SOC 2 CC6 Requirements
INSERT INTO framework_requirements (id, domain_id, code, title, description, sort_order, created_at, updated_at)
VALUES
  ('fr000001-0001-0001-0001-000000000001', 'fd000001-0001-0001-0001-000000000004', 'CC6.1', 'Logical Access Security', 'The entity implements logical access security software, infrastructure, and architectures over protected information assets', 1, NOW(), NOW()),
  ('fr000001-0001-0001-0001-000000000002', 'fd000001-0001-0001-0001-000000000004', 'CC6.2', 'User Authentication', 'Prior to issuing system credentials and granting access, the entity registers and authorizes new users', 2, NOW(), NOW()),
  ('fr000001-0001-0001-0001-000000000003', 'fd000001-0001-0001-0001-000000000004', 'CC6.3', 'Role-Based Access', 'The entity authorizes, modifies, or removes access to data based on roles and responsibilities', 3, NOW(), NOW()),
  ('fr000001-0001-0001-0001-000000000004', 'fd000001-0001-0001-0001-000000000005', 'CC7.1', 'Intrusion Detection', 'The entity uses detection and monitoring procedures to identify changes to configurations and new vulnerabilities', 4, NOW(), NOW()),
  ('fr000001-0001-0001-0001-000000000005', 'fd000001-0001-0001-0001-000000000005', 'CC7.2', 'Anomaly Monitoring', 'The entity monitors system components for anomalies indicative of malicious acts', 5, NOW(), NOW()),
  ('fr000001-0001-0001-0001-000000000006', 'fd000001-0001-0001-0001-000000000006', 'CC8.1', 'Change Authorization', 'The entity authorizes, designs, develops, configures, documents, tests, approves, and implements changes', 6, NOW(), NOW());

-- ISO 27001 A.9 Requirements
INSERT INTO framework_requirements (id, domain_id, code, title, description, sort_order, created_at, updated_at)
VALUES
  ('fr000002-0001-0001-0001-000000000001', 'fd000002-0001-0001-0001-000000000004', 'A.9.1.1', 'Access Control Policy', 'An access control policy shall be established, documented, and reviewed', 1, NOW(), NOW()),
  ('fr000002-0001-0001-0001-000000000002', 'fd000002-0001-0001-0001-000000000004', 'A.9.2.1', 'User Registration', 'A formal user registration and de-registration process shall be implemented', 2, NOW(), NOW()),
  ('fr000002-0001-0001-0001-000000000003', 'fd000002-0001-0001-0001-000000000004', 'A.9.4.1', 'Information Access Restriction', 'Access to information and application system functions shall be restricted', 3, NOW(), NOW());

-- HIPAA Requirements
INSERT INTO framework_requirements (id, domain_id, code, title, description, sort_order, created_at, updated_at)
VALUES
  ('fr000003-0001-0001-0001-000000000001', 'fd000003-0001-0001-0001-000000000001', '164.308(a)(1)', 'Security Management Process', 'Implement policies and procedures to prevent, detect, contain, and correct security violations', 1, NOW(), NOW()),
  ('fr000003-0001-0001-0001-000000000002', 'fd000003-0001-0001-0001-000000000001', '164.308(a)(3)', 'Workforce Security', 'Implement policies and procedures to ensure workforce members have appropriate ePHI access', 2, NOW(), NOW()),
  ('fr000003-0001-0001-0001-000000000003', 'fd000003-0001-0001-0001-000000000003', '164.312(a)(1)', 'Access Control', 'Implement technical policies and procedures for electronic information systems with ePHI', 3, NOW(), NOW()),
  ('fr000003-0001-0001-0001-000000000004', 'fd000003-0001-0001-0001-000000000003', '164.312(e)(1)', 'Transmission Security', 'Implement technical security measures to guard against unauthorized access to ePHI being transmitted', 4, NOW(), NOW());

-- ============================================================================
-- 6. AGENT RUNS
-- ============================================================================
INSERT INTO agent_runs (id, org_id, agent_type, trigger, status, input_data, output_data, error_message, started_at, completed_at, tokens_used, created_at, updated_at)
VALUES
  ('ar000001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'controls_generation', 'onboarding', 'completed', '{"framework_ids": ["ff000001-0001-0001-0001-000000000001"]}', '{"controls_created": 12}', NULL, NOW() - INTERVAL '2 hours', NOW() - INTERVAL '1 hour', 4500, NOW(), NOW()),
  ('ar000001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'policy_generation', 'onboarding', 'completed', '{"framework_ids": ["ff000001-0001-0001-0001-000000000001"]}', '{"policies_created": 8}', NULL, NOW() - INTERVAL '1 hour', NOW() - INTERVAL '30 minutes', 6200, NOW(), NOW()),
  ('ar000001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', 'evidence_generation', 'manual', 'completed', '{"control_ids": ["ctrl0001-0001-0001-0001-000000000001"]}', '{"evidence_created": 5}', NULL, NOW() - INTERVAL '30 minutes', NOW() - INTERVAL '15 minutes', 0, NOW(), NOW()),
  ('ar000001-0001-0001-0001-000000000004', '11111111-1111-1111-1111-111111111111', 'risk_assessment', 'manual', 'running', '{"scope": "full_org"}', '{}', NULL, NOW() - INTERVAL '5 minutes', NULL, NULL, NOW(), NOW()),
  ('ar000001-0001-0001-0001-000000000005', '22222222-2222-2222-2222-222222222222', 'controls_generation', 'onboarding', 'failed', '{"framework_ids": ["ff000001-0001-0001-0001-000000000003"]}', '{}', 'LLM API key not configured', NOW() - INTERVAL '3 hours', NOW() - INTERVAL '3 hours', 0, NOW(), NOW());

-- ============================================================================
-- 7. CONTROLS (Acme Corp - SOC 2 mapped)
-- ============================================================================
INSERT INTO controls (id, org_id, template_id, title, description, implementation_details, owner_id, status, effectiveness, automation_level, test_procedure, last_test_date, last_test_result, agent_run_id, created_at, updated_at)
VALUES
  ('ctrl0001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', NULL, 'Multi-Factor Authentication Enforcement', 'All users must authenticate using MFA for access to production systems and admin consoles', 'Enforced via Okta with TOTP and WebAuthn as secondary factors. Conditional access policies require MFA for all admin and production access.', 'aaaa0001-0001-0001-0001-000000000003', 'implemented', 'effective', 'automated', 'Verify MFA enrollment rate via Okta API and test login flow without MFA is blocked', NOW() - INTERVAL '7 days', 'pass', 'ar000001-0001-0001-0001-000000000001', NOW(), NOW()),

  ('ctrl0001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', NULL, 'Encryption at Rest', 'All data at rest must be encrypted using AES-256 or equivalent', 'AWS RDS instances use AES-256 encryption. S3 buckets configured with SSE-S3. EBS volumes encrypted by default.', 'aaaa0001-0001-0001-0001-000000000003', 'implemented', 'effective', 'automated', 'Run AWS Config rule check for unencrypted resources', NOW() - INTERVAL '14 days', 'pass', 'ar000001-0001-0001-0001-000000000001', NOW(), NOW()),

  ('ctrl0001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', NULL, 'Encryption in Transit', 'All data transmitted over networks must use TLS 1.2 or higher', 'ALB configured with TLS 1.2 minimum. HSTS headers enforced. Internal service mesh uses mutual TLS.', 'aaaa0001-0001-0001-0001-000000000003', 'implemented', 'effective', 'automated', 'SSL Labs scan and certificate expiry monitoring', NOW() - INTERVAL '3 days', 'pass', 'ar000001-0001-0001-0001-000000000001', NOW(), NOW()),

  ('ctrl0001-0001-0001-0001-000000000004', '11111111-1111-1111-1111-111111111111', NULL, 'Access Reviews - Quarterly', 'User access to critical systems is reviewed and recertified quarterly', 'Quarterly campaigns created in QuickTrust. Department managers review access for their reports. IT reviews admin/privileged access.', 'aaaa0001-0001-0001-0001-000000000002', 'implemented', 'partially_effective', 'semi_automated', 'Verify Q4 campaign completed with 100% coverage', NOW() - INTERVAL '30 days', 'partial', 'ar000001-0001-0001-0001-000000000001', NOW(), NOW()),

  ('ctrl0001-0001-0001-0001-000000000005', '11111111-1111-1111-1111-111111111111', NULL, 'Vulnerability Scanning', 'Weekly automated vulnerability scans on all production infrastructure', 'Prowler runs weekly scans. Dependabot enabled on all GitHub repos. Critical vulnerabilities patched within 72 hours.', 'aaaa0001-0001-0001-0001-000000000003', 'implemented', 'effective', 'automated', 'Verify scan execution logs and remediation SLA compliance', NOW() - INTERVAL '5 days', 'pass', NULL, NOW(), NOW()),

  ('ctrl0001-0001-0001-0001-000000000006', '11111111-1111-1111-1111-111111111111', NULL, 'Change Management Process', 'All production changes follow an approval and review workflow', 'GitHub branch protection requires PR reviews. CI/CD pipeline enforces test passage. Deploy approval via GitHub Environments.', 'aaaa0001-0001-0001-0001-000000000003', 'implemented', 'effective', 'automated', 'Audit GitHub PR merge history for unapproved merges', NOW() - INTERVAL '10 days', 'pass', NULL, NOW(), NOW()),

  ('ctrl0001-0001-0001-0001-000000000007', '11111111-1111-1111-1111-111111111111', NULL, 'Incident Response Plan', 'Documented incident response plan tested annually via tabletop exercises', 'IRP documented in Confluence. Annual tabletop with engineering and leadership. Slack channel #incident-response for real-time coordination.', 'aaaa0001-0001-0001-0001-000000000002', 'implemented', 'effective', 'manual', 'Review IRP document currency and tabletop exercise records', NOW() - INTERVAL '60 days', 'pass', NULL, NOW(), NOW()),

  ('ctrl0001-0001-0001-0001-000000000008', '11111111-1111-1111-1111-111111111111', NULL, 'Security Awareness Training', 'All employees complete annual security awareness training', 'Training program via QuickTrust. Covers phishing, password hygiene, data handling, incident reporting. Mandatory for all roles.', 'aaaa0001-0001-0001-0001-000000000002', 'implemented', 'partially_effective', 'manual', 'Check training completion rates across all departments', NOW() - INTERVAL '45 days', 'partial', NULL, NOW(), NOW()),

  ('ctrl0001-0001-0001-0001-000000000009', '11111111-1111-1111-1111-111111111111', NULL, 'Backup and Recovery', 'Automated daily backups with tested recovery procedures', 'AWS RDS automated backups (35-day retention). S3 cross-region replication. Monthly restore tests documented.', 'aaaa0001-0001-0001-0001-000000000003', 'in_progress', NULL, 'automated', 'Perform test restore and verify data integrity', NULL, NULL, NULL, NOW(), NOW()),

  ('ctrl0001-0001-0001-0001-000000000010', '11111111-1111-1111-1111-111111111111', NULL, 'Logging and Monitoring', 'Centralized logging with alerting for security events', 'CloudTrail enabled across all regions. CloudWatch Logs for application logs. PagerDuty for critical alerts.', 'aaaa0001-0001-0001-0001-000000000003', 'draft', NULL, 'semi_automated', 'Verify log retention policy and alert rule coverage', NULL, NULL, NULL, NOW(), NOW()),

  ('ctrl0001-0001-0001-0001-000000000011', '11111111-1111-1111-1111-111111111111', NULL, 'Vendor Risk Assessment', 'All critical vendors assessed annually for security posture', 'Vendor risk questionnaire via QuickTrust. Critical vendors reassessed annually. Vendor contracts include security requirements.', 'aaaa0001-0001-0001-0001-000000000002', 'not_implemented', NULL, 'manual', 'Review vendor assessment completion status', NULL, NULL, NULL, NOW(), NOW()),

  ('ctrl0001-0001-0001-0001-000000000012', '11111111-1111-1111-1111-111111111111', NULL, 'Data Classification', 'All data assets classified by sensitivity level', 'Classification scheme: Public, Internal, Confidential, Restricted. Data inventory maintained in wiki.', 'aaaa0001-0001-0001-0001-000000000002', 'draft', NULL, 'manual', 'Review data inventory completeness', NULL, NULL, NULL, NOW(), NOW());

-- HealthFirst Controls (HIPAA)
INSERT INTO controls (id, org_id, title, description, status, effectiveness, automation_level, owner_id, created_at, updated_at)
VALUES
  ('ctrl0002-0001-0001-0001-000000000001', '22222222-2222-2222-2222-222222222222', 'PHI Access Logging', 'All access to Protected Health Information is logged and auditable', 'implemented', 'effective', 'automated', 'bbbb0001-0001-0001-0001-000000000002', NOW(), NOW()),
  ('ctrl0002-0001-0001-0001-000000000002', '22222222-2222-2222-2222-222222222222', 'ePHI Encryption', 'All electronic Protected Health Information encrypted at rest and in transit', 'implemented', 'effective', 'automated', 'bbbb0001-0001-0001-0001-000000000002', NOW(), NOW()),
  ('ctrl0002-0001-0001-0001-000000000003', '22222222-2222-2222-2222-222222222222', 'BAA Management', 'Business Associate Agreements executed with all vendors handling PHI', 'in_progress', NULL, 'manual', 'bbbb0001-0001-0001-0001-000000000002', NOW(), NOW());

-- ============================================================================
-- 8. CONTROL FRAMEWORK MAPPINGS
-- ============================================================================
INSERT INTO control_framework_mappings (id, control_id, requirement_id, created_at, updated_at)
VALUES
  ('cfm00001-0001-0001-0001-000000000001', 'ctrl0001-0001-0001-0001-000000000001', 'fr000001-0001-0001-0001-000000000002', NOW(), NOW()),
  ('cfm00001-0001-0001-0001-000000000002', 'ctrl0001-0001-0001-0001-000000000002', 'fr000001-0001-0001-0001-000000000001', NOW(), NOW()),
  ('cfm00001-0001-0001-0001-000000000003', 'ctrl0001-0001-0001-0001-000000000003', 'fr000001-0001-0001-0001-000000000001', NOW(), NOW()),
  ('cfm00001-0001-0001-0001-000000000004', 'ctrl0001-0001-0001-0001-000000000004', 'fr000001-0001-0001-0001-000000000003', NOW(), NOW()),
  ('cfm00001-0001-0001-0001-000000000005', 'ctrl0001-0001-0001-0001-000000000005', 'fr000001-0001-0001-0001-000000000004', NOW(), NOW()),
  ('cfm00001-0001-0001-0001-000000000006', 'ctrl0001-0001-0001-0001-000000000006', 'fr000001-0001-0001-0001-000000000006', NOW(), NOW());

-- ============================================================================
-- 9. EVIDENCE
-- ============================================================================
INSERT INTO evidence (id, org_id, control_id, title, status, collected_at, expires_at, artifact_url, artifact_hash, file_url, file_name, data, collection_method, collector, created_at, updated_at)
VALUES
  ('ev000001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'ctrl0001-0001-0001-0001-000000000001', 'Okta MFA Enrollment Report', 'collected', NOW() - INTERVAL '2 days', NOW() + INTERVAL '28 days', NULL, 'sha256:a1b2c3d4e5f6...', NULL, NULL, '{"total_users": 148, "mfa_enrolled": 145, "enrollment_rate": 0.98}', 'automated', 'okta_mfa_enrollment', NOW(), NOW()),

  ('ev000001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'ctrl0001-0001-0001-0001-000000000001', 'AWS IAM MFA Report', 'collected', NOW() - INTERVAL '1 day', NOW() + INTERVAL '29 days', NULL, 'sha256:b2c3d4e5f6a7...', NULL, NULL, '{"iam_users": 12, "mfa_enabled": 12, "root_mfa": true}', 'automated', 'aws_iam_mfa', NOW(), NOW()),

  ('ev000001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', 'ctrl0001-0001-0001-0001-000000000002', 'AWS Encryption at Rest Check', 'collected', NOW() - INTERVAL '3 days', NOW() + INTERVAL '27 days', NULL, 'sha256:c3d4e5f6a7b8...', NULL, NULL, '{"rds_encrypted": true, "s3_default_encryption": true, "ebs_encrypted": true, "unencrypted_resources": 0}', 'automated', 'aws_encryption_check', NOW(), NOW()),

  ('ev000001-0001-0001-0001-000000000004', '11111111-1111-1111-1111-111111111111', 'ctrl0001-0001-0001-0001-000000000003', 'TLS Configuration Screenshot', 'collected', NOW() - INTERVAL '5 days', NOW() + INTERVAL '85 days', 's3://evidence/acme/tls-config-2026.png', 'sha256:d4e5f6a7b8c9...', '/evidence/tls-config-2026.png', 'tls-config-2026.png', '{}', 'manual', NULL, NOW(), NOW()),

  ('ev000001-0001-0001-0001-000000000005', '11111111-1111-1111-1111-111111111111', 'ctrl0001-0001-0001-0001-000000000005', 'GitHub Dependabot Alerts Summary', 'collected', NOW() - INTERVAL '1 day', NOW() + INTERVAL '6 days', NULL, 'sha256:e5f6a7b8c9d0...', NULL, NULL, '{"total_alerts": 3, "critical": 0, "high": 1, "medium": 2, "repos_scanned": 8}', 'automated', 'github_dependabot', NOW(), NOW()),

  ('ev000001-0001-0001-0001-000000000006', '11111111-1111-1111-1111-111111111111', 'ctrl0001-0001-0001-0001-000000000005', 'Prowler AWS Security Scan', 'collected', NOW() - INTERVAL '2 days', NOW() + INTERVAL '5 days', NULL, 'sha256:f6a7b8c9d0e1...', NULL, NULL, '{"total_checks": 245, "pass": 228, "fail": 12, "warning": 5, "pass_rate": 0.93}', 'automated', 'prowler_full_scan', NOW(), NOW()),

  ('ev000001-0001-0001-0001-000000000007', '11111111-1111-1111-1111-111111111111', 'ctrl0001-0001-0001-0001-000000000006', 'GitHub Branch Protection Config', 'collected', NOW() - INTERVAL '4 days', NOW() + INTERVAL '26 days', NULL, 'sha256:a7b8c9d0e1f2...', NULL, NULL, '{"repos_checked": 8, "protected": 8, "require_reviews": true, "require_ci": true}', 'automated', 'github_branch_protection', NOW(), NOW()),

  ('ev000001-0001-0001-0001-000000000008', '11111111-1111-1111-1111-111111111111', 'ctrl0001-0001-0001-0001-000000000006', 'AWS CloudTrail Status', 'collected', NOW() - INTERVAL '1 day', NOW() + INTERVAL '29 days', NULL, 'sha256:b8c9d0e1f2a3...', NULL, NULL, '{"trails": 2, "multi_region": true, "log_validation": true, "s3_logging": true}', 'automated', 'aws_cloudtrail', NOW(), NOW()),

  ('ev000001-0001-0001-0001-000000000009', '11111111-1111-1111-1111-111111111111', 'ctrl0001-0001-0001-0001-000000000007', 'Incident Response Plan Document', 'collected', NOW() - INTERVAL '60 days', NOW() + INTERVAL '305 days', 's3://evidence/acme/irp-v3.pdf', 'sha256:c9d0e1f2a3b4...', '/evidence/irp-v3.pdf', 'irp-v3.pdf', '{}', 'manual', NULL, NOW(), NOW()),

  ('ev000001-0001-0001-0001-000000000010', '11111111-1111-1111-1111-111111111111', 'ctrl0001-0001-0001-0001-000000000004', 'Q4 2025 Access Review Report', 'stale', NOW() - INTERVAL '95 days', NOW() - INTERVAL '5 days', NULL, NULL, NULL, NULL, '{"entries_reviewed": 120, "approved": 112, "revoked": 8}', 'manual', NULL, NOW(), NOW()),

  ('ev000001-0001-0001-0001-000000000011', '11111111-1111-1111-1111-111111111111', 'ctrl0001-0001-0001-0001-000000000009', 'Backup Configuration - Pending', 'pending', NULL, NULL, NULL, NULL, NULL, NULL, '{}', 'manual', NULL, NOW(), NOW());

-- ============================================================================
-- 10. POLICIES
-- ============================================================================
INSERT INTO policies (id, org_id, title, content, version, status, owner_id, approved_by_id, approved_at, published_at, next_review_date, framework_ids, control_ids, agent_run_id, created_at, updated_at)
VALUES
  ('pol00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'Information Security Policy', '## 1. Purpose\nThis policy establishes the information security framework for Acme Corp.\n\n## 2. Scope\nApplies to all employees, contractors, and third parties.\n\n## 3. Policy Statements\n- All systems must implement appropriate security controls.\n- Security incidents must be reported within 4 hours.\n- Annual risk assessments are mandatory.', '2.0', 'published', 'aaaa0001-0001-0001-0001-000000000002', 'aaaa0001-0001-0001-0001-000000000001', NOW() - INTERVAL '30 days', NOW() - INTERVAL '28 days', NOW() + INTERVAL '337 days', '["ff000001-0001-0001-0001-000000000001"]', '[]', 'ar000001-0001-0001-0001-000000000002', NOW(), NOW()),

  ('pol00001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'Access Control Policy', '## 1. Purpose\nDefines access control requirements for all Acme Corp systems.\n\n## 2. Access Principles\n- Least privilege access\n- Need-to-know basis\n- Segregation of duties\n\n## 3. Requirements\n- MFA required for all users\n- Quarterly access reviews\n- Immediate revocation upon termination', '1.0', 'published', 'aaaa0001-0001-0001-0001-000000000002', 'aaaa0001-0001-0001-0001-000000000001', NOW() - INTERVAL '25 days', NOW() - INTERVAL '24 days', NOW() + INTERVAL '341 days', '["ff000001-0001-0001-0001-000000000001"]', '["ctrl0001-0001-0001-0001-000000000001","ctrl0001-0001-0001-0001-000000000004"]', 'ar000001-0001-0001-0001-000000000002', NOW(), NOW()),

  ('pol00001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', 'Data Classification Policy', '## 1. Purpose\nEstablishes data classification levels and handling procedures.\n\n## 2. Classification Levels\n- **Public**: No restrictions\n- **Internal**: Restricted to employees\n- **Confidential**: Need-to-know with encryption\n- **Restricted**: Highest security, PII/PHI/PCI data', '1.0', 'published', 'aaaa0001-0001-0001-0001-000000000002', 'aaaa0001-0001-0001-0001-000000000001', NOW() - INTERVAL '20 days', NOW() - INTERVAL '19 days', NOW() + INTERVAL '346 days', '["ff000001-0001-0001-0001-000000000001"]', '["ctrl0001-0001-0001-0001-000000000012"]', NULL, NOW(), NOW()),

  ('pol00001-0001-0001-0001-000000000004', '11111111-1111-1111-1111-111111111111', 'Incident Response Policy', '## 1. Purpose\nDefines incident classification, response, and escalation procedures.\n\n## 2. Severity Levels\n- P1: Critical (30 min response)\n- P2: High (2 hour response)\n- P3: Medium (24 hour response)\n- P4: Low (72 hour response)', '1.0', 'approved', 'aaaa0001-0001-0001-0001-000000000002', 'aaaa0001-0001-0001-0001-000000000001', NOW() - INTERVAL '10 days', NULL, NOW() + INTERVAL '355 days', '["ff000001-0001-0001-0001-000000000001"]', '["ctrl0001-0001-0001-0001-000000000007"]', NULL, NOW(), NOW()),

  ('pol00001-0001-0001-0001-000000000005', '11111111-1111-1111-1111-111111111111', 'Acceptable Use Policy', '## 1. Purpose\nDefines acceptable and prohibited use of company systems and data.\n\n## 2. Acceptable Use\n- Business purposes only\n- No unauthorized software installation\n- No data exfiltration', '1.0', 'pending_review', 'aaaa0001-0001-0001-0001-000000000002', NULL, NULL, NULL, NULL, '[]', '[]', NULL, NOW(), NOW()),

  ('pol00001-0001-0001-0001-000000000006', '11111111-1111-1111-1111-111111111111', 'Vendor Management Policy', 'DRAFT: Vendor risk management procedures...', '0.1', 'draft', 'aaaa0001-0001-0001-0001-000000000002', NULL, NULL, NULL, NULL, '[]', '["ctrl0001-0001-0001-0001-000000000011"]', NULL, NOW(), NOW()),

  ('pol00001-0001-0001-0001-000000000007', '11111111-1111-1111-1111-111111111111', 'Password Policy', '## 1. Purpose\nDefines password requirements.\n\n## 2. Requirements\n- Minimum 12 characters\n- Complexity requirements\n- 90-day rotation\n- No password reuse (last 12)', '1.0', 'archived', 'aaaa0001-0001-0001-0001-000000000002', 'aaaa0001-0001-0001-0001-000000000001', NOW() - INTERVAL '400 days', NOW() - INTERVAL '395 days', NOW() - INTERVAL '30 days', '["ff000001-0001-0001-0001-000000000001"]', '[]', NULL, NOW(), NOW());

-- ============================================================================
-- 11. RISKS
-- ============================================================================
INSERT INTO risks (id, org_id, title, description, category, likelihood, impact, risk_score, risk_level, status, treatment_plan, treatment_type, treatment_status, treatment_due_date, residual_likelihood, residual_impact, residual_score, owner_id, reviewer_id, last_review_date, next_review_date, created_at, updated_at)
VALUES
  ('risk0001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'Unauthorized Access to Production Database', 'Risk of unauthorized access to production PostgreSQL database containing customer data', 'technical', 2, 5, 10, 'high', 'mitigated', 'Implement network segmentation, enforce MFA, enable database audit logging, restrict access to VPN-only', 'mitigate', 'completed', NOW() - INTERVAL '30 days', 1, 3, 3, 'aaaa0001-0001-0001-0001-000000000003', 'aaaa0001-0001-0001-0001-000000000002', NOW() - INTERVAL '15 days', NOW() + INTERVAL '75 days', NOW(), NOW()),

  ('risk0001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'Third-Party Data Breach', 'Risk of customer data exposure through compromised vendor or integration partner', 'vendor', 3, 4, 12, 'high', 'treating', 'Establish vendor assessment program, require SOC 2 reports, limit data shared with vendors', 'mitigate', 'in_progress', NOW() + INTERVAL '60 days', NULL, NULL, NULL, 'aaaa0001-0001-0001-0001-000000000002', 'aaaa0001-0001-0001-0001-000000000005', NOW() - INTERVAL '10 days', NOW() + INTERVAL '80 days', NOW(), NOW()),

  ('risk0001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', 'Ransomware Attack', 'Risk of ransomware infection disrupting business operations and encrypting critical data', 'technical', 3, 5, 15, 'critical', 'treating', 'Deploy EDR solution, implement network segmentation, maintain offline backups, conduct phishing training', 'mitigate', 'in_progress', NOW() + INTERVAL '45 days', NULL, NULL, NULL, 'aaaa0001-0001-0001-0001-000000000003', 'aaaa0001-0001-0001-0001-000000000005', NOW() - INTERVAL '5 days', NOW() + INTERVAL '85 days', NOW(), NOW()),

  ('risk0001-0001-0001-0001-000000000004', '11111111-1111-1111-1111-111111111111', 'Key Employee Departure', 'Risk of operational disruption due to departure of key engineering staff without knowledge transfer', 'operational', 4, 3, 12, 'high', 'identified', NULL, 'mitigate', NULL, NULL, NULL, NULL, NULL, 'aaaa0001-0001-0001-0001-000000000005', NULL, NULL, NULL, NOW(), NOW()),

  ('risk0001-0001-0001-0001-000000000005', '11111111-1111-1111-1111-111111111111', 'Regulatory Non-Compliance Fine', 'Risk of fines from GDPR/CCPA non-compliance due to improper data handling', 'compliance', 2, 4, 8, 'medium', 'accepted', 'Risk accepted with monitoring. Privacy controls in place. DPO appointed.', 'accept', 'completed', NULL, 2, 4, 8, 'aaaa0001-0001-0001-0001-000000000002', 'aaaa0001-0001-0001-0001-000000000005', NOW() - INTERVAL '20 days', NOW() + INTERVAL '70 days', NOW(), NOW()),

  ('risk0001-0001-0001-0001-000000000006', '11111111-1111-1111-1111-111111111111', 'Cloud Service Provider Outage', 'Risk of extended AWS outage impacting application availability', 'technical', 2, 3, 6, 'medium', 'mitigated', 'Multi-AZ deployment. DNS failover configured. Recovery playbook documented and tested.', 'mitigate', 'completed', NOW() - INTERVAL '60 days', 1, 2, 2, 'aaaa0001-0001-0001-0001-000000000003', NULL, NOW() - INTERVAL '30 days', NOW() + INTERVAL '60 days', NOW(), NOW()),

  ('risk0001-0001-0001-0001-000000000007', '11111111-1111-1111-1111-111111111111', 'Phishing Attack on Employees', 'Risk of successful phishing leading to credential compromise', 'people', 4, 3, 12, 'high', 'treating', 'Quarterly phishing simulations, security awareness training, email filtering, MFA enforcement', 'mitigate', 'in_progress', NOW() + INTERVAL '30 days', NULL, NULL, NULL, 'aaaa0001-0001-0001-0001-000000000002', NULL, NOW() - INTERVAL '7 days', NOW() + INTERVAL '83 days', NOW(), NOW());

-- ============================================================================
-- 12. RISK CONTROL MAPPINGS
-- ============================================================================
INSERT INTO risk_control_mappings (id, risk_id, control_id, created_at, updated_at)
VALUES
  ('rcm00001-0001-0001-0001-000000000001', 'risk0001-0001-0001-0001-000000000001', 'ctrl0001-0001-0001-0001-000000000001', NOW(), NOW()),
  ('rcm00001-0001-0001-0001-000000000002', 'risk0001-0001-0001-0001-000000000001', 'ctrl0001-0001-0001-0001-000000000002', NOW(), NOW()),
  ('rcm00001-0001-0001-0001-000000000003', 'risk0001-0001-0001-0001-000000000002', 'ctrl0001-0001-0001-0001-000000000011', NOW(), NOW()),
  ('rcm00001-0001-0001-0001-000000000004', 'risk0001-0001-0001-0001-000000000003', 'ctrl0001-0001-0001-0001-000000000009', NOW(), NOW()),
  ('rcm00001-0001-0001-0001-000000000005', 'risk0001-0001-0001-0001-000000000007', 'ctrl0001-0001-0001-0001-000000000008', NOW(), NOW());

-- ============================================================================
-- 13. INCIDENTS
-- ============================================================================
INSERT INTO incidents (id, org_id, title, description, severity, status, category, assigned_to_id, detected_at, resolved_at, post_mortem_notes, related_control_ids, created_at, updated_at)
VALUES
  ('inc00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'Unauthorized S3 Bucket Access Attempt', 'CloudTrail logs show repeated unauthorized access attempts to the customer-data S3 bucket from an unknown IP address', 'P2', 'resolved', 'unauthorized_access', 'aaaa0001-0001-0001-0001-000000000003', NOW() - INTERVAL '15 days', NOW() - INTERVAL '14 days', 'Root cause: Leaked AWS access key in a public GitHub repo. Key rotated within 2 hours. Implemented pre-commit hooks for secret scanning.', '["ctrl0001-0001-0001-0001-000000000002"]', NOW(), NOW()),

  ('inc00001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'Phishing Email Targeting Finance Team', 'Multiple finance team members received a sophisticated phishing email impersonating the CEO requesting wire transfer', 'P3', 'closed', 'phishing', 'aaaa0001-0001-0001-0001-000000000002', NOW() - INTERVAL '45 days', NOW() - INTERVAL '44 days', 'No users clicked the link. Emails quarantined by email gateway. Additional phishing training scheduled.', '["ctrl0001-0001-0001-0001-000000000008"]', NOW(), NOW()),

  ('inc00001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', 'Production Database Slow Queries Causing Timeout', 'Application experiencing 5xx errors due to unoptimized database queries during peak load', 'P2', 'investigating', 'availability', 'aaaa0001-0001-0001-0001-000000000003', NOW() - INTERVAL '1 day', NULL, NULL, '[]', NOW(), NOW()),

  ('inc00001-0001-0001-0001-000000000004', '11111111-1111-1111-1111-111111111111', 'SSL Certificate Expiry Warning', 'Monitoring alert: SSL certificate for api.acme.com expires in 7 days', 'P4', 'open', 'configuration', 'aaaa0001-0001-0001-0001-000000000003', NOW() - INTERVAL '2 hours', NULL, NULL, '["ctrl0001-0001-0001-0001-000000000003"]', NOW(), NOW());

-- ============================================================================
-- 14. INCIDENT TIMELINE EVENTS
-- ============================================================================
INSERT INTO incident_timeline_events (id, incident_id, actor_id, event_type, description, occurred_at, created_at, updated_at)
VALUES
  ('ite00001-0001-0001-0001-000000000001', 'inc00001-0001-0001-0001-000000000001', 'aaaa0001-0001-0001-0001-000000000003', 'status_change', 'Incident opened - Unauthorized S3 access detected via CloudTrail', NOW() - INTERVAL '15 days', NOW(), NOW()),
  ('ite00001-0001-0001-0001-000000000002', 'inc00001-0001-0001-0001-000000000001', 'aaaa0001-0001-0001-0001-000000000003', 'note', 'Identified leaked access key in public GitHub repository acme/internal-tools commit abc123', NOW() - INTERVAL '15 days' + INTERVAL '30 minutes', NOW(), NOW()),
  ('ite00001-0001-0001-0001-000000000003', 'inc00001-0001-0001-0001-000000000001', 'aaaa0001-0001-0001-0001-000000000001', 'assignment', 'Escalated to Dave DevOps for immediate key rotation', NOW() - INTERVAL '15 days' + INTERVAL '45 minutes', NOW(), NOW()),
  ('ite00001-0001-0001-0001-000000000004', 'inc00001-0001-0001-0001-000000000001', 'aaaa0001-0001-0001-0001-000000000003', 'note', 'AWS access key rotated. Old key deactivated. No evidence of data exfiltration in CloudTrail logs.', NOW() - INTERVAL '14 days' + INTERVAL '2 hours', NOW(), NOW()),
  ('ite00001-0001-0001-0001-000000000005', 'inc00001-0001-0001-0001-000000000001', 'aaaa0001-0001-0001-0001-000000000003', 'status_change', 'Incident resolved - Key rotated, pre-commit hooks implemented', NOW() - INTERVAL '14 days', NOW(), NOW()),
  ('ite00001-0001-0001-0001-000000000006', 'inc00001-0001-0001-0001-000000000003', 'aaaa0001-0001-0001-0001-000000000003', 'status_change', 'Incident opened - Database performance degradation detected', NOW() - INTERVAL '1 day', NOW(), NOW()),
  ('ite00001-0001-0001-0001-000000000007', 'inc00001-0001-0001-0001-000000000003', 'aaaa0001-0001-0001-0001-000000000003', 'note', 'Analyzing slow query logs. Suspect missing index on orders.customer_id column.', NOW() - INTERVAL '22 hours', NOW(), NOW());

-- ============================================================================
-- 15. AUDITS
-- ============================================================================
INSERT INTO audits (id, org_id, title, framework_id, audit_type, status, auditor_firm, lead_auditor_name, scheduled_start, scheduled_end, readiness_score, created_at, updated_at)
VALUES
  ('aud00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'SOC 2 Type II Annual Audit 2026', 'ff000001-0001-0001-0001-000000000001', 'external', 'fieldwork', 'Deloitte & Touche', 'Sarah Johnson, CPA', NOW() + INTERVAL '30 days', NOW() + INTERVAL '60 days', 78.5, NOW(), NOW()),
  ('aud00001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'Internal Security Review Q1 2026', NULL, 'internal', 'completed', NULL, 'Grace Auditor', NOW() - INTERVAL '45 days', NOW() - INTERVAL '30 days', 82.0, NOW(), NOW()),
  ('aud00001-0001-0001-0001-000000000003', '22222222-2222-2222-2222-222222222222', 'HIPAA Security Risk Assessment 2026', 'ff000001-0001-0001-0001-000000000003', 'external', 'planning', 'KPMG', 'Michael Chen', NOW() + INTERVAL '90 days', NOW() + INTERVAL '120 days', NULL, NOW(), NOW());

-- ============================================================================
-- 16. AUDIT FINDINGS
-- ============================================================================
INSERT INTO audit_findings (id, audit_id, title, description, severity, status, remediation_plan, remediation_due_date, created_at, updated_at)
VALUES
  ('af000001-0001-0001-0001-000000000001', 'aud00001-0001-0001-0001-000000000002', 'Incomplete Access Review Coverage', 'Q4 2025 access review campaign covered only 85% of systems. AWS console and Slack admin access were not included.', 'medium', 'remediation_in_progress', 'Expand access review template to include all AWS accounts and Slack workspace admin roles', NOW() + INTERVAL '30 days', NOW(), NOW()),
  ('af000001-0001-0001-0001-000000000002', 'aud00001-0001-0001-0001-000000000002', 'Missing Backup Restore Test Documentation', 'No documented evidence of backup restore testing in the last 6 months', 'high', 'open', 'Conduct monthly restore tests and document results in QuickTrust evidence module', NOW() + INTERVAL '14 days', NOW(), NOW()),
  ('af000001-0001-0001-0001-000000000003', 'aud00001-0001-0001-0001-000000000002', 'Stale Evidence for Logging Control', 'CloudTrail evidence was 45 days old at time of review. Collection should be automated.', 'low', 'closed', 'Configured automated weekly CloudTrail evidence collection via AWS integration', NOW() - INTERVAL '15 days', NOW(), NOW());

-- ============================================================================
-- 17. VENDORS
-- ============================================================================
INSERT INTO vendors (id, org_id, name, category, website, risk_tier, status, contact_name, contact_email, contract_start_date, contract_end_date, last_assessment_date, next_assessment_date, assessment_score, notes, tags, created_at, updated_at)
VALUES
  ('vnd00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'AWS', 'cloud_infrastructure', 'https://aws.amazon.com', 'critical', 'active', 'AWS Enterprise Support', 'support@aws.amazon.com', '2024-01-01', '2026-12-31', NOW() - INTERVAL '30 days', NOW() + INTERVAL '335 days', 95, 'Primary cloud provider. SOC 2 report on file.', '["cloud","infrastructure","critical"]', NOW(), NOW()),

  ('vnd00001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'Datadog', 'monitoring', 'https://datadog.com', 'high', 'active', 'Jane Smith', 'jane.smith@datadog.com', '2025-03-01', '2026-02-28', NOW() - INTERVAL '90 days', NOW() + INTERVAL '275 days', 88, 'Application monitoring and log aggregation', '["monitoring","saas"]', NOW(), NOW()),

  ('vnd00001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', 'Stripe', 'payment_processing', 'https://stripe.com', 'critical', 'active', 'Stripe Support', 'support@stripe.com', '2024-06-01', '2026-05-31', NOW() - INTERVAL '60 days', NOW() + INTERVAL '305 days', 92, 'Payment processing. PCI DSS Level 1 certified.', '["payments","pci","critical"]', NOW(), NOW()),

  ('vnd00001-0001-0001-0001-000000000004', '11111111-1111-1111-1111-111111111111', 'Okta', 'identity', 'https://okta.com', 'critical', 'active', 'Okta Account Manager', 'am@okta.com', '2024-01-15', '2026-01-14', NOW() - INTERVAL '45 days', NOW() + INTERVAL '320 days', 90, 'SSO and MFA provider for all applications', '["identity","sso","mfa","critical"]', NOW(), NOW()),

  ('vnd00001-0001-0001-0001-000000000005', '11111111-1111-1111-1111-111111111111', 'Slack', 'communication', 'https://slack.com', 'medium', 'active', NULL, NULL, '2025-01-01', '2026-12-31', NULL, NOW() + INTERVAL '90 days', NULL, 'Team communication platform', '["communication","saas"]', NOW(), NOW()),

  ('vnd00001-0001-0001-0001-000000000006', '11111111-1111-1111-1111-111111111111', 'Legacy CRM Vendor', 'crm', 'https://legacycrm.example.com', 'low', 'terminated', 'Bob Legacy', 'bob@legacycrm.example.com', '2022-01-01', '2025-06-30', NOW() - INTERVAL '200 days', NULL, 60, 'Contract terminated. Migration to HubSpot complete.', '["crm","terminated"]', NOW(), NOW());

-- ============================================================================
-- 18. VENDOR ASSESSMENTS
-- ============================================================================
INSERT INTO vendor_assessments (id, vendor_id, org_id, assessed_by_id, assessment_date, score, risk_tier_assigned, notes, questionnaire_data, created_at, updated_at)
VALUES
  ('va000001-0001-0001-0001-000000000001', 'vnd00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'aaaa0001-0001-0001-0001-000000000002', NOW() - INTERVAL '30 days', 95, 'critical', 'SOC 2 Type II report reviewed. ISO 27001 certified. Excellent security posture.', '{"encryption": "yes", "mfa": "yes", "soc2": "yes", "pentest_frequency": "quarterly"}', NOW(), NOW()),
  ('va000001-0001-0001-0001-000000000002', 'vnd00001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', 'aaaa0001-0001-0001-0001-000000000002', NOW() - INTERVAL '60 days', 92, 'critical', 'PCI DSS Level 1 certified. Strong data handling practices.', '{"encryption": "yes", "mfa": "yes", "pci_certified": "level_1", "data_residency": "us"}', NOW(), NOW());

-- ============================================================================
-- 19. TRAINING COURSES
-- ============================================================================
INSERT INTO training_courses (id, org_id, title, description, content_url, course_type, required_roles, duration_minutes, is_required, is_active, created_at, updated_at)
VALUES
  ('tc000001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'Security Awareness Fundamentals', 'Annual security awareness training covering phishing, password hygiene, data handling, and incident reporting procedures', 'https://training.acme.com/security-101', 'document', '["employee","control_owner","compliance_manager","admin"]', 45, true, true, NOW(), NOW()),
  ('tc000001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'GDPR Data Privacy Training', 'Understanding GDPR requirements, data subject rights, lawful processing, and breach notification obligations', 'https://training.acme.com/gdpr', 'video', '["employee","compliance_manager"]', 30, true, true, NOW(), NOW()),
  ('tc000001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', 'Secure Coding Practices', 'OWASP Top 10, secure code review, input validation, and output encoding for developers', 'https://training.acme.com/secure-coding', 'quiz', '["control_owner"]', 60, false, true, NOW(), NOW()),
  ('tc000001-0001-0001-0001-000000000004', '11111111-1111-1111-1111-111111111111', 'Incident Response Procedures', 'How to identify, report, and respond to security incidents per the IRP', 'https://training.acme.com/ir-procedures', 'document', '["employee","control_owner","compliance_manager","admin"]', 20, true, true, NOW(), NOW());

-- ============================================================================
-- 20. TRAINING ASSIGNMENTS
-- ============================================================================
INSERT INTO training_assignments (id, org_id, course_id, user_id, status, due_date, completed_at, score, attempts, assigned_by_id, created_at, updated_at)
VALUES
  ('ta000001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'tc000001-0001-0001-0001-000000000001', 'aaaa0001-0001-0001-0001-000000000004', 'completed', NOW() - INTERVAL '10 days', NOW() - INTERVAL '12 days', 92, 1, 'aaaa0001-0001-0001-0001-000000000002', NOW(), NOW()),
  ('ta000001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'tc000001-0001-0001-0001-000000000001', 'aaaa0001-0001-0001-0001-000000000003', 'completed', NOW() - INTERVAL '10 days', NOW() - INTERVAL '15 days', 88, 1, 'aaaa0001-0001-0001-0001-000000000002', NOW(), NOW()),
  ('ta000001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', 'tc000001-0001-0001-0001-000000000002', 'aaaa0001-0001-0001-0001-000000000004', 'in_progress', NOW() + INTERVAL '20 days', NULL, NULL, 0, 'aaaa0001-0001-0001-0001-000000000002', NOW(), NOW()),
  ('ta000001-0001-0001-0001-000000000004', '11111111-1111-1111-1111-111111111111', 'tc000001-0001-0001-0001-000000000003', 'aaaa0001-0001-0001-0001-000000000003', 'assigned', NOW() + INTERVAL '30 days', NULL, NULL, 0, 'aaaa0001-0001-0001-0001-000000000002', NOW(), NOW()),
  ('ta000001-0001-0001-0001-000000000005', '11111111-1111-1111-1111-111111111111', 'tc000001-0001-0001-0001-000000000001', 'aaaa0001-0001-0001-0001-000000000005', 'overdue', NOW() - INTERVAL '30 days', NULL, NULL, 0, 'aaaa0001-0001-0001-0001-000000000002', NOW(), NOW()),
  ('ta000001-0001-0001-0001-000000000006', '11111111-1111-1111-1111-111111111111', 'tc000001-0001-0001-0001-000000000004', 'aaaa0001-0001-0001-0001-000000000004', 'completed', NOW() - INTERVAL '5 days', NOW() - INTERVAL '8 days', 100, 1, 'aaaa0001-0001-0001-0001-000000000002', NOW(), NOW());

-- ============================================================================
-- 21. ACCESS REVIEW CAMPAIGNS
-- ============================================================================
INSERT INTO access_review_campaigns (id, org_id, title, description, reviewer_id, status, due_date, completed_at, created_at, updated_at)
VALUES
  ('arc00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'Q1 2026 Quarterly Access Review', 'Quarterly access review covering all critical systems including AWS, GitHub, Okta, and database access', 'aaaa0001-0001-0001-0001-000000000001', 'active', NOW() + INTERVAL '15 days', NULL, NOW(), NOW()),
  ('arc00001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'Q4 2025 Quarterly Access Review', 'Quarterly access review for Q4 2025', 'aaaa0001-0001-0001-0001-000000000001', 'completed', NOW() - INTERVAL '60 days', NOW() - INTERVAL '62 days', NOW(), NOW());

-- ============================================================================
-- 22. ACCESS REVIEW ENTRIES
-- ============================================================================
INSERT INTO access_review_entries (id, campaign_id, org_id, user_name, user_email, system_name, resource, current_access, decision, decided_by_id, decided_at, notes, created_at, updated_at)
VALUES
  ('are00001-0001-0001-0001-000000000001', 'arc00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'Dave DevOps', 'devops@acme.com', 'AWS Console', 'Production Account', 'admin', 'approved', 'aaaa0001-0001-0001-0001-000000000001', NOW() - INTERVAL '2 days', 'Required for infrastructure management', NOW(), NOW()),
  ('are00001-0001-0001-0001-000000000002', 'arc00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'Eve Employee', 'employee@acme.com', 'AWS Console', 'Production Account', 'read-only', 'approved', 'aaaa0001-0001-0001-0001-000000000001', NOW() - INTERVAL '2 days', 'Needed for debugging production issues', NOW(), NOW()),
  ('are00001-0001-0001-0001-000000000003', 'arc00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'Former Contractor', 'contractor@external.com', 'GitHub', 'acme/main-app', 'write', 'revoked', 'aaaa0001-0001-0001-0001-000000000001', NOW() - INTERVAL '1 day', 'Contractor engagement ended. Access revoked.', NOW(), NOW()),
  ('are00001-0001-0001-0001-000000000004', 'arc00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'Charlie Compliance', 'compliance@acme.com', 'PostgreSQL', 'production-db', 'read-only', NULL, NULL, NULL, NULL, NOW(), NOW()),
  ('are00001-0001-0001-0001-000000000005', 'arc00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'Dave DevOps', 'devops@acme.com', 'Okta Admin', 'Admin Console', 'super_admin', NULL, NULL, NULL, NULL, NOW(), NOW());

-- ============================================================================
-- 23. MONITOR RULES
-- ============================================================================
INSERT INTO monitor_rules (id, org_id, control_id, title, description, check_type, schedule, is_active, config, last_checked_at, last_result, created_at, updated_at)
VALUES
  ('mr000001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'ctrl0001-0001-0001-0001-000000000001', 'MFA Evidence Freshness', 'Alert if MFA enrollment evidence is older than 30 days', 'evidence_staleness', 'daily', true, '{"max_age_days": 30}', NOW() - INTERVAL '6 hours', 'pass', NOW(), NOW()),
  ('mr000001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', NULL, 'Draft Controls Check', 'Alert if any controls remain in draft status for more than 14 days', 'control_status', 'daily', true, '{"target_statuses": ["draft"], "max_age_days": 14}', NOW() - INTERVAL '6 hours', 'fail', NOW(), NOW()),
  ('mr000001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', NULL, 'Policy Review Date Check', 'Alert when policies are approaching or past their next review date', 'policy_expiry', 'weekly', true, '{"warning_days_before": 30}', NOW() - INTERVAL '2 days', 'fail', NOW(), NOW()),
  ('mr000001-0001-0001-0001-000000000004', '11111111-1111-1111-1111-111111111111', 'ctrl0001-0001-0001-0001-000000000005', 'Prowler Scan Recency', 'Alert if Prowler scan results are older than 7 days', 'evidence_staleness', 'daily', true, '{"max_age_days": 7}', NOW() - INTERVAL '6 hours', 'pass', NOW(), NOW());

-- ============================================================================
-- 24. MONITOR ALERTS
-- ============================================================================
INSERT INTO monitor_alerts (id, org_id, rule_id, severity, status, title, details, triggered_at, resolved_at, acknowledged_by_id, created_at, updated_at)
VALUES
  ('ma000001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'mr000001-0001-0001-0001-000000000002', 'medium', 'open', 'Controls in Draft Status', '{"controls_in_draft": ["ctrl0001-0001-0001-0001-000000000010", "ctrl0001-0001-0001-0001-000000000012"], "count": 2}', NOW() - INTERVAL '6 hours', NULL, NULL, NOW(), NOW()),
  ('ma000001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'mr000001-0001-0001-0001-000000000003', 'high', 'acknowledged', 'Password Policy Past Review Date', '{"policy_id": "pol00001-0001-0001-0001-000000000007", "policy_title": "Password Policy", "days_overdue": 30}', NOW() - INTERVAL '2 days', NULL, 'aaaa0001-0001-0001-0001-000000000002', NOW(), NOW()),
  ('ma000001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', 'mr000001-0001-0001-0001-000000000001', 'low', 'resolved', 'MFA Evidence Approaching Staleness', '{"evidence_id": "ev000001-0001-0001-0001-000000000001", "age_days": 28}', NOW() - INTERVAL '5 days', NOW() - INTERVAL '3 days', 'aaaa0001-0001-0001-0001-000000000003', NOW(), NOW());

-- ============================================================================
-- 25. INTEGRATIONS
-- ============================================================================
INSERT INTO integrations (id, org_id, provider, name, status, config, credentials_ref, last_sync_at, created_at, updated_at)
VALUES
  ('int00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'aws', 'AWS Production Account', 'connected', '{"region": "us-east-1", "account_id": "123456789012"}', 'vault://aws/prod-credentials', NOW() - INTERVAL '1 day', NOW(), NOW()),
  ('int00001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'github', 'GitHub Organization', 'connected', '{"org_name": "acme-corp", "repos": ["main-app", "api-service", "infra"]}', 'vault://github/token', NOW() - INTERVAL '1 day', NOW(), NOW()),
  ('int00001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', 'okta', 'Okta Workforce', 'connected', '{"domain": "acme.okta.com"}', 'vault://okta/api-key', NOW() - INTERVAL '2 days', NOW(), NOW()),
  ('int00001-0001-0001-0001-000000000004', '11111111-1111-1111-1111-111111111111', 'prowler', 'Prowler AWS Scanner', 'connected', '{"scan_type": "full", "compliance_frameworks": ["cis", "soc2"]}', 'vault://aws/prowler-role', NOW() - INTERVAL '2 days', NOW(), NOW()),
  ('int00001-0001-0001-0001-000000000005', '11111111-1111-1111-1111-111111111111', 'aws', 'AWS Staging Account', 'disconnected', '{"region": "us-east-1", "account_id": "987654321098"}', NULL, NULL, NOW(), NOW());

-- ============================================================================
-- 26. COLLECTION JOBS
-- ============================================================================
INSERT INTO collection_jobs (id, org_id, integration_id, evidence_template_id, control_id, status, collector_type, result_data, evidence_id, error_message, created_at, updated_at)
VALUES
  ('cj000001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'int00001-0001-0001-0001-000000000001', NULL, 'ctrl0001-0001-0001-0001-000000000001', 'completed', 'aws_iam_mfa', '{"total_users": 12, "mfa_enabled": 12, "compliant": true}', 'ev000001-0001-0001-0001-000000000002', NULL, NOW(), NOW()),
  ('cj000001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'int00001-0001-0001-0001-000000000002', NULL, 'ctrl0001-0001-0001-0001-000000000006', 'completed', 'github_branch_protection', '{"repos_checked": 8, "all_protected": true}', 'ev000001-0001-0001-0001-000000000007', NULL, NOW(), NOW()),
  ('cj000001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', 'int00001-0001-0001-0001-000000000003', NULL, 'ctrl0001-0001-0001-0001-000000000001', 'completed', 'okta_mfa_enrollment', '{"total_users": 148, "enrolled": 145, "rate": 0.98}', 'ev000001-0001-0001-0001-000000000001', NULL, NOW(), NOW()),
  ('cj000001-0001-0001-0001-000000000004', '11111111-1111-1111-1111-111111111111', 'int00001-0001-0001-0001-000000000004', NULL, 'ctrl0001-0001-0001-0001-000000000005', 'completed', 'prowler_full_scan', '{"total_checks": 245, "pass": 228, "fail": 12, "pass_rate": 0.93}', 'ev000001-0001-0001-0001-000000000006', NULL, NOW(), NOW()),
  ('cj000001-0001-0001-0001-000000000005', '11111111-1111-1111-1111-111111111111', 'int00001-0001-0001-0001-000000000005', NULL, NULL, 'failed', 'aws_iam_mfa', NULL, NULL, 'InvalidCredentials: AWS access key not configured for staging account', NOW(), NOW());

-- ============================================================================
-- 27. QUESTIONNAIRES
-- ============================================================================
INSERT INTO questionnaires (id, org_id, title, source, status, questions, total_questions, answered_count, created_at, updated_at)
VALUES
  ('qst00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'Enterprise Customer Security Questionnaire', 'Acme Corp - BigBank RFP', 'in_progress', '[{"id": "q1", "text": "Do you enforce MFA for all users?"}, {"id": "q2", "text": "Is data encrypted at rest?"}, {"id": "q3", "text": "Do you have a SOC 2 report?"}, {"id": "q4", "text": "What is your incident response time SLA?"}, {"id": "q5", "text": "Do you conduct penetration tests?"}]', 5, 3, NOW(), NOW()),
  ('qst00001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'Vendor Onboarding Security Assessment', 'Acme Corp - Partner Portal', 'completed', '[{"id": "q1", "text": "Describe your access control mechanisms"}, {"id": "q2", "text": "How do you handle data at rest encryption?"}, {"id": "q3", "text": "What compliance certifications do you hold?"}]', 3, 3, NOW(), NOW()),
  ('qst00001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', 'CAIQ (Consensus Assessments Initiative Questionnaire)', 'CSA STAR', 'draft', '[]', 0, 0, NOW(), NOW());

-- ============================================================================
-- 28. QUESTIONNAIRE RESPONSES
-- ============================================================================
INSERT INTO questionnaire_responses (id, questionnaire_id, org_id, question_id, question_text, answer, confidence, source_type, source_id, is_approved, approved_by_id, created_at, updated_at)
VALUES
  ('qr000001-0001-0001-0001-000000000001', 'qst00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'q1', 'Do you enforce MFA for all users?', 'Yes. Multi-factor authentication is enforced for all users via Okta with TOTP and WebAuthn support. MFA enrollment rate is 98%. Conditional access policies require MFA for all admin and production access.', 0.95, 'control', 'ctrl0001-0001-0001-0001-000000000001', true, 'aaaa0001-0001-0001-0001-000000000002', NOW(), NOW()),
  ('qr000001-0001-0001-0001-000000000002', 'qst00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'q2', 'Is data encrypted at rest?', 'Yes. All data at rest is encrypted using AES-256. AWS RDS instances, S3 buckets (SSE-S3), and EBS volumes are all configured with encryption by default.', 0.92, 'control', 'ctrl0001-0001-0001-0001-000000000002', true, 'aaaa0001-0001-0001-0001-000000000002', NOW(), NOW()),
  ('qr000001-0001-0001-0001-000000000003', 'qst00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'q3', 'Do you have a SOC 2 report?', 'Our SOC 2 Type II audit is currently in fieldwork phase, scheduled for completion in Q2 2026. We can provide the report upon completion.', 0.78, 'manual', NULL, false, NULL, NOW(), NOW());

-- ============================================================================
-- 29. TRUST CENTER CONFIG & DOCUMENTS
-- ============================================================================
INSERT INTO trust_center_configs (id, org_id, is_published, slug, headline, description, contact_email, logo_url, certifications, branding, created_at, updated_at)
VALUES
  ('tcc00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', true, 'acme-corp', 'Acme Corp Trust Center', 'Learn about our commitment to security, privacy, and compliance. We are dedicated to protecting your data with enterprise-grade controls.', 'security@acme.com', 'https://acme.com/logo.png', '["SOC 2 Type II (in progress)", "ISO 27001 (planned)"]', '{"primary_color": "#1a73e8", "font": "Inter"}', NOW(), NOW());

INSERT INTO trust_center_documents (id, org_id, title, document_type, is_public, requires_nda, file_url, description, valid_until, sort_order, created_at, updated_at)
VALUES
  ('tcd00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'Information Security Policy', 'policy', true, false, 's3://trust-center/acme/info-sec-policy.pdf', 'Our comprehensive information security policy covering data protection, access control, and incident response', NULL, 1, NOW(), NOW()),
  ('tcd00001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'SOC 2 Type II Report', 'soc2', false, true, NULL, 'SOC 2 Type II audit report - available upon request with signed NDA', NOW() + INTERVAL '365 days', 2, NOW(), NOW()),
  ('tcd00001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', 'Penetration Test Summary', 'pentest', false, true, 's3://trust-center/acme/pentest-summary-2025.pdf', 'Annual penetration test executive summary', NOW() + INTERVAL '180 days', 3, NOW(), NOW());

-- ============================================================================
-- 30. REPORTS
-- ============================================================================
INSERT INTO reports (id, org_id, title, report_type, format, status, parameters, generated_at, file_url, requested_by_id, error_message, created_at, updated_at)
VALUES
  ('rpt00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'Compliance Summary - March 2026', 'compliance_summary', 'pdf', 'completed', '{"date_range": "2026-03-01/2026-03-31"}', NOW() - INTERVAL '1 day', 's3://reports/acme/compliance-summary-2026-03.pdf', 'aaaa0001-0001-0001-0001-000000000002', NULL, NOW(), NOW()),
  ('rpt00001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'Risk Register Export', 'risk_report', 'csv', 'completed', '{}', NOW() - INTERVAL '3 days', 's3://reports/acme/risk-register-2026-02.csv', 'aaaa0001-0001-0001-0001-000000000005', NULL, NOW(), NOW()),
  ('rpt00001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', 'Evidence Audit Trail', 'evidence_audit', 'pdf', 'generating', '{"framework_id": "ff000001-0001-0001-0001-000000000001"}', NULL, NULL, 'aaaa0001-0001-0001-0001-000000000002', NULL, NOW(), NOW()),
  ('rpt00001-0001-0001-0001-000000000004', '11111111-1111-1111-1111-111111111111', 'Training Completion Report', 'training_completion', 'pdf', 'completed', '{"quarter": "Q1 2026"}', NOW() - INTERVAL '2 days', 's3://reports/acme/training-q1-2026.pdf', 'aaaa0001-0001-0001-0001-000000000002', NULL, NOW(), NOW());

-- ============================================================================
-- 31. NOTIFICATIONS
-- ============================================================================
INSERT INTO notifications (id, org_id, user_id, channel, category, title, message, severity, entity_type, entity_id, is_read, read_at, sent_at, metadata, created_at, updated_at)
VALUES
  ('ntf00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'aaaa0001-0001-0001-0001-000000000002', 'in_app', 'monitoring_alert', 'Controls in Draft Status', '2 controls have been in draft status for more than 14 days. Please review and update their status.', 'warning', 'monitor_alert', 'ma000001-0001-0001-0001-000000000001', false, NULL, NOW() - INTERVAL '6 hours', '{}', NOW(), NOW()),
  ('ntf00001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'aaaa0001-0001-0001-0001-000000000002', 'in_app', 'policy_expiry', 'Password Policy Overdue for Review', 'The Password Policy is 30 days past its review date. Please update or archive this policy.', 'critical', 'policy', 'pol00001-0001-0001-0001-000000000007', true, NOW() - INTERVAL '1 day', NOW() - INTERVAL '2 days', '{}', NOW(), NOW()),
  ('ntf00001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', 'aaaa0001-0001-0001-0001-000000000003', 'in_app', 'incident', 'New Incident Assigned', 'You have been assigned to incident: Production Database Slow Queries Causing Timeout (P2)', 'warning', 'incident', 'inc00001-0001-0001-0001-000000000003', false, NULL, NOW() - INTERVAL '1 day', '{}', NOW(), NOW()),
  ('ntf00001-0001-0001-0001-000000000004', '11111111-1111-1111-1111-111111111111', 'aaaa0001-0001-0001-0001-000000000005', 'in_app', 'training', 'Training Overdue', 'Security Awareness Fundamentals training is 30 days overdue. Please complete it as soon as possible.', 'warning', 'training_assignment', 'ta000001-0001-0001-0001-000000000005', false, NULL, NOW() - INTERVAL '3 days', '{}', NOW(), NOW()),
  ('ntf00001-0001-0001-0001-000000000005', '11111111-1111-1111-1111-111111111111', 'aaaa0001-0001-0001-0001-000000000001', 'in_app', 'access_review', 'Access Review Entries Pending Decision', '2 access review entries in Q1 2026 campaign still need your decision.', 'info', 'access_review_campaign', 'arc00001-0001-0001-0001-000000000001', false, NULL, NOW() - INTERVAL '12 hours', '{}', NOW(), NOW());

-- ============================================================================
-- 32. AUDIT LOGS
-- ============================================================================
INSERT INTO audit_logs (id, org_id, actor_type, actor_id, action, entity_type, entity_id, changes, ip_address, timestamp)
VALUES
  ('al000001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'user', 'aaaa0001-0001-0001-0001-000000000001', 'create', 'organization', '11111111-1111-1111-1111-111111111111', '{"name": "Acme Corp"}', '10.0.1.100', NOW() - INTERVAL '90 days'),
  ('al000001-0001-0001-0001-000000000002', '11111111-1111-1111-1111-111111111111', 'user', 'aaaa0001-0001-0001-0001-000000000002', 'update', 'policy', 'pol00001-0001-0001-0001-000000000001', '{"status": {"old": "draft", "new": "published"}}', '10.0.1.101', NOW() - INTERVAL '28 days'),
  ('al000001-0001-0001-0001-000000000003', '11111111-1111-1111-1111-111111111111', 'agent', 'ar000001-0001-0001-0001-000000000001', 'create', 'control', 'ctrl0001-0001-0001-0001-000000000001', '{"title": "Multi-Factor Authentication Enforcement", "source": "ai_generated"}', NULL, NOW() - INTERVAL '85 days'),
  ('al000001-0001-0001-0001-000000000004', '11111111-1111-1111-1111-111111111111', 'user', 'aaaa0001-0001-0001-0001-000000000001', 'update', 'control', 'ctrl0001-0001-0001-0001-000000000001', '{"status": {"old": "draft", "new": "implemented"}}', '10.0.1.100', NOW() - INTERVAL '70 days'),
  ('al000001-0001-0001-0001-000000000005', '11111111-1111-1111-1111-111111111111', 'system', 'collection_service', 'create', 'evidence', 'ev000001-0001-0001-0001-000000000001', '{"collector": "okta_mfa_enrollment", "method": "automated"}', NULL, NOW() - INTERVAL '2 days'),
  ('al000001-0001-0001-0001-000000000006', '11111111-1111-1111-1111-111111111111', 'user', 'aaaa0001-0001-0001-0001-000000000003', 'update', 'incident', 'inc00001-0001-0001-0001-000000000001', '{"status": {"old": "open", "new": "resolved"}}', '10.0.1.102', NOW() - INTERVAL '14 days'),
  ('al000001-0001-0001-0001-000000000007', '11111111-1111-1111-1111-111111111111', 'user', 'aaaa0001-0001-0001-0001-000000000001', 'create', 'auditor_access_token', 'aud00001-0001-0001-0001-000000000001', '{"audit": "SOC 2 Type II Annual Audit 2026", "expires_in": "72h"}', '10.0.1.100', NOW() - INTERVAL '5 days'),
  ('al000001-0001-0001-0001-000000000008', '11111111-1111-1111-1111-111111111111', 'user', 'aaaa0001-0001-0001-0001-000000000001', 'delete', 'access_review_entry', 'are00001-0001-0001-0001-000000000003', '{"decision": "revoked", "user": "Former Contractor"}', '10.0.1.100', NOW() - INTERVAL '1 day');

-- ============================================================================
-- 33. ONBOARDING SESSIONS
-- ============================================================================
INSERT INTO onboarding_sessions (id, org_id, status, current_step, steps_completed, metadata, created_at, updated_at)
VALUES
  ('obs00001-0001-0001-0001-000000000001', '11111111-1111-1111-1111-111111111111', 'completed', 4, '["org_setup", "framework_selection", "agent_generation", "review"]', '{"frameworks_selected": ["SOC 2 Type II"], "controls_generated": 12, "policies_generated": 8}', NOW(), NOW()),
  ('obs00001-0001-0001-0001-000000000002', '22222222-2222-2222-2222-222222222222', 'in_progress', 2, '["org_setup", "framework_selection"]', '{"frameworks_selected": ["HIPAA"]}', NOW(), NOW()),
  ('obs00001-0001-0001-0001-000000000003', '33333333-3333-3333-3333-333333333333', 'pending', 1, '["org_setup"]', '{}', NOW(), NOW());

COMMIT;

-- ============================================================================
-- USEFUL TEST QUERIES
-- ============================================================================

-- 1. Dashboard overview for Acme Corp
-- SELECT
--   (SELECT COUNT(*) FROM controls WHERE org_id = '11111111-1111-1111-1111-111111111111') AS total_controls,
--   (SELECT COUNT(*) FROM controls WHERE org_id = '11111111-1111-1111-1111-111111111111' AND status = 'implemented') AS implemented_controls,
--   (SELECT COUNT(*) FROM evidence WHERE org_id = '11111111-1111-1111-1111-111111111111') AS total_evidence,
--   (SELECT COUNT(*) FROM policies WHERE org_id = '11111111-1111-1111-1111-111111111111' AND status = 'published') AS published_policies,
--   (SELECT COUNT(*) FROM risks WHERE org_id = '11111111-1111-1111-1111-111111111111') AS total_risks,
--   (SELECT COUNT(*) FROM incidents WHERE org_id = '11111111-1111-1111-1111-111111111111' AND status IN ('open', 'investigating')) AS open_incidents;

-- 2. Compliance score calculation
-- SELECT
--   ROUND(
--     (COUNT(*) FILTER (WHERE status = 'implemented') * 100.0 / NULLIF(COUNT(*), 0)),
--     1
--   ) AS compliance_percentage
-- FROM controls
-- WHERE org_id = '11111111-1111-1111-1111-111111111111';

-- 3. Risk matrix distribution
-- SELECT risk_level, COUNT(*) AS count
-- FROM risks
-- WHERE org_id = '11111111-1111-1111-1111-111111111111'
-- GROUP BY risk_level
-- ORDER BY
--   CASE risk_level WHEN 'critical' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 WHEN 'low' THEN 4 END;

-- 4. Evidence collection status per control
-- SELECT c.title AS control_title, c.status AS control_status,
--   COUNT(e.id) AS evidence_count,
--   COUNT(e.id) FILTER (WHERE e.status = 'collected') AS collected,
--   COUNT(e.id) FILTER (WHERE e.status = 'stale') AS stale,
--   COUNT(e.id) FILTER (WHERE e.status = 'pending') AS pending
-- FROM controls c
-- LEFT JOIN evidence e ON e.control_id = c.id
-- WHERE c.org_id = '11111111-1111-1111-1111-111111111111'
-- GROUP BY c.id, c.title, c.status
-- ORDER BY c.title;

-- 5. Policy lifecycle status
-- SELECT status, COUNT(*) AS count
-- FROM policies
-- WHERE org_id = '11111111-1111-1111-1111-111111111111'
-- GROUP BY status;

-- 6. Training completion rates
-- SELECT tc.title AS course,
--   COUNT(ta.id) AS assigned,
--   COUNT(ta.id) FILTER (WHERE ta.status = 'completed') AS completed,
--   ROUND(COUNT(ta.id) FILTER (WHERE ta.status = 'completed') * 100.0 / NULLIF(COUNT(ta.id), 0), 1) AS completion_rate
-- FROM training_courses tc
-- LEFT JOIN training_assignments ta ON ta.course_id = tc.id
-- WHERE tc.org_id = '11111111-1111-1111-1111-111111111111'
-- GROUP BY tc.id, tc.title;

-- 7. Vendor risk distribution
-- SELECT risk_tier, COUNT(*) AS count
-- FROM vendors
-- WHERE org_id = '11111111-1111-1111-1111-111111111111' AND status = 'active'
-- GROUP BY risk_tier;

-- 8. Open monitoring alerts
-- SELECT ma.title, ma.severity, ma.status, mr.check_type, ma.triggered_at
-- FROM monitor_alerts ma
-- JOIN monitor_rules mr ON mr.id = ma.rule_id
-- WHERE ma.org_id = '11111111-1111-1111-1111-111111111111' AND ma.status != 'resolved'
-- ORDER BY
--   CASE ma.severity WHEN 'critical' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 WHEN 'low' THEN 4 END;

-- 9. Agent run history
-- SELECT agent_type, status, trigger,
--   started_at, completed_at,
--   EXTRACT(EPOCH FROM (completed_at - started_at)) AS duration_seconds,
--   tokens_used
-- FROM agent_runs
-- WHERE org_id = '11111111-1111-1111-1111-111111111111'
-- ORDER BY created_at DESC;

-- 10. Multi-tenant isolation verification
-- SELECT 'organizations' AS entity, org_id, COUNT(*) FROM users GROUP BY org_id
-- UNION ALL
-- SELECT 'controls', org_id, COUNT(*) FROM controls GROUP BY org_id
-- UNION ALL
-- SELECT 'policies', org_id, COUNT(*) FROM policies GROUP BY org_id
-- UNION ALL
-- SELECT 'risks', org_id, COUNT(*) FROM risks GROUP BY org_id
-- UNION ALL
-- SELECT 'evidence', org_id, COUNT(*) FROM evidence GROUP BY org_id
-- ORDER BY entity, org_id;

-- 11. Audit readiness overview
-- SELECT a.title, a.audit_type, a.status, a.readiness_score,
--   a.scheduled_start, a.scheduled_end,
--   COUNT(af.id) AS total_findings,
--   COUNT(af.id) FILTER (WHERE af.status = 'open') AS open_findings
-- FROM audits a
-- LEFT JOIN audit_findings af ON af.audit_id = a.id
-- WHERE a.org_id = '11111111-1111-1111-1111-111111111111'
-- GROUP BY a.id;

-- 12. Unread notifications per user
-- SELECT u.full_name, u.role, COUNT(n.id) AS unread_count
-- FROM users u
-- LEFT JOIN notifications n ON n.user_id = u.id AND n.is_read = false
-- WHERE u.org_id = '11111111-1111-1111-1111-111111111111'
-- GROUP BY u.id, u.full_name, u.role
-- HAVING COUNT(n.id) > 0;
