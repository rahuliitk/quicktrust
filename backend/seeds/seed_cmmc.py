"""CMMC 2.0 (Cybersecurity Maturity Model Certification) — framework seed data."""

CMMC_FRAMEWORK = {
    "name": "CMMC 2.0",
    "version": "2.0",
    "category": "Government & Federal",
    "description": "Cybersecurity Maturity Model Certification (CMMC) 2.0 — a framework required by the U.S. Department of Defense for contractors handling Federal Contract Information (FCI) and Controlled Unclassified Information (CUI), establishing three levels of cybersecurity maturity.",
    "domains": [
        {
            "code": "CMMC-AC",
            "name": "Access Control",
            "description": "Controls to limit information system access to authorized users, processes acting on behalf of authorized users, and devices, and to limit transactions and functions that authorized users are permitted to execute.",
            "sort_order": 1,
            "requirements": [
                {
                    "code": "CMMC-AC.L1-3.1.1",
                    "title": "Authorized Access Control",
                    "description": "Limit information system access to authorized users, processes acting on behalf of authorized users, or devices (including other information systems).",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CMMC-AC.L1-3.1.1a", "title": "System access is limited to authorized users and devices", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-AC.L1-3.1.2",
                    "title": "Transaction and Function Control",
                    "description": "Limit information system access to the types of transactions and functions that authorized users are permitted to execute.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CMMC-AC.L1-3.1.2a", "title": "Authorized transactions and functions are enforced", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-AC.L2-3.1.3",
                    "title": "CUI Flow Enforcement",
                    "description": "Control the flow of CUI in accordance with approved authorizations.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CMMC-AC.L2-3.1.3a", "title": "CUI flow controls are enforced", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-AC.L2-3.1.5",
                    "title": "Least Privilege",
                    "description": "Employ the principle of least privilege, including for specific security functions and privileged accounts.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CMMC-AC.L2-3.1.5a", "title": "Least privilege is applied to all accounts", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-AC.L2-3.1.12",
                    "title": "Remote Access Control",
                    "description": "Monitor and control remote access sessions.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "CMMC-AC.L2-3.1.12a", "title": "Remote access sessions are monitored and controlled", "sort_order": 1},
                        {"code": "CMMC-AC.L2-3.1.12b", "title": "Cryptographic mechanisms protect remote access", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "CMMC-AT",
            "name": "Awareness and Training",
            "description": "Controls to ensure that managers, systems administrators, and users of organizational systems are made aware of security risks and trained to carry out their information security responsibilities.",
            "sort_order": 2,
            "requirements": [
                {
                    "code": "CMMC-AT.L2-3.2.1",
                    "title": "Role-Based Risk Awareness",
                    "description": "Ensure that managers, systems administrators, and users of organizational systems are made aware of the security risks associated with their activities and of the applicable policies, standards, and procedures related to the security of those systems.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CMMC-AT.L2-3.2.1a", "title": "Security risk awareness is provided to all personnel", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-AT.L2-3.2.2",
                    "title": "Role-Based Training",
                    "description": "Ensure that personnel are trained to carry out their assigned information security-related duties and responsibilities.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CMMC-AT.L2-3.2.2a", "title": "Role-based security training is completed", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-AT.L2-3.2.3",
                    "title": "Insider Threat Awareness",
                    "description": "Provide security awareness training on recognizing and reporting potential indicators of insider threat.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CMMC-AT.L2-3.2.3a", "title": "Insider threat awareness training is provided", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CMMC-AU",
            "name": "Audit and Accountability",
            "description": "Controls to create and retain system audit logs and records to enable monitoring, analysis, investigation, and reporting of unlawful or unauthorized system activity.",
            "sort_order": 3,
            "requirements": [
                {
                    "code": "CMMC-AU.L2-3.3.1",
                    "title": "System Auditing",
                    "description": "Create and retain system audit logs and records to the extent needed to enable the monitoring, analysis, investigation, and reporting of unlawful or unauthorized system activity.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CMMC-AU.L2-3.3.1a", "title": "Audit logs are created and retained", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-AU.L2-3.3.2",
                    "title": "User Accountability",
                    "description": "Ensure that the actions of individual system users can be uniquely traced to those users so they can be held accountable for their actions.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CMMC-AU.L2-3.3.2a", "title": "User actions are uniquely traceable", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-AU.L2-3.3.5",
                    "title": "Audit Review and Correlation",
                    "description": "Correlate audit record review, analysis, and reporting processes for investigation and response to indications of unlawful, unauthorized, suspicious, or unusual activity.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CMMC-AU.L2-3.3.5a", "title": "Audit records are reviewed and correlated", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-AU.L2-3.3.8",
                    "title": "Audit Protection",
                    "description": "Protect audit information and audit logging tools from unauthorized access, modification, and deletion.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CMMC-AU.L2-3.3.8a", "title": "Audit information is protected from tampering", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CMMC-CM",
            "name": "Configuration Management",
            "description": "Controls to establish and maintain baseline configurations and inventories of organizational systems throughout their system development life cycles.",
            "sort_order": 4,
            "requirements": [
                {
                    "code": "CMMC-CM.L2-3.4.1",
                    "title": "System Baselining",
                    "description": "Establish and maintain baseline configurations and inventories of organizational systems (including hardware, software, firmware, and documentation) throughout the respective system development life cycles.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CMMC-CM.L2-3.4.1a", "title": "Baseline configurations and inventories are maintained", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-CM.L2-3.4.2",
                    "title": "Security Configuration Enforcement",
                    "description": "Establish and enforce security configuration settings for information technology products employed in organizational systems.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CMMC-CM.L2-3.4.2a", "title": "Security configuration settings are enforced", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-CM.L2-3.4.3",
                    "title": "System Change Management",
                    "description": "Track, review, approve or disapprove, and log changes to organizational systems.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CMMC-CM.L2-3.4.3a", "title": "System changes are tracked and approved", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-CM.L2-3.4.6",
                    "title": "Least Functionality",
                    "description": "Employ the principle of least functionality by configuring organizational systems to provide only essential capabilities.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CMMC-CM.L2-3.4.6a", "title": "Systems are configured for least functionality", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CMMC-IA",
            "name": "Identification and Authentication",
            "description": "Controls to identify and authenticate users, processes acting on behalf of users, and devices before allowing access to organizational systems.",
            "sort_order": 5,
            "requirements": [
                {
                    "code": "CMMC-IA.L1-3.5.1",
                    "title": "Identification",
                    "description": "Identify information system users, processes acting on behalf of users, or devices.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CMMC-IA.L1-3.5.1a", "title": "System users and devices are identified", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-IA.L1-3.5.2",
                    "title": "Authentication",
                    "description": "Authenticate (or verify) the identities of those users, processes, or devices, as a prerequisite to allowing access to organizational information systems.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CMMC-IA.L1-3.5.2a", "title": "User authentication is enforced before access", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-IA.L2-3.5.3",
                    "title": "Multi-Factor Authentication",
                    "description": "Use multifactor authentication for local and network access to privileged accounts and for network access to non-privileged accounts.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CMMC-IA.L2-3.5.3a", "title": "MFA is enforced for privileged and network access", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-IA.L2-3.5.10",
                    "title": "Cryptographically-Protected Passwords",
                    "description": "Store and transmit only cryptographically-protected passwords.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CMMC-IA.L2-3.5.10a", "title": "Passwords are cryptographically protected", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CMMC-IR",
            "name": "Incident Response",
            "description": "Controls to establish an operational incident-handling capability including preparation, detection, analysis, containment, recovery, and user response activities.",
            "sort_order": 6,
            "requirements": [
                {
                    "code": "CMMC-IR.L2-3.6.1",
                    "title": "Incident Handling",
                    "description": "Establish an operational incident-handling capability for organizational systems that includes preparation, detection, analysis, containment, recovery, and user response activities.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CMMC-IR.L2-3.6.1a", "title": "Incident handling capability is operational", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-IR.L2-3.6.2",
                    "title": "Incident Reporting",
                    "description": "Track, document, and report incidents to designated officials and/or authorities both internal and external to the organization, including the DoD as required.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CMMC-IR.L2-3.6.2a", "title": "Incidents are reported to designated officials and DoD", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-IR.L2-3.6.3",
                    "title": "Incident Response Testing",
                    "description": "Test the organizational incident response capability.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CMMC-IR.L2-3.6.3a", "title": "Incident response capability is tested", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CMMC-MA",
            "name": "Maintenance",
            "description": "Controls for performing timely maintenance on organizational systems and controlling maintenance tools and remote maintenance activities.",
            "sort_order": 7,
            "requirements": [
                {
                    "code": "CMMC-MA.L2-3.7.1",
                    "title": "System Maintenance",
                    "description": "Perform maintenance on organizational systems.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CMMC-MA.L2-3.7.1a", "title": "System maintenance is performed and documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-MA.L2-3.7.2",
                    "title": "Maintenance Tool Control",
                    "description": "Provide effective controls on the tools, techniques, mechanisms, and personnel used to conduct system maintenance.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CMMC-MA.L2-3.7.2a", "title": "Maintenance tools are controlled", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-MA.L2-3.7.5",
                    "title": "Nonlocal Maintenance",
                    "description": "Require multifactor authentication to establish nonlocal maintenance sessions via external network connections and terminate such connections when nonlocal maintenance is complete.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CMMC-MA.L2-3.7.5a", "title": "Nonlocal maintenance requires MFA and session termination", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CMMC-MP",
            "name": "Media Protection",
            "description": "Controls to protect, sanitize, and control system media containing CUI, including both paper and digital media.",
            "sort_order": 8,
            "requirements": [
                {
                    "code": "CMMC-MP.L1-3.8.3",
                    "title": "Media Disposal",
                    "description": "Sanitize or destroy information system media containing Federal Contract Information before disposal or release for reuse.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CMMC-MP.L1-3.8.3a", "title": "FCI/CUI media is sanitized before disposal", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-MP.L2-3.8.1",
                    "title": "Media Protection",
                    "description": "Protect (i.e., physically control and securely store) system media containing CUI, both paper and digital.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CMMC-MP.L2-3.8.1a", "title": "CUI media is physically controlled and stored securely", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-MP.L2-3.8.6",
                    "title": "Portable Storage Encryption",
                    "description": "Implement cryptographic mechanisms to protect the confidentiality of CUI stored on digital media during transport unless otherwise protected by alternative physical safeguards.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CMMC-MP.L2-3.8.6a", "title": "Portable storage with CUI is encrypted", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CMMC-PS",
            "name": "Personnel Security",
            "description": "Controls to screen individuals prior to authorizing access to systems containing CUI and to protect CUI during and after personnel actions.",
            "sort_order": 9,
            "requirements": [
                {
                    "code": "CMMC-PS.L2-3.9.1",
                    "title": "Screen Individuals",
                    "description": "Screen individuals prior to authorizing access to organizational systems containing CUI.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CMMC-PS.L2-3.9.1a", "title": "Personnel screening is completed before CUI access", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-PS.L2-3.9.2",
                    "title": "Personnel Actions",
                    "description": "Ensure that organizational systems containing CUI are protected during and after personnel actions such as terminations and transfers.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CMMC-PS.L2-3.9.2a", "title": "CUI is protected during personnel transitions", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CMMC-PE",
            "name": "Physical Protection",
            "description": "Controls to limit physical access to organizational systems, equipment, and operating environments to authorized individuals.",
            "sort_order": 10,
            "requirements": [
                {
                    "code": "CMMC-PE.L1-3.10.1",
                    "title": "Limit Physical Access",
                    "description": "Limit physical access to organizational information systems, equipment, and the respective operating environments to authorized individuals.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CMMC-PE.L1-3.10.1a", "title": "Physical access is limited to authorized individuals", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-PE.L1-3.10.3",
                    "title": "Escort Visitors",
                    "description": "Escort visitors and monitor visitor activity.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CMMC-PE.L1-3.10.3a", "title": "Visitors are escorted and their activity is monitored", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-PE.L1-3.10.5",
                    "title": "Manage Physical Access",
                    "description": "Manage physical access devices.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CMMC-PE.L1-3.10.5a", "title": "Physical access devices are managed", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-PE.L2-3.10.2",
                    "title": "Monitor Physical Facility",
                    "description": "Protect and monitor the physical facility and support infrastructure for organizational systems.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CMMC-PE.L2-3.10.2a", "title": "Physical facility is monitored continuously", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CMMC-RA",
            "name": "Risk Assessment",
            "description": "Controls for periodically assessing the risk to organizational operations, assets, and individuals resulting from the operation of organizational systems and the associated processing, storage, or transmission of CUI.",
            "sort_order": 11,
            "requirements": [
                {
                    "code": "CMMC-RA.L2-3.11.1",
                    "title": "Risk Assessments",
                    "description": "Periodically assess the risk to organizational operations, organizational assets, and individuals, resulting from the operation of organizational systems and the associated processing, storage, or transmission of CUI.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CMMC-RA.L2-3.11.1a", "title": "Periodic risk assessments are conducted", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-RA.L2-3.11.2",
                    "title": "Vulnerability Scanning",
                    "description": "Scan for vulnerabilities in organizational systems and applications periodically and when new vulnerabilities affecting those systems and applications are identified.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CMMC-RA.L2-3.11.2a", "title": "Vulnerability scanning is performed periodically", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-RA.L2-3.11.3",
                    "title": "Vulnerability Remediation",
                    "description": "Remediate vulnerabilities in accordance with risk assessments.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CMMC-RA.L2-3.11.3a", "title": "Vulnerabilities are remediated based on risk", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CMMC-CA",
            "name": "Security Assessment",
            "description": "Controls for periodically assessing security controls, developing plans of action, and implementing continuous monitoring to ensure effectiveness of controls protecting CUI.",
            "sort_order": 12,
            "requirements": [
                {
                    "code": "CMMC-CA.L2-3.12.1",
                    "title": "Security Control Assessment",
                    "description": "Periodically assess the security controls in organizational systems to determine if the controls are effective in their application.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CMMC-CA.L2-3.12.1a", "title": "Security controls are periodically assessed", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-CA.L2-3.12.2",
                    "title": "Plan of Action",
                    "description": "Develop and implement plans of action designed to correct deficiencies and reduce or eliminate vulnerabilities in organizational systems.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CMMC-CA.L2-3.12.2a", "title": "Plans of action are developed for identified deficiencies", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-CA.L2-3.12.4",
                    "title": "System Security Plan",
                    "description": "Develop, document, and periodically update system security plans that describe system boundaries, system environments of operation, how security requirements are implemented, and the relationships with or connections to other systems.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CMMC-CA.L2-3.12.4a", "title": "System security plan is documented and maintained", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CMMC-SC",
            "name": "System and Communications Protection",
            "description": "Controls for monitoring, controlling, and protecting communications at external and internal boundaries of organizational systems, and employing architectural designs and cryptographic mechanisms.",
            "sort_order": 13,
            "requirements": [
                {
                    "code": "CMMC-SC.L1-3.13.1",
                    "title": "Boundary Protection",
                    "description": "Monitor, control, and protect communications (i.e., information transmitted or received by organizational systems) at the external boundaries and key internal boundaries of organizational systems.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CMMC-SC.L1-3.13.1a", "title": "Boundary protection monitors and controls communications", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-SC.L1-3.13.5",
                    "title": "Public-Access System Separation",
                    "description": "Implement subnetworks for publicly accessible system components that are physically or logically separated from internal networks.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CMMC-SC.L1-3.13.5a", "title": "Public-access systems are separated from internal networks", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-SC.L2-3.13.8",
                    "title": "Data in Transit Encryption",
                    "description": "Implement cryptographic mechanisms to prevent unauthorized disclosure of CUI during transmission unless otherwise protected by alternative physical safeguards.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CMMC-SC.L2-3.13.8a", "title": "CUI is encrypted during transmission", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-SC.L2-3.13.11",
                    "title": "FIPS-Validated Cryptography",
                    "description": "Employ FIPS-validated cryptography when used to protect the confidentiality of CUI.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CMMC-SC.L2-3.13.11a", "title": "FIPS-validated cryptography is used for CUI", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-SC.L2-3.13.16",
                    "title": "Data at Rest Protection",
                    "description": "Protect the confidentiality of CUI at rest.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "CMMC-SC.L2-3.13.16a", "title": "CUI at rest is protected", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CMMC-SI",
            "name": "System and Information Integrity",
            "description": "Controls for identifying, reporting, and correcting system flaws in a timely manner, providing malicious code protection, and monitoring system security alerts and advisories.",
            "sort_order": 14,
            "requirements": [
                {
                    "code": "CMMC-SI.L1-3.14.1",
                    "title": "Flaw Remediation",
                    "description": "Identify, report, and correct information and information system flaws in a timely manner.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CMMC-SI.L1-3.14.1a", "title": "System flaws are identified and corrected timely", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-SI.L1-3.14.2",
                    "title": "Malicious Code Protection",
                    "description": "Provide protection from malicious code at appropriate locations within organizational information systems.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CMMC-SI.L1-3.14.2a", "title": "Malicious code protection is deployed", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-SI.L1-3.14.4",
                    "title": "Update Malicious Code Protection",
                    "description": "Update malicious code protection mechanisms when new releases are available.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CMMC-SI.L1-3.14.4a", "title": "Malware signatures are kept current", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-SI.L2-3.14.3",
                    "title": "Security Alerts and Advisories",
                    "description": "Monitor system security alerts and advisories and take action in response.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CMMC-SI.L2-3.14.3a", "title": "Security alerts are monitored and actioned", "sort_order": 1},
                    ],
                },
                {
                    "code": "CMMC-SI.L2-3.14.6",
                    "title": "System Monitoring",
                    "description": "Monitor organizational systems, including inbound and outbound communications traffic, to detect attacks and indicators of potential attacks.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "CMMC-SI.L2-3.14.6a", "title": "System monitoring detects attacks and indicators", "sort_order": 1},
                    ],
                },
            ],
        },
    ],
}


async def seed_cmmc_framework(db):
    """Seed the CMMC 2.0 framework."""
    from sqlalchemy import select
    from app.models.framework import Framework
    from app.models.framework_domain import FrameworkDomain
    from app.models.framework_requirement import FrameworkRequirement
    from app.models.control_objective import ControlObjective

    # Check if already seeded
    existing = await db.execute(
        select(Framework).where(Framework.name == CMMC_FRAMEWORK["name"])
    )
    if existing.scalar_one_or_none():
        print("  -> CMMC 2.0 framework already seeded, skipping.")
        return

    fw_data = CMMC_FRAMEWORK
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
    print(f"  Seeded CMMC 2.0: {req_count} requirements, {obj_count} objectives.")
    return framework
