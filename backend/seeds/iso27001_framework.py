"""ISO 27001:2022 Annex A — framework seed data with 4 themes and 93 controls."""

ISO27001_FRAMEWORK = {
    "name": "ISO 27001",
    "version": "2022",
    "category": "Information Security",
    "description": "ISO/IEC 27001:2022 Annex A — Information security, cybersecurity, and privacy protection controls organized into 4 themes with 93 controls.",
    "domains": [
        {
            "code": "A.5",
            "name": "Organizational Controls",
            "description": "Organizational controls addressing policies, roles, responsibilities, and management of information security.",
            "sort_order": 1,
            "requirements": [
                {"code": "A.5.1", "title": "Policies for information security", "description": "Information security policy and topic-specific policies shall be defined, approved, published, communicated, and reviewed.", "sort_order": 1, "objectives": [
                    {"code": "A.5.1.1", "title": "Information security policy is approved and published", "sort_order": 1},
                ]},
                {"code": "A.5.2", "title": "Information security roles and responsibilities", "description": "Information security roles and responsibilities shall be defined and allocated.", "sort_order": 2, "objectives": [
                    {"code": "A.5.2.1", "title": "Security roles are defined and assigned", "sort_order": 1},
                ]},
                {"code": "A.5.3", "title": "Segregation of duties", "description": "Conflicting duties and areas of responsibility shall be segregated.", "sort_order": 3, "objectives": [
                    {"code": "A.5.3.1", "title": "Duty segregation is implemented", "sort_order": 1},
                ]},
                {"code": "A.5.4", "title": "Management responsibilities", "description": "Management shall require all personnel to apply information security in accordance with the established policy.", "sort_order": 4, "objectives": [
                    {"code": "A.5.4.1", "title": "Management enforces security policy compliance", "sort_order": 1},
                ]},
                {"code": "A.5.5", "title": "Contact with authorities", "description": "The organization shall establish and maintain contact with relevant authorities.", "sort_order": 5, "objectives": [
                    {"code": "A.5.5.1", "title": "Authority contact procedures are documented", "sort_order": 1},
                ]},
                {"code": "A.5.6", "title": "Contact with special interest groups", "description": "The organization shall establish and maintain contact with special interest groups or forums.", "sort_order": 6, "objectives": [
                    {"code": "A.5.6.1", "title": "Industry group memberships are maintained", "sort_order": 1},
                ]},
                {"code": "A.5.7", "title": "Threat intelligence", "description": "Information relating to information security threats shall be collected and analysed.", "sort_order": 7, "objectives": [
                    {"code": "A.5.7.1", "title": "Threat intelligence feeds are monitored", "sort_order": 1},
                ]},
                {"code": "A.5.8", "title": "Information security in project management", "description": "Information security shall be integrated into project management.", "sort_order": 8, "objectives": [
                    {"code": "A.5.8.1", "title": "Projects include security requirements", "sort_order": 1},
                ]},
                {"code": "A.5.9", "title": "Inventory of information and other associated assets", "description": "An inventory of information and other associated assets shall be developed and maintained.", "sort_order": 9, "objectives": [
                    {"code": "A.5.9.1", "title": "Asset inventory is maintained", "sort_order": 1},
                ]},
                {"code": "A.5.10", "title": "Acceptable use of information and other associated assets", "description": "Rules for the acceptable use of information and associated assets shall be identified, documented, and implemented.", "sort_order": 10, "objectives": [
                    {"code": "A.5.10.1", "title": "Acceptable use policy is documented", "sort_order": 1},
                ]},
                {"code": "A.5.11", "title": "Return of assets", "description": "Personnel shall return all organizational assets upon termination.", "sort_order": 11, "objectives": [
                    {"code": "A.5.11.1", "title": "Asset return process is enforced", "sort_order": 1},
                ]},
                {"code": "A.5.12", "title": "Classification of information", "description": "Information shall be classified according to information security needs.", "sort_order": 12, "objectives": [
                    {"code": "A.5.12.1", "title": "Data classification scheme is implemented", "sort_order": 1},
                ]},
                {"code": "A.5.13", "title": "Labelling of information", "description": "Procedures for information labelling shall be developed and implemented.", "sort_order": 13, "objectives": [
                    {"code": "A.5.13.1", "title": "Information labelling procedures exist", "sort_order": 1},
                ]},
                {"code": "A.5.14", "title": "Information transfer", "description": "Information transfer rules, procedures, or agreements shall be in place.", "sort_order": 14, "objectives": [
                    {"code": "A.5.14.1", "title": "Information transfer rules are defined", "sort_order": 1},
                ]},
                {"code": "A.5.15", "title": "Access control", "description": "Rules to control physical and logical access shall be established.", "sort_order": 15, "objectives": [
                    {"code": "A.5.15.1", "title": "Access control policy is defined", "sort_order": 1},
                ]},
                {"code": "A.5.16", "title": "Identity management", "description": "The full life cycle of identities shall be managed.", "sort_order": 16, "objectives": [
                    {"code": "A.5.16.1", "title": "Identity lifecycle management is implemented", "sort_order": 1},
                ]},
                {"code": "A.5.17", "title": "Authentication information", "description": "Allocation and management of authentication information shall be controlled.", "sort_order": 17, "objectives": [
                    {"code": "A.5.17.1", "title": "Authentication information is securely managed", "sort_order": 1},
                ]},
                {"code": "A.5.18", "title": "Access rights", "description": "Access rights shall be provisioned, reviewed, modified, and removed in accordance with policy.", "sort_order": 18, "objectives": [
                    {"code": "A.5.18.1", "title": "Access rights are managed per policy", "sort_order": 1},
                ]},
                {"code": "A.5.19", "title": "Information security in supplier relationships", "description": "Processes and procedures shall be defined to manage information security risks associated with suppliers.", "sort_order": 19, "objectives": [
                    {"code": "A.5.19.1", "title": "Supplier security requirements are defined", "sort_order": 1},
                ]},
                {"code": "A.5.20", "title": "Addressing information security within supplier agreements", "description": "Relevant information security requirements shall be established with each supplier.", "sort_order": 20, "objectives": [
                    {"code": "A.5.20.1", "title": "Supplier agreements include security clauses", "sort_order": 1},
                ]},
                {"code": "A.5.21", "title": "Managing information security in the ICT supply chain", "description": "Processes shall be defined for managing information security risks associated with ICT products and services supply chain.", "sort_order": 21, "objectives": [
                    {"code": "A.5.21.1", "title": "ICT supply chain risks are managed", "sort_order": 1},
                ]},
                {"code": "A.5.22", "title": "Monitoring, review and change management of supplier services", "description": "The organization shall regularly monitor, review, evaluate, and manage change in supplier information security practices.", "sort_order": 22, "objectives": [
                    {"code": "A.5.22.1", "title": "Supplier services are regularly reviewed", "sort_order": 1},
                ]},
                {"code": "A.5.23", "title": "Information security for use of cloud services", "description": "Processes for acquisition, use, management, and exit from cloud services shall be established.", "sort_order": 23, "objectives": [
                    {"code": "A.5.23.1", "title": "Cloud service security processes are defined", "sort_order": 1},
                ]},
                {"code": "A.5.24", "title": "Information security incident management planning and preparation", "description": "The organization shall plan and prepare for managing information security incidents.", "sort_order": 24, "objectives": [
                    {"code": "A.5.24.1", "title": "Incident management plan is established", "sort_order": 1},
                ]},
                {"code": "A.5.25", "title": "Assessment and decision on information security events", "description": "The organization shall assess information security events and decide if they are to be categorized as incidents.", "sort_order": 25, "objectives": [
                    {"code": "A.5.25.1", "title": "Security event assessment process exists", "sort_order": 1},
                ]},
                {"code": "A.5.26", "title": "Response to information security incidents", "description": "Information security incidents shall be responded to in accordance with the documented procedures.", "sort_order": 26, "objectives": [
                    {"code": "A.5.26.1", "title": "Incident response procedures are followed", "sort_order": 1},
                ]},
                {"code": "A.5.27", "title": "Learning from information security incidents", "description": "Knowledge gained from information security incidents shall be used to strengthen controls.", "sort_order": 27, "objectives": [
                    {"code": "A.5.27.1", "title": "Lessons learned are incorporated into controls", "sort_order": 1},
                ]},
                {"code": "A.5.28", "title": "Collection of evidence", "description": "The organization shall establish and implement procedures for the identification, collection, acquisition, and preservation of evidence.", "sort_order": 28, "objectives": [
                    {"code": "A.5.28.1", "title": "Evidence collection procedures exist", "sort_order": 1},
                ]},
                {"code": "A.5.29", "title": "Information security during disruption", "description": "The organization shall plan how to maintain information security at an appropriate level during disruption.", "sort_order": 29, "objectives": [
                    {"code": "A.5.29.1", "title": "Business continuity plans address security", "sort_order": 1},
                ]},
                {"code": "A.5.30", "title": "ICT readiness for business continuity", "description": "ICT readiness shall be planned, implemented, maintained, and tested based on business continuity objectives.", "sort_order": 30, "objectives": [
                    {"code": "A.5.30.1", "title": "ICT continuity plans are tested", "sort_order": 1},
                ]},
                {"code": "A.5.31", "title": "Legal, statutory, regulatory and contractual requirements", "description": "Legal, statutory, regulatory, and contractual requirements relevant to information security shall be identified.", "sort_order": 31, "objectives": [
                    {"code": "A.5.31.1", "title": "Compliance requirements are identified", "sort_order": 1},
                ]},
                {"code": "A.5.32", "title": "Intellectual property rights", "description": "The organization shall implement appropriate procedures to protect intellectual property rights.", "sort_order": 32, "objectives": [
                    {"code": "A.5.32.1", "title": "IP protection procedures are implemented", "sort_order": 1},
                ]},
                {"code": "A.5.33", "title": "Protection of records", "description": "Records shall be protected from loss, destruction, falsification, unauthorized access, and unauthorized release.", "sort_order": 33, "objectives": [
                    {"code": "A.5.33.1", "title": "Record protection controls are in place", "sort_order": 1},
                ]},
                {"code": "A.5.34", "title": "Privacy and protection of PII", "description": "The organization shall identify and meet the requirements regarding the preservation of privacy and protection of PII.", "sort_order": 34, "objectives": [
                    {"code": "A.5.34.1", "title": "PII protection requirements are met", "sort_order": 1},
                ]},
                {"code": "A.5.35", "title": "Independent review of information security", "description": "The organization's approach to managing information security shall be independently reviewed at planned intervals.", "sort_order": 35, "objectives": [
                    {"code": "A.5.35.1", "title": "Independent security reviews are conducted", "sort_order": 1},
                ]},
                {"code": "A.5.36", "title": "Compliance with policies, rules and standards for information security", "description": "Compliance with the organization's information security policy and standards shall be regularly reviewed.", "sort_order": 36, "objectives": [
                    {"code": "A.5.36.1", "title": "Policy compliance is regularly reviewed", "sort_order": 1},
                ]},
                {"code": "A.5.37", "title": "Documented operating procedures", "description": "Operating procedures for information processing facilities shall be documented and made available.", "sort_order": 37, "objectives": [
                    {"code": "A.5.37.1", "title": "Operating procedures are documented", "sort_order": 1},
                ]},
            ],
        },
        {
            "code": "A.6",
            "name": "People Controls",
            "description": "Controls related to people, including screening, terms of employment, awareness, and disciplinary processes.",
            "sort_order": 2,
            "requirements": [
                {"code": "A.6.1", "title": "Screening", "description": "Background verification checks on all candidates shall be carried out prior to joining the organization.", "sort_order": 1, "objectives": [
                    {"code": "A.6.1.1", "title": "Background checks are performed", "sort_order": 1},
                ]},
                {"code": "A.6.2", "title": "Terms and conditions of employment", "description": "Employment contractual agreements shall state the personnel's and the organization's responsibilities for information security.", "sort_order": 2, "objectives": [
                    {"code": "A.6.2.1", "title": "Employment contracts include security responsibilities", "sort_order": 1},
                ]},
                {"code": "A.6.3", "title": "Information security awareness, education and training", "description": "Personnel shall receive appropriate information security awareness education and training.", "sort_order": 3, "objectives": [
                    {"code": "A.6.3.1", "title": "Security awareness training is delivered", "sort_order": 1},
                ]},
                {"code": "A.6.4", "title": "Disciplinary process", "description": "A disciplinary process shall be formalized and communicated to take actions against personnel who have committed an information security policy violation.", "sort_order": 4, "objectives": [
                    {"code": "A.6.4.1", "title": "Disciplinary process for violations exists", "sort_order": 1},
                ]},
                {"code": "A.6.5", "title": "Responsibilities after termination or change of employment", "description": "Information security responsibilities that remain valid after termination or change of employment shall be defined and enforced.", "sort_order": 5, "objectives": [
                    {"code": "A.6.5.1", "title": "Post-employment security obligations are defined", "sort_order": 1},
                ]},
                {"code": "A.6.6", "title": "Confidentiality or non-disclosure agreements", "description": "Confidentiality or non-disclosure agreements reflecting the organization's needs for the protection of information shall be identified and regularly reviewed.", "sort_order": 6, "objectives": [
                    {"code": "A.6.6.1", "title": "NDAs are in place and reviewed", "sort_order": 1},
                ]},
                {"code": "A.6.7", "title": "Remote working", "description": "Security measures shall be implemented when personnel are working remotely.", "sort_order": 7, "objectives": [
                    {"code": "A.6.7.1", "title": "Remote working security measures exist", "sort_order": 1},
                ]},
                {"code": "A.6.8", "title": "Information security event reporting", "description": "The organization shall provide a mechanism for personnel to report observed or suspected information security events.", "sort_order": 8, "objectives": [
                    {"code": "A.6.8.1", "title": "Security event reporting mechanism exists", "sort_order": 1},
                ]},
            ],
        },
        {
            "code": "A.7",
            "name": "Physical Controls",
            "description": "Controls for physical security of premises, equipment, and physical media.",
            "sort_order": 3,
            "requirements": [
                {"code": "A.7.1", "title": "Physical security perimeters", "description": "Security perimeters shall be defined and used to protect areas that contain information and associated assets.", "sort_order": 1, "objectives": [
                    {"code": "A.7.1.1", "title": "Security perimeters are defined", "sort_order": 1},
                ]},
                {"code": "A.7.2", "title": "Physical entry", "description": "Secure areas shall be protected by appropriate entry controls.", "sort_order": 2, "objectives": [
                    {"code": "A.7.2.1", "title": "Physical entry controls are implemented", "sort_order": 1},
                ]},
                {"code": "A.7.3", "title": "Securing offices, rooms and facilities", "description": "Physical security for offices, rooms, and facilities shall be designed and implemented.", "sort_order": 3, "objectives": [
                    {"code": "A.7.3.1", "title": "Office security is implemented", "sort_order": 1},
                ]},
                {"code": "A.7.4", "title": "Physical security monitoring", "description": "Premises shall be continuously monitored for unauthorized physical access.", "sort_order": 4, "objectives": [
                    {"code": "A.7.4.1", "title": "Physical security monitoring is operational", "sort_order": 1},
                ]},
                {"code": "A.7.5", "title": "Protecting against physical and environmental threats", "description": "Protection against physical and environmental threats shall be designed and implemented.", "sort_order": 5, "objectives": [
                    {"code": "A.7.5.1", "title": "Environmental protections are in place", "sort_order": 1},
                ]},
                {"code": "A.7.6", "title": "Working in secure areas", "description": "Security measures for working in secure areas shall be designed and implemented.", "sort_order": 6, "objectives": [
                    {"code": "A.7.6.1", "title": "Secure area procedures are documented", "sort_order": 1},
                ]},
                {"code": "A.7.7", "title": "Clear desk and clear screen", "description": "Clear desk rules and clear screen rules shall be defined and enforced.", "sort_order": 7, "objectives": [
                    {"code": "A.7.7.1", "title": "Clear desk and screen policy is enforced", "sort_order": 1},
                ]},
                {"code": "A.7.8", "title": "Equipment siting and protection", "description": "Equipment shall be sited securely and protected.", "sort_order": 8, "objectives": [
                    {"code": "A.7.8.1", "title": "Equipment is securely sited", "sort_order": 1},
                ]},
                {"code": "A.7.9", "title": "Security of assets off-premises", "description": "Off-site assets shall be protected.", "sort_order": 9, "objectives": [
                    {"code": "A.7.9.1", "title": "Off-site asset protection is implemented", "sort_order": 1},
                ]},
                {"code": "A.7.10", "title": "Storage media", "description": "Storage media shall be managed through their life cycle.", "sort_order": 10, "objectives": [
                    {"code": "A.7.10.1", "title": "Media lifecycle management is implemented", "sort_order": 1},
                ]},
                {"code": "A.7.11", "title": "Supporting utilities", "description": "Information processing facilities shall be protected from power failures and other disruptions caused by failures in supporting utilities.", "sort_order": 11, "objectives": [
                    {"code": "A.7.11.1", "title": "Utility protections are in place", "sort_order": 1},
                ]},
                {"code": "A.7.12", "title": "Cabling security", "description": "Cables carrying power, data, or supporting information services shall be protected.", "sort_order": 12, "objectives": [
                    {"code": "A.7.12.1", "title": "Cabling is secured", "sort_order": 1},
                ]},
                {"code": "A.7.13", "title": "Equipment maintenance", "description": "Equipment shall be maintained correctly to ensure availability, integrity, and confidentiality of information.", "sort_order": 13, "objectives": [
                    {"code": "A.7.13.1", "title": "Equipment maintenance schedules are followed", "sort_order": 1},
                ]},
                {"code": "A.7.14", "title": "Secure disposal or re-use of equipment", "description": "Items of equipment containing storage media shall be verified to ensure that sensitive data has been removed or securely overwritten.", "sort_order": 14, "objectives": [
                    {"code": "A.7.14.1", "title": "Secure disposal procedures are followed", "sort_order": 1},
                ]},
            ],
        },
        {
            "code": "A.8",
            "name": "Technological Controls",
            "description": "Controls for technology including endpoints, access, cryptography, development, and operations.",
            "sort_order": 4,
            "requirements": [
                {"code": "A.8.1", "title": "User endpoint devices", "description": "Information stored on, processed by, or accessible via user endpoint devices shall be protected.", "sort_order": 1, "objectives": [
                    {"code": "A.8.1.1", "title": "Endpoint protection is implemented", "sort_order": 1},
                ]},
                {"code": "A.8.2", "title": "Privileged access rights", "description": "The allocation and use of privileged access rights shall be restricted and managed.", "sort_order": 2, "objectives": [
                    {"code": "A.8.2.1", "title": "Privileged access is restricted", "sort_order": 1},
                ]},
                {"code": "A.8.3", "title": "Information access restriction", "description": "Access to information and application system functions shall be restricted.", "sort_order": 3, "objectives": [
                    {"code": "A.8.3.1", "title": "Information access restrictions are enforced", "sort_order": 1},
                ]},
                {"code": "A.8.4", "title": "Access to source code", "description": "Read and write access to source code, development tools, and software libraries shall be appropriately managed.", "sort_order": 4, "objectives": [
                    {"code": "A.8.4.1", "title": "Source code access is controlled", "sort_order": 1},
                ]},
                {"code": "A.8.5", "title": "Secure authentication", "description": "Secure authentication technologies and procedures shall be established.", "sort_order": 5, "objectives": [
                    {"code": "A.8.5.1", "title": "Secure authentication is enforced", "sort_order": 1},
                ]},
                {"code": "A.8.6", "title": "Capacity management", "description": "The use of resources shall be monitored and adjusted in line with current and expected capacity requirements.", "sort_order": 6, "objectives": [
                    {"code": "A.8.6.1", "title": "Capacity monitoring is implemented", "sort_order": 1},
                ]},
                {"code": "A.8.7", "title": "Protection against malware", "description": "Protection against malware shall be implemented and supported by appropriate user awareness.", "sort_order": 7, "objectives": [
                    {"code": "A.8.7.1", "title": "Malware protection is deployed", "sort_order": 1},
                ]},
                {"code": "A.8.8", "title": "Management of technical vulnerabilities", "description": "Information about technical vulnerabilities of information systems in use shall be obtained and appropriate measures taken.", "sort_order": 8, "objectives": [
                    {"code": "A.8.8.1", "title": "Vulnerability management process exists", "sort_order": 1},
                ]},
                {"code": "A.8.9", "title": "Configuration management", "description": "Configurations, including security configurations, of hardware, software, services, and networks shall be established, documented, and managed.", "sort_order": 9, "objectives": [
                    {"code": "A.8.9.1", "title": "Configuration management is implemented", "sort_order": 1},
                ]},
                {"code": "A.8.10", "title": "Information deletion", "description": "Information stored in information systems, devices, or in any other storage media shall be deleted when no longer required.", "sort_order": 10, "objectives": [
                    {"code": "A.8.10.1", "title": "Data deletion procedures are followed", "sort_order": 1},
                ]},
                {"code": "A.8.11", "title": "Data masking", "description": "Data masking shall be used in accordance with the organization's topic-specific policy on access control.", "sort_order": 11, "objectives": [
                    {"code": "A.8.11.1", "title": "Data masking is applied where required", "sort_order": 1},
                ]},
                {"code": "A.8.12", "title": "Data leakage prevention", "description": "Data leakage prevention measures shall be applied to systems, networks, and any other devices that process, store, or transmit sensitive information.", "sort_order": 12, "objectives": [
                    {"code": "A.8.12.1", "title": "DLP controls are implemented", "sort_order": 1},
                ]},
                {"code": "A.8.13", "title": "Information backup", "description": "Backup copies of information, software, and systems shall be maintained and regularly tested.", "sort_order": 13, "objectives": [
                    {"code": "A.8.13.1", "title": "Backup procedures are tested regularly", "sort_order": 1},
                ]},
                {"code": "A.8.14", "title": "Redundancy of information processing facilities", "description": "Information processing facilities shall be implemented with sufficient redundancy.", "sort_order": 14, "objectives": [
                    {"code": "A.8.14.1", "title": "Redundancy requirements are met", "sort_order": 1},
                ]},
                {"code": "A.8.15", "title": "Logging", "description": "Logs that record activities, exceptions, faults, and other relevant events shall be produced, stored, protected, and analysed.", "sort_order": 15, "objectives": [
                    {"code": "A.8.15.1", "title": "Logging is implemented and monitored", "sort_order": 1},
                ]},
                {"code": "A.8.16", "title": "Monitoring activities", "description": "Networks, systems, and applications shall be monitored for anomalous behaviour.", "sort_order": 16, "objectives": [
                    {"code": "A.8.16.1", "title": "Anomaly monitoring is operational", "sort_order": 1},
                ]},
                {"code": "A.8.17", "title": "Clock synchronization", "description": "The clocks of information processing systems shall be synchronized to approved time sources.", "sort_order": 17, "objectives": [
                    {"code": "A.8.17.1", "title": "Clock synchronization is configured", "sort_order": 1},
                ]},
                {"code": "A.8.18", "title": "Use of privileged utility programs", "description": "The use of utility programs that might be capable of overriding system and application controls shall be restricted.", "sort_order": 18, "objectives": [
                    {"code": "A.8.18.1", "title": "Privileged utility use is restricted", "sort_order": 1},
                ]},
                {"code": "A.8.19", "title": "Installation of software on operational systems", "description": "Procedures and measures shall be implemented to securely manage software installation.", "sort_order": 19, "objectives": [
                    {"code": "A.8.19.1", "title": "Software installation is controlled", "sort_order": 1},
                ]},
                {"code": "A.8.20", "title": "Networks security", "description": "Networks and network devices shall be secured, managed, and controlled.", "sort_order": 20, "objectives": [
                    {"code": "A.8.20.1", "title": "Network security controls are implemented", "sort_order": 1},
                ]},
                {"code": "A.8.21", "title": "Security of network services", "description": "Security mechanisms, service levels, and service requirements of network services shall be identified, implemented, and monitored.", "sort_order": 21, "objectives": [
                    {"code": "A.8.21.1", "title": "Network service security is managed", "sort_order": 1},
                ]},
                {"code": "A.8.22", "title": "Segregation of networks", "description": "Groups of information services, users, and information systems shall be segregated in the organization's networks.", "sort_order": 22, "objectives": [
                    {"code": "A.8.22.1", "title": "Network segregation is implemented", "sort_order": 1},
                ]},
                {"code": "A.8.23", "title": "Web filtering", "description": "Access to external websites shall be managed to reduce exposure to malicious content.", "sort_order": 23, "objectives": [
                    {"code": "A.8.23.1", "title": "Web filtering is configured", "sort_order": 1},
                ]},
                {"code": "A.8.24", "title": "Use of cryptography", "description": "Rules for the effective use of cryptography shall be defined and implemented.", "sort_order": 24, "objectives": [
                    {"code": "A.8.24.1", "title": "Cryptography policy is defined", "sort_order": 1},
                ]},
                {"code": "A.8.25", "title": "Secure development life cycle", "description": "Rules for the secure development of software and systems shall be established and applied.", "sort_order": 25, "objectives": [
                    {"code": "A.8.25.1", "title": "SDLC security practices are defined", "sort_order": 1},
                ]},
                {"code": "A.8.26", "title": "Application security requirements", "description": "Information security requirements shall be identified, specified, and approved when developing or acquiring applications.", "sort_order": 26, "objectives": [
                    {"code": "A.8.26.1", "title": "Application security requirements are specified", "sort_order": 1},
                ]},
                {"code": "A.8.27", "title": "Secure system architecture and engineering principles", "description": "Principles for engineering secure systems shall be established, documented, maintained, and applied.", "sort_order": 27, "objectives": [
                    {"code": "A.8.27.1", "title": "Secure architecture principles are applied", "sort_order": 1},
                ]},
                {"code": "A.8.28", "title": "Secure coding", "description": "Secure coding principles shall be applied to software development.", "sort_order": 28, "objectives": [
                    {"code": "A.8.28.1", "title": "Secure coding standards are followed", "sort_order": 1},
                ]},
                {"code": "A.8.29", "title": "Security testing in development and acceptance", "description": "Security testing processes shall be defined and implemented in the development life cycle.", "sort_order": 29, "objectives": [
                    {"code": "A.8.29.1", "title": "Security testing is performed", "sort_order": 1},
                ]},
                {"code": "A.8.30", "title": "Outsourced development", "description": "The organization shall direct, monitor, and review the activities related to outsourced system development.", "sort_order": 30, "objectives": [
                    {"code": "A.8.30.1", "title": "Outsourced development is supervised", "sort_order": 1},
                ]},
                {"code": "A.8.31", "title": "Separation of development, test and production environments", "description": "Development, testing, and production environments shall be separated and secured.", "sort_order": 31, "objectives": [
                    {"code": "A.8.31.1", "title": "Environment separation is enforced", "sort_order": 1},
                ]},
                {"code": "A.8.32", "title": "Change management", "description": "Changes to information processing facilities and information systems shall be subject to change management procedures.", "sort_order": 32, "objectives": [
                    {"code": "A.8.32.1", "title": "Change management procedures are followed", "sort_order": 1},
                ]},
                {"code": "A.8.33", "title": "Test information", "description": "Test information shall be appropriately selected, protected, and managed.", "sort_order": 33, "objectives": [
                    {"code": "A.8.33.1", "title": "Test data is properly managed", "sort_order": 1},
                ]},
                {"code": "A.8.34", "title": "Protection of information systems during audit testing", "description": "Audit tests and other assurance activities involving assessment of operational systems shall be planned and agreed.", "sort_order": 34, "objectives": [
                    {"code": "A.8.34.1", "title": "Audit testing is planned and controlled", "sort_order": 1},
                ]},
            ],
        },
    ],
}


