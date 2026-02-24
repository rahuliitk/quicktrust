"""NIST 800-53 Rev 5 — Security and Privacy Controls for Information Systems — framework seed data."""

NIST_800_53_FRAMEWORK = {
    "name": "NIST 800-53",
    "version": "Rev 5",
    "category": "Security & Compliance",
    "description": "NIST Special Publication 800-53 Revision 5 — Security and Privacy Controls for Information Systems and Organizations. Provides a comprehensive catalog of security and privacy controls for federal information systems.",
    "domains": [
        {
            "code": "AC",
            "name": "Access Control",
            "description": "Controls for managing access to information systems and data, including account management, access enforcement, separation of duties, and least privilege.",
            "sort_order": 1,
            "requirements": [
                {
                    "code": "AC-1",
                    "title": "Policy and Procedures",
                    "description": "Develop, document, and disseminate an access control policy and procedures that address purpose, scope, roles, responsibilities, management commitment, coordination, and compliance.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "AC-1a", "title": "Access control policy is developed and documented", "sort_order": 1},
                        {"code": "AC-1b", "title": "Access control procedures are reviewed and updated", "sort_order": 2},
                    ],
                },
                {
                    "code": "AC-2",
                    "title": "Account Management",
                    "description": "Define and document account types, establish conditions for group and role membership, assign account managers, and require approvals for account creation requests.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "AC-2a", "title": "Account types are defined and documented", "sort_order": 1},
                        {"code": "AC-2b", "title": "Account managers are assigned", "sort_order": 2},
                        {"code": "AC-2c", "title": "Inactive accounts are disabled within defined time period", "sort_order": 3},
                    ],
                },
                {
                    "code": "AC-3",
                    "title": "Access Enforcement",
                    "description": "Enforce approved authorizations for logical access to information and system resources in accordance with applicable access control policies.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "AC-3a", "title": "Access enforcement mechanisms are implemented", "sort_order": 1},
                    ],
                },
                {
                    "code": "AC-5",
                    "title": "Separation of Duties",
                    "description": "Identify and document duties of individuals requiring separation, and define system access authorizations to support separation of duties.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "AC-5a", "title": "Duties requiring separation are identified", "sort_order": 1},
                        {"code": "AC-5b", "title": "Access authorizations enforce separation of duties", "sort_order": 2},
                    ],
                },
                {
                    "code": "AC-6",
                    "title": "Least Privilege",
                    "description": "Employ the principle of least privilege, allowing only authorized accesses for users and processes that are necessary to accomplish assigned organizational tasks.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "AC-6a", "title": "Least privilege is enforced for all users and processes", "sort_order": 1},
                        {"code": "AC-6b", "title": "Privileged accounts are restricted and monitored", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "AT",
            "name": "Awareness and Training",
            "description": "Controls for ensuring personnel are adequately trained and aware of security and privacy policies, procedures, and their responsibilities.",
            "sort_order": 2,
            "requirements": [
                {
                    "code": "AT-1",
                    "title": "Policy and Procedures",
                    "description": "Develop, document, and disseminate an awareness and training policy that addresses purpose, scope, roles, responsibilities, and compliance.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "AT-1a", "title": "Security awareness and training policy is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "AT-2",
                    "title": "Literacy Training and Awareness",
                    "description": "Provide security and privacy literacy training to system users as part of initial training and at least annually thereafter, including recognizing and reporting indicators of insider threat.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "AT-2a", "title": "Security awareness training is provided to all users", "sort_order": 1},
                        {"code": "AT-2b", "title": "Training includes social engineering and insider threat awareness", "sort_order": 2},
                    ],
                },
                {
                    "code": "AT-3",
                    "title": "Role-Based Training",
                    "description": "Provide role-based security and privacy training to personnel with assigned security roles and responsibilities before authorizing access and at defined frequency thereafter.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "AT-3a", "title": "Role-based security training is delivered before access is granted", "sort_order": 1},
                        {"code": "AT-3b", "title": "Training records are maintained", "sort_order": 2},
                    ],
                },
                {
                    "code": "AT-4",
                    "title": "Training Records",
                    "description": "Document and monitor security and privacy training activities, including basic security and privacy awareness training and role-based training.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "AT-4a", "title": "Training completion records are documented and retained", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "AU",
            "name": "Audit and Accountability",
            "description": "Controls for creating, protecting, and retaining audit records to enable monitoring, analysis, investigation, and reporting of unauthorized activity.",
            "sort_order": 3,
            "requirements": [
                {
                    "code": "AU-1",
                    "title": "Policy and Procedures",
                    "description": "Develop, document, and disseminate an audit and accountability policy that addresses purpose, scope, roles, responsibilities, and compliance.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "AU-1a", "title": "Audit and accountability policy is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "AU-2",
                    "title": "Event Logging",
                    "description": "Identify the types of events that the system is capable of logging in support of the audit function and coordinate the event logging function with other organizations.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "AU-2a", "title": "Auditable events are identified and documented", "sort_order": 1},
                        {"code": "AU-2b", "title": "Event logging is coordinated across the organization", "sort_order": 2},
                    ],
                },
                {
                    "code": "AU-3",
                    "title": "Content of Audit Records",
                    "description": "Ensure that audit records contain information that establishes the type of event, when and where the event occurred, the source, and the outcome of the event.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "AU-3a", "title": "Audit records contain sufficient detail for forensic analysis", "sort_order": 1},
                    ],
                },
                {
                    "code": "AU-6",
                    "title": "Audit Record Review, Analysis, and Reporting",
                    "description": "Review and analyze system audit records for indications of inappropriate or unusual activity and report findings to designated organizational officials.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "AU-6a", "title": "Audit records are reviewed and analyzed regularly", "sort_order": 1},
                        {"code": "AU-6b", "title": "Findings from audit analysis are reported", "sort_order": 2},
                    ],
                },
                {
                    "code": "AU-9",
                    "title": "Protection of Audit Information",
                    "description": "Protect audit information and audit logging tools from unauthorized access, modification, and deletion.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "AU-9a", "title": "Audit logs are protected from unauthorized modification", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CA",
            "name": "Assessment, Authorization, and Monitoring",
            "description": "Controls for assessing security and privacy controls, authorizing systems for operation, and monitoring controls on an ongoing basis.",
            "sort_order": 4,
            "requirements": [
                {
                    "code": "CA-1",
                    "title": "Policy and Procedures",
                    "description": "Develop, document, and disseminate a security assessment and authorization policy that addresses purpose, scope, roles, responsibilities, and compliance.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CA-1a", "title": "Assessment and authorization policy is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "CA-2",
                    "title": "Control Assessments",
                    "description": "Develop a control assessment plan, assess the controls in the system at a defined frequency, produce an assessment report, and provide results to designated officials.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CA-2a", "title": "Security control assessment plan is developed", "sort_order": 1},
                        {"code": "CA-2b", "title": "Control assessments are conducted at defined frequency", "sort_order": 2},
                    ],
                },
                {
                    "code": "CA-5",
                    "title": "Plan of Action and Milestones",
                    "description": "Develop a plan of action and milestones for the system to document planned remediation actions and update it based on findings from control assessments and audits.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CA-5a", "title": "POA&M is developed and maintained", "sort_order": 1},
                        {"code": "CA-5b", "title": "POA&M is updated based on assessment findings", "sort_order": 2},
                    ],
                },
                {
                    "code": "CA-7",
                    "title": "Continuous Monitoring",
                    "description": "Develop a continuous monitoring strategy and implement a continuous monitoring program that includes ongoing assessment of control effectiveness.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CA-7a", "title": "Continuous monitoring strategy is developed", "sort_order": 1},
                        {"code": "CA-7b", "title": "Continuous monitoring program is operational", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "CM",
            "name": "Configuration Management",
            "description": "Controls for establishing and maintaining baseline configurations and inventories of systems, and managing changes to those configurations.",
            "sort_order": 5,
            "requirements": [
                {
                    "code": "CM-1",
                    "title": "Policy and Procedures",
                    "description": "Develop, document, and disseminate a configuration management policy that addresses purpose, scope, roles, responsibilities, and compliance.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CM-1a", "title": "Configuration management policy is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "CM-2",
                    "title": "Baseline Configuration",
                    "description": "Develop, document, and maintain a current baseline configuration of the system under configuration control.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CM-2a", "title": "Baseline configurations are documented and maintained", "sort_order": 1},
                    ],
                },
                {
                    "code": "CM-3",
                    "title": "Configuration Change Control",
                    "description": "Determine and document the types of changes to the system that are configuration-controlled and employ a formal change control process.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CM-3a", "title": "Configuration-controlled changes are identified", "sort_order": 1},
                        {"code": "CM-3b", "title": "Changes are approved through formal change control", "sort_order": 2},
                    ],
                },
                {
                    "code": "CM-6",
                    "title": "Configuration Settings",
                    "description": "Establish and document configuration settings for components employed within the system that reflect the most restrictive mode consistent with operational requirements.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CM-6a", "title": "Secure configuration settings are documented and enforced", "sort_order": 1},
                    ],
                },
                {
                    "code": "CM-8",
                    "title": "System Component Inventory",
                    "description": "Develop and document an inventory of system components that accurately reflects the system, is consistent with the authorization boundary, and is at the level of granularity necessary for tracking.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "CM-8a", "title": "System component inventory is maintained and accurate", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CP",
            "name": "Contingency Planning",
            "description": "Controls for establishing, maintaining, and implementing plans for emergency response, backup operations, and post-disaster recovery of information systems.",
            "sort_order": 6,
            "requirements": [
                {
                    "code": "CP-1",
                    "title": "Policy and Procedures",
                    "description": "Develop, document, and disseminate a contingency planning policy that addresses purpose, scope, roles, responsibilities, and compliance.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CP-1a", "title": "Contingency planning policy is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "CP-2",
                    "title": "Contingency Plan",
                    "description": "Develop a contingency plan that identifies essential mission and business functions, provides recovery objectives and reconstitution procedures, and is reviewed and approved.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CP-2a", "title": "Contingency plan is developed and approved", "sort_order": 1},
                        {"code": "CP-2b", "title": "Recovery objectives (RTO/RPO) are defined", "sort_order": 2},
                    ],
                },
                {
                    "code": "CP-4",
                    "title": "Contingency Plan Testing",
                    "description": "Test the contingency plan at a defined frequency using defined tests to determine the effectiveness of the plan and the readiness to execute the plan.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CP-4a", "title": "Contingency plan is tested at defined frequency", "sort_order": 1},
                        {"code": "CP-4b", "title": "Test results are reviewed and incorporated into plan updates", "sort_order": 2},
                    ],
                },
                {
                    "code": "CP-9",
                    "title": "System Backup",
                    "description": "Conduct backups of user-level and system-level information at defined frequency, protect backup information during storage, and transfer backup information to alternate storage site.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CP-9a", "title": "System and data backups are performed regularly", "sort_order": 1},
                        {"code": "CP-9b", "title": "Backup integrity is verified through restoration testing", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "IA",
            "name": "Identification and Authentication",
            "description": "Controls for identifying and authenticating users, devices, and processes before granting access to information systems.",
            "sort_order": 7,
            "requirements": [
                {
                    "code": "IA-1",
                    "title": "Policy and Procedures",
                    "description": "Develop, document, and disseminate an identification and authentication policy that addresses purpose, scope, roles, responsibilities, and compliance.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "IA-1a", "title": "Identification and authentication policy is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "IA-2",
                    "title": "Identification and Authentication (Organizational Users)",
                    "description": "Uniquely identify and authenticate organizational users and associate that unique identification with processes acting on behalf of those users.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "IA-2a", "title": "Organizational users are uniquely identified and authenticated", "sort_order": 1},
                        {"code": "IA-2b", "title": "Multi-factor authentication is implemented for privileged accounts", "sort_order": 2},
                    ],
                },
                {
                    "code": "IA-4",
                    "title": "Identifier Management",
                    "description": "Manage system identifiers by receiving authorization to assign an identifier, selecting and assigning an identifier, preventing reuse, and disabling identifiers after defined period of inactivity.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "IA-4a", "title": "Identifier lifecycle is managed", "sort_order": 1},
                    ],
                },
                {
                    "code": "IA-5",
                    "title": "Authenticator Management",
                    "description": "Manage system authenticators by verifying identity before distributing authenticators, establishing initial authenticator content, and ensuring authenticators have sufficient strength.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "IA-5a", "title": "Authenticator strength requirements are enforced", "sort_order": 1},
                        {"code": "IA-5b", "title": "Default authenticators are changed upon installation", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "IR",
            "name": "Incident Response",
            "description": "Controls for establishing an operational incident handling capability for the organization, including preparation, detection, analysis, containment, recovery, and user response activities.",
            "sort_order": 8,
            "requirements": [
                {
                    "code": "IR-1",
                    "title": "Policy and Procedures",
                    "description": "Develop, document, and disseminate an incident response policy that addresses purpose, scope, roles, responsibilities, and compliance.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "IR-1a", "title": "Incident response policy is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "IR-2",
                    "title": "Incident Response Training",
                    "description": "Provide incident response training to system users consistent with assigned roles and responsibilities within a defined time period of assuming an incident response role.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "IR-2a", "title": "Incident response training is provided to designated personnel", "sort_order": 1},
                    ],
                },
                {
                    "code": "IR-4",
                    "title": "Incident Handling",
                    "description": "Implement an incident handling capability that includes preparation, detection and analysis, containment, eradication, and recovery.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "IR-4a", "title": "Incident handling procedures cover full incident lifecycle", "sort_order": 1},
                        {"code": "IR-4b", "title": "Incidents are correlated for trending and analysis", "sort_order": 2},
                    ],
                },
                {
                    "code": "IR-5",
                    "title": "Incident Monitoring",
                    "description": "Track and document system security and privacy incidents on an ongoing basis.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "IR-5a", "title": "Incidents are tracked and documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "IR-6",
                    "title": "Incident Reporting",
                    "description": "Require personnel to report suspected incidents to the organizational incident response capability within a defined time period.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "IR-6a", "title": "Incident reporting procedures and timelines are defined", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "MA",
            "name": "Maintenance",
            "description": "Controls for performing maintenance on information systems, including controlled maintenance, maintenance tools, and remote maintenance.",
            "sort_order": 9,
            "requirements": [
                {
                    "code": "MA-1",
                    "title": "Policy and Procedures",
                    "description": "Develop, document, and disseminate a system maintenance policy that addresses purpose, scope, roles, responsibilities, and compliance.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "MA-1a", "title": "System maintenance policy is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "MA-2",
                    "title": "Controlled Maintenance",
                    "description": "Schedule, document, and review records of maintenance and repairs on system components in accordance with manufacturer specifications and organizational requirements.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "MA-2a", "title": "Maintenance activities are scheduled and documented", "sort_order": 1},
                        {"code": "MA-2b", "title": "Maintenance records are reviewed", "sort_order": 2},
                    ],
                },
                {
                    "code": "MA-4",
                    "title": "Nonlocal Maintenance",
                    "description": "Approve and monitor nonlocal maintenance and diagnostic activities, and terminate sessions and network connections when nonlocal maintenance is completed.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "MA-4a", "title": "Nonlocal maintenance is approved and monitored", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "MP",
            "name": "Media Protection",
            "description": "Controls for protecting system media, both paper and digital, including access, marking, storage, transport, sanitization, and use.",
            "sort_order": 10,
            "requirements": [
                {
                    "code": "MP-1",
                    "title": "Policy and Procedures",
                    "description": "Develop, document, and disseminate a media protection policy that addresses purpose, scope, roles, responsibilities, and compliance.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "MP-1a", "title": "Media protection policy is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "MP-2",
                    "title": "Media Access",
                    "description": "Restrict access to digital and non-digital media to authorized individuals using defined security controls.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "MP-2a", "title": "Media access is restricted to authorized individuals", "sort_order": 1},
                    ],
                },
                {
                    "code": "MP-6",
                    "title": "Media Sanitization",
                    "description": "Sanitize system media prior to disposal, release out of organizational control, or release for reuse using defined sanitization techniques.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "MP-6a", "title": "Media sanitization procedures are implemented", "sort_order": 1},
                        {"code": "MP-6b", "title": "Sanitization records are maintained", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "PE",
            "name": "Physical and Environmental Protection",
            "description": "Controls for protecting the physical facility and the environment in which systems operate, including physical access, monitoring, and environmental controls.",
            "sort_order": 11,
            "requirements": [
                {
                    "code": "PE-1",
                    "title": "Policy and Procedures",
                    "description": "Develop, document, and disseminate a physical and environmental protection policy that addresses purpose, scope, roles, responsibilities, and compliance.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "PE-1a", "title": "Physical and environmental protection policy is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "PE-2",
                    "title": "Physical Access Authorizations",
                    "description": "Develop, approve, and maintain a list of individuals with authorized access to the facility and issue authorization credentials.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "PE-2a", "title": "Physical access authorization list is maintained", "sort_order": 1},
                    ],
                },
                {
                    "code": "PE-3",
                    "title": "Physical Access Control",
                    "description": "Enforce physical access authorizations at defined entry and exit points to the facility, maintain physical access audit logs, and control access to areas designated as publicly accessible.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "PE-3a", "title": "Physical access controls are enforced at entry/exit points", "sort_order": 1},
                        {"code": "PE-3b", "title": "Physical access logs are maintained", "sort_order": 2},
                    ],
                },
                {
                    "code": "PE-6",
                    "title": "Monitoring Physical Access",
                    "description": "Monitor physical access to the facility where the system resides to detect and respond to physical security incidents.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "PE-6a", "title": "Physical access monitoring is operational", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "PL",
            "name": "Planning",
            "description": "Controls for developing security and privacy plans, rules of behavior, and information architecture for systems.",
            "sort_order": 12,
            "requirements": [
                {
                    "code": "PL-1",
                    "title": "Policy and Procedures",
                    "description": "Develop, document, and disseminate a planning policy that addresses purpose, scope, roles, responsibilities, and compliance.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "PL-1a", "title": "Security planning policy is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "PL-2",
                    "title": "System Security and Privacy Plans",
                    "description": "Develop security and privacy plans for the system that are consistent with the organization's enterprise architecture and reviewed and approved by the authorizing official.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "PL-2a", "title": "System security plan is developed and approved", "sort_order": 1},
                        {"code": "PL-2b", "title": "Security plan is reviewed and updated regularly", "sort_order": 2},
                    ],
                },
                {
                    "code": "PL-4",
                    "title": "Rules of Behavior",
                    "description": "Establish and provide to individuals requiring access to the system, the rules that describe their responsibilities and expected behavior for information and system usage.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "PL-4a", "title": "Rules of behavior are established and acknowledged by users", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "PM",
            "name": "Program Management",
            "description": "Controls for managing the information security and privacy program at the organizational level, including risk management strategy, enterprise architecture, and critical infrastructure plan.",
            "sort_order": 13,
            "requirements": [
                {
                    "code": "PM-1",
                    "title": "Information Security Program Plan",
                    "description": "Develop and disseminate an organization-wide information security program plan that provides an overview of the requirements for the security program.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "PM-1a", "title": "Information security program plan is developed and disseminated", "sort_order": 1},
                    ],
                },
                {
                    "code": "PM-9",
                    "title": "Risk Management Strategy",
                    "description": "Develop a comprehensive strategy to manage risk to organizational operations, assets, individuals, and other organizations.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "PM-9a", "title": "Risk management strategy is developed and implemented", "sort_order": 1},
                    ],
                },
                {
                    "code": "PM-10",
                    "title": "Authorization Process",
                    "description": "Manage the security and privacy state of organizational systems through authorization processes, including designation of risk-executive functions.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "PM-10a", "title": "System authorization process is established", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "PS",
            "name": "Personnel Security",
            "description": "Controls for ensuring the trustworthiness of personnel with access to information systems, including screening, termination, transfer, and access agreements.",
            "sort_order": 14,
            "requirements": [
                {
                    "code": "PS-1",
                    "title": "Policy and Procedures",
                    "description": "Develop, document, and disseminate a personnel security policy that addresses purpose, scope, roles, responsibilities, and compliance.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "PS-1a", "title": "Personnel security policy is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "PS-3",
                    "title": "Personnel Screening",
                    "description": "Screen individuals prior to authorizing access to the system and rescreen individuals at a defined frequency.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "PS-3a", "title": "Personnel screening is conducted before access is granted", "sort_order": 1},
                    ],
                },
                {
                    "code": "PS-4",
                    "title": "Personnel Termination",
                    "description": "Upon termination of individual employment, disable system access within defined time period, terminate or revoke authenticators, and retrieve all organizational information system-related property.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "PS-4a", "title": "Access is disabled upon termination within defined timeframe", "sort_order": 1},
                        {"code": "PS-4b", "title": "Organizational property is retrieved upon termination", "sort_order": 2},
                    ],
                },
                {
                    "code": "PS-5",
                    "title": "Personnel Transfer",
                    "description": "Review and confirm ongoing operational need for current logical and physical access authorizations when individuals are reassigned or transferred.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "PS-5a", "title": "Access authorizations are reviewed during personnel transfers", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "RA",
            "name": "Risk Assessment",
            "description": "Controls for assessing risks to organizational operations, organizational assets, individuals, and other organizations resulting from the operation and use of systems.",
            "sort_order": 15,
            "requirements": [
                {
                    "code": "RA-1",
                    "title": "Policy and Procedures",
                    "description": "Develop, document, and disseminate a risk assessment policy that addresses purpose, scope, roles, responsibilities, and compliance.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "RA-1a", "title": "Risk assessment policy is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "RA-3",
                    "title": "Risk Assessment",
                    "description": "Conduct a risk assessment to identify, estimate, and prioritize risks to organizational operations, assets, individuals, and other organizations resulting from the operation and use of the system.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "RA-3a", "title": "Risk assessment is conducted and documented", "sort_order": 1},
                        {"code": "RA-3b", "title": "Risk assessment results are reviewed by leadership", "sort_order": 2},
                    ],
                },
                {
                    "code": "RA-5",
                    "title": "Vulnerability Monitoring and Scanning",
                    "description": "Monitor and scan for vulnerabilities in the system and hosted applications at a defined frequency, and when new vulnerabilities potentially affecting the system are identified and reported.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "RA-5a", "title": "Vulnerability scanning is performed at defined frequency", "sort_order": 1},
                        {"code": "RA-5b", "title": "Vulnerabilities are remediated within defined timeframes", "sort_order": 2},
                    ],
                },
            ],
        },
        {
            "code": "SA",
            "name": "System and Services Acquisition",
            "description": "Controls for managing the system development life cycle, acquisition processes, and supply chain risk management.",
            "sort_order": 16,
            "requirements": [
                {
                    "code": "SA-1",
                    "title": "Policy and Procedures",
                    "description": "Develop, document, and disseminate a system and services acquisition policy that addresses purpose, scope, roles, responsibilities, and compliance.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "SA-1a", "title": "System and services acquisition policy is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "SA-3",
                    "title": "System Development Life Cycle",
                    "description": "Acquire, develop, and manage the system using a defined system development life cycle that incorporates information security and privacy considerations.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "SA-3a", "title": "SDLC incorporates security and privacy considerations", "sort_order": 1},
                    ],
                },
                {
                    "code": "SA-4",
                    "title": "Acquisition Process",
                    "description": "Include security and privacy functional requirements, strength requirements, assurance requirements, and documentation requirements in system acquisition contracts.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "SA-4a", "title": "Acquisition contracts include security requirements", "sort_order": 1},
                        {"code": "SA-4b", "title": "Third-party security assessments are required for acquisitions", "sort_order": 2},
                    ],
                },
                {
                    "code": "SA-9",
                    "title": "External System Services",
                    "description": "Require that providers of external system services comply with organizational security and privacy requirements and employ appropriate controls.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "SA-9a", "title": "External service providers comply with security requirements", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "SC",
            "name": "System and Communications Protection",
            "description": "Controls for protecting system communications including boundary protection, cryptographic protection, and denial-of-service protection.",
            "sort_order": 17,
            "requirements": [
                {
                    "code": "SC-1",
                    "title": "Policy and Procedures",
                    "description": "Develop, document, and disseminate a system and communications protection policy that addresses purpose, scope, roles, responsibilities, and compliance.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "SC-1a", "title": "System and communications protection policy is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "SC-7",
                    "title": "Boundary Protection",
                    "description": "Monitor and control communications at the external managed interfaces to the system and at key internal managed interfaces within the system.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "SC-7a", "title": "Boundary protection mechanisms are implemented", "sort_order": 1},
                        {"code": "SC-7b", "title": "External and internal boundary interfaces are monitored", "sort_order": 2},
                    ],
                },
                {
                    "code": "SC-8",
                    "title": "Transmission Confidentiality and Integrity",
                    "description": "Protect the confidentiality and integrity of transmitted information using cryptographic mechanisms.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "SC-8a", "title": "Data in transit is encrypted", "sort_order": 1},
                    ],
                },
                {
                    "code": "SC-12",
                    "title": "Cryptographic Key Establishment and Management",
                    "description": "Establish and manage cryptographic keys when cryptography is employed within the system in accordance with defined key management requirements.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "SC-12a", "title": "Cryptographic key management procedures are established", "sort_order": 1},
                    ],
                },
                {
                    "code": "SC-28",
                    "title": "Protection of Information at Rest",
                    "description": "Protect the confidentiality and integrity of information at rest using cryptographic mechanisms.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "SC-28a", "title": "Data at rest is encrypted", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "SI",
            "name": "System and Information Integrity",
            "description": "Controls for identifying, reporting, and correcting system flaws, providing protection from malicious code, and monitoring system security alerts.",
            "sort_order": 18,
            "requirements": [
                {
                    "code": "SI-1",
                    "title": "Policy and Procedures",
                    "description": "Develop, document, and disseminate a system and information integrity policy that addresses purpose, scope, roles, responsibilities, and compliance.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "SI-1a", "title": "System and information integrity policy is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "SI-2",
                    "title": "Flaw Remediation",
                    "description": "Identify, report, and correct system flaws, test software and firmware updates for effectiveness and potential side effects, and install security-relevant updates within defined time period.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "SI-2a", "title": "System flaws are identified and remediated", "sort_order": 1},
                        {"code": "SI-2b", "title": "Security patches are applied within defined timeframes", "sort_order": 2},
                    ],
                },
                {
                    "code": "SI-3",
                    "title": "Malicious Code Protection",
                    "description": "Implement malicious code protection mechanisms at system entry and exit points to detect and eradicate malicious code.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "SI-3a", "title": "Malicious code protection is deployed and updated", "sort_order": 1},
                    ],
                },
                {
                    "code": "SI-4",
                    "title": "System Monitoring",
                    "description": "Monitor the system to detect attacks and indicators of potential attacks, unauthorized local, network, and remote connections.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "SI-4a", "title": "System monitoring for attacks is operational", "sort_order": 1},
                        {"code": "SI-4b", "title": "Monitoring alerts are generated and reviewed", "sort_order": 2},
                    ],
                },
                {
                    "code": "SI-5",
                    "title": "Security Alerts, Advisories, and Directives",
                    "description": "Receive system security alerts, advisories, and directives from designated external organizations on an ongoing basis and generate internal alerts as deemed necessary.",
                    "sort_order": 5,
                    "objectives": [
                        {"code": "SI-5a", "title": "Security alerts and advisories are received and acted upon", "sort_order": 1},
                    ],
                },
            ],
        },
    ],
}


async def seed_nist_800_53_framework(db):
    """Seed the NIST 800-53 Rev 5 framework."""
    from sqlalchemy import select
    from app.models.framework import Framework
    from app.models.framework_domain import FrameworkDomain
    from app.models.framework_requirement import FrameworkRequirement
    from app.models.control_objective import ControlObjective

    # Check if already seeded
    existing = await db.execute(
        select(Framework).where(Framework.name == NIST_800_53_FRAMEWORK["name"])
    )
    if existing.scalar_one_or_none():
        print("  -> NIST 800-53 framework already seeded, skipping.")
        return

    fw_data = NIST_800_53_FRAMEWORK
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
    print(f"  Seeded NIST 800-53: {req_count} requirements, {obj_count} objectives.")
    return framework