async def seed_iso27001_framework(db):
    from app.models.framework import Framework
    from app.models.framework_domain import FrameworkDomain
    from app.models.framework_requirement import FrameworkRequirement
    from app.models.control_objective import ControlObjective
    from sqlalchemy import select

    # Check if already seeded
    existing = await db.execute(
        select(Framework).where(Framework.name == ISO27001_FRAMEWORK["name"])
    )
    if existing.scalar_one_or_none():
        print("ISO 27001 framework already seeded, skipping.")
        return None

    framework = Framework(
        name=ISO27001_FRAMEWORK["name"],
        version=ISO27001_FRAMEWORK["version"],
        category=ISO27001_FRAMEWORK["category"],
        description=ISO27001_FRAMEWORK["description"],
    )
    db.add(framework)
    await db.flush()

    total_controls = 0
    for domain_data in ISO27001_FRAMEWORK["domains"]:
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
            total_controls += 1

            for obj_data in req_data.get("objectives", []):
                obj = ControlObjective(
                    requirement_id=req.id,
                    code=obj_data["code"],
                    title=obj_data["title"],
                    sort_order=obj_data["sort_order"],
                )
                db.add(obj)

    await db.commit()
    print(f"Seeded ISO 27001 framework with {len(ISO27001_FRAMEWORK['domains'])} domains, {total_controls} controls.")
    return framework
