"""CIS Controls v8 — Center for Internet Security Critical Security Controls — framework seed data."""

CIS_FRAMEWORK = {
    "name": "CIS Controls",
    "version": "v8",
    "category": "Security & Compliance",
    "description": "CIS Critical Security Controls Version 8 — a prioritized set of 18 safeguards to mitigate the most prevalent cyber attacks against systems and networks, organized into three implementation groups (IG1, IG2, IG3).",
    "domains": [
        {
            "code": "CIS.1",
            "name": "Inventory and Control of Enterprise Assets",
            "description": "Actively manage (inventory, track, and correct) all enterprise assets connected to the infrastructure to accurately know the totality of assets that need to be monitored and protected.",
            "sort_order": 1,
            "requirements": [
                {
                    "code": "CIS.1.1",
                    "title": "Establish and Maintain Detailed Enterprise Asset Inventory",
                    "description": "Establish and maintain an accurate, detailed, and up-to-date inventory of all enterprise assets with the potential to store or process data, including end-user devices, network devices, IoT devices, and servers.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CIS.1.1a", "title": "Enterprise asset inventory is established and maintained", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.1.2",
                    "title": "Address Unauthorized Assets",
                    "description": "Ensure that a process exists to address unauthorized assets on a weekly basis. The enterprise may choose to remove the asset from the network, deny the asset from connecting remotely, or quarantine the asset.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CIS.1.2a", "title": "Unauthorized assets are identified and addressed weekly", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.1.3",
                    "title": "Utilize an Active Discovery Tool",
                    "description": "Utilize an active discovery tool to identify assets connected to the enterprise's network. Configure the active discovery tool to execute daily, or more frequently.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CIS.1.3a", "title": "Active discovery tool scans the network daily", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CIS.2",
            "name": "Inventory and Control of Software Assets",
            "description": "Actively manage (inventory, track, and correct) all software on the network so that only authorized software is installed and can execute, and that unauthorized and unmanaged software is found and prevented from installation or execution.",
            "sort_order": 2,
            "requirements": [
                {
                    "code": "CIS.2.1",
                    "title": "Establish and Maintain a Software Inventory",
                    "description": "Establish and maintain a detailed inventory of all licensed software installed on enterprise assets, including title, publisher, initial install/use date, and business purpose.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CIS.2.1a", "title": "Software inventory is established and maintained", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.2.2",
                    "title": "Ensure Authorized Software is Currently Supported",
                    "description": "Ensure that only currently supported software is designated as authorized in the software inventory. Unsupported software is tagged as unsupported in the inventory system.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CIS.2.2a", "title": "Unsupported software is identified and addressed", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.2.3",
                    "title": "Address Unauthorized Software",
                    "description": "Ensure that unauthorized software is either removed or the inventory is updated in a timely manner, at least monthly.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CIS.2.3a", "title": "Unauthorized software is removed or documented monthly", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CIS.3",
            "name": "Data Protection",
            "description": "Develop processes and technical controls to identify, classify, securely handle, retain, and dispose of data.",
            "sort_order": 3,
            "requirements": [
                {
                    "code": "CIS.3.1",
                    "title": "Establish and Maintain a Data Management Process",
                    "description": "Establish and maintain a data management process that addresses data sensitivity, data owner, handling of data, data retention limits, and disposal requirements.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CIS.3.1a", "title": "Data management process is documented and maintained", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.3.2",
                    "title": "Establish and Maintain a Data Inventory",
                    "description": "Establish and maintain a data inventory based on the enterprise's data management process, at minimum inventorying sensitive data.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CIS.3.2a", "title": "Sensitive data inventory is maintained", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.3.3",
                    "title": "Configure Data Access Control Lists",
                    "description": "Configure data access control lists based on a user's need to know, applying to local and remote file systems, databases, and applications.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CIS.3.3a", "title": "Data access control lists are configured based on need-to-know", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.3.4",
                    "title": "Enforce Data Retention",
                    "description": "Retain data according to the enterprise's data management process, ensuring data retention includes both minimum and maximum timelines.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CIS.3.4a", "title": "Data retention policies are enforced", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CIS.4",
            "name": "Secure Configuration of Enterprise Assets and Software",
            "description": "Establish and maintain the secure configuration of enterprise assets and software, including end-user devices, network devices, servers, and applications.",
            "sort_order": 4,
            "requirements": [
                {
                    "code": "CIS.4.1",
                    "title": "Establish and Maintain a Secure Configuration Process",
                    "description": "Establish and maintain a secure configuration process for enterprise assets and software. Review and update documentation annually or when significant enterprise changes occur.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CIS.4.1a", "title": "Secure configuration process is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.4.2",
                    "title": "Establish and Maintain a Secure Configuration for Network Infrastructure",
                    "description": "Establish and maintain a secure configuration process for network devices, including firewalls, routers, and switches.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CIS.4.2a", "title": "Network device configurations follow security baselines", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.4.7",
                    "title": "Manage Default Accounts on Enterprise Assets and Software",
                    "description": "Manage default accounts on enterprise assets and software, such as root, administrator, and other preconfigured vendor accounts, including disabling or modifying them.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CIS.4.7a", "title": "Default accounts are disabled or have changed credentials", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CIS.5",
            "name": "Account Management",
            "description": "Use processes and tools to assign and manage authorization to credentials for user accounts, including administrator accounts, service accounts, and application accounts.",
            "sort_order": 5,
            "requirements": [
                {
                    "code": "CIS.5.1",
                    "title": "Establish and Maintain an Inventory of Accounts",
                    "description": "Establish and maintain an inventory of all accounts managed in the enterprise, including user, administrator, and service accounts.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CIS.5.1a", "title": "Account inventory is maintained and reviewed", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.5.3",
                    "title": "Disable Dormant Accounts",
                    "description": "Delete or disable any dormant accounts after a period of 45 days of inactivity, where supported.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CIS.5.3a", "title": "Dormant accounts are disabled within 45 days", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.5.4",
                    "title": "Restrict Administrator Privileges to Dedicated Administrator Accounts",
                    "description": "Restrict administrator privileges to dedicated administrator accounts on enterprise assets. Conduct general computing activities with non-privileged accounts.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CIS.5.4a", "title": "Administrator privileges are limited to dedicated accounts", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CIS.6",
            "name": "Access Control Management",
            "description": "Use processes and tools to create, assign, manage, and revoke access credentials and privileges for user, administrator, and service accounts for enterprise assets and software.",
            "sort_order": 6,
            "requirements": [
                {
                    "code": "CIS.6.1",
                    "title": "Establish an Access Granting Process",
                    "description": "Establish and follow a process, preferably automated, for granting access to enterprise assets upon new hire, rights grant, or role change.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CIS.6.1a", "title": "Access granting process is documented and followed", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.6.2",
                    "title": "Establish an Access Revoking Process",
                    "description": "Establish and follow a process, preferably automated, for revoking access to enterprise assets, through disabling accounts rather than deleting accounts, upon termination, rights revocation, or role change.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CIS.6.2a", "title": "Access revoking process is established and timely", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.6.3",
                    "title": "Require MFA for Externally-Exposed Applications",
                    "description": "Require all externally-exposed enterprise or third-party applications to enforce multi-factor authentication where supported.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CIS.6.3a", "title": "MFA is enforced for externally-exposed applications", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.6.5",
                    "title": "Require MFA for Administrative Access",
                    "description": "Require MFA for all administrative access accounts, where supported, on all enterprise assets, whether managed on-site or through a third-party provider.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CIS.6.5a", "title": "MFA is enforced for all administrative access", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CIS.7",
            "name": "Continuous Vulnerability Management",
            "description": "Develop a plan to continuously assess and track vulnerabilities on all enterprise assets, in order to remediate and minimize the window of opportunity for attackers.",
            "sort_order": 7,
            "requirements": [
                {
                    "code": "CIS.7.1",
                    "title": "Establish and Maintain a Vulnerability Management Process",
                    "description": "Establish and maintain a documented vulnerability management process for enterprise assets, including a schedule for addressing vulnerabilities based on severity.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CIS.7.1a", "title": "Vulnerability management process is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.7.2",
                    "title": "Establish and Maintain a Remediation Process",
                    "description": "Establish and maintain a risk-based remediation strategy documented in a remediation process, with monthly or more frequent review.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CIS.7.2a", "title": "Risk-based remediation process is established", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.7.4",
                    "title": "Perform Automated Application Patch Management",
                    "description": "Perform application updates on enterprise assets through automated patch management on a monthly or more frequent basis.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CIS.7.4a", "title": "Automated application patching is operational", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CIS.8",
            "name": "Audit Log Management",
            "description": "Collect, alert, review, and retain audit logs of events that could help detect, understand, or recover from an attack.",
            "sort_order": 8,
            "requirements": [
                {
                    "code": "CIS.8.1",
                    "title": "Establish and Maintain an Audit Log Management Process",
                    "description": "Establish and maintain an audit log management process that defines the enterprise's logging requirements, including collection, review, and retention of audit logs.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CIS.8.1a", "title": "Audit log management process is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.8.2",
                    "title": "Collect Audit Logs",
                    "description": "Collect audit logs, ensuring standardized logging is enabled across all enterprise assets and software where feasible.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CIS.8.2a", "title": "Audit log collection is enabled across enterprise assets", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.8.5",
                    "title": "Collect Detailed Audit Logs",
                    "description": "Configure detailed audit logging for enterprise assets containing sensitive data, including event source, date, username, timestamp, source addresses, destination addresses, and other useful elements.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CIS.8.5a", "title": "Detailed audit logs capture required fields", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.8.9",
                    "title": "Centralize Audit Logs",
                    "description": "Centralize, to the extent possible, audit log collection and retention across enterprise assets.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CIS.8.9a", "title": "Audit logs are centralized for analysis", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CIS.9",
            "name": "Email and Web Browser Protections",
            "description": "Improve protections and detections of threats from email and web vectors, as these are opportunities for attackers to manipulate human behavior through direct engagement.",
            "sort_order": 9,
            "requirements": [
                {
                    "code": "CIS.9.1",
                    "title": "Ensure Use of Only Fully Supported Browsers and Email Clients",
                    "description": "Ensure only fully supported browsers and email clients are allowed to execute in the enterprise, using the latest version of browsers and email clients.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CIS.9.1a", "title": "Only supported browsers and email clients are permitted", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.9.2",
                    "title": "Use DNS Filtering Services",
                    "description": "Use DNS filtering services on all enterprise assets to block access to known malicious domains.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CIS.9.2a", "title": "DNS filtering blocks known malicious domains", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.9.6",
                    "title": "Block Unnecessary File Types",
                    "description": "Block unnecessary file types attempting to enter the enterprise's email gateway.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CIS.9.6a", "title": "Unnecessary file types are blocked at email gateway", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CIS.10",
            "name": "Malware Defenses",
            "description": "Prevent or control the installation, spread, and execution of malicious applications, code, or scripts on enterprise assets.",
            "sort_order": 10,
            "requirements": [
                {
                    "code": "CIS.10.1",
                    "title": "Deploy and Maintain Anti-Malware Software",
                    "description": "Install and maintain anti-malware software on all enterprise assets.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CIS.10.1a", "title": "Anti-malware software is deployed on all assets", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.10.2",
                    "title": "Configure Automatic Anti-Malware Signature Updates",
                    "description": "Configure automatic updates for anti-malware signature files on all enterprise assets.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CIS.10.2a", "title": "Anti-malware signatures are updated automatically", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.10.4",
                    "title": "Configure Automatic Anti-Malware Scanning of Removable Media",
                    "description": "Configure anti-malware software to automatically scan removable media.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CIS.10.4a", "title": "Removable media is automatically scanned for malware", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CIS.11",
            "name": "Data Recovery",
            "description": "Establish and maintain data recovery practices sufficient to restore in-scope enterprise assets to a pre-incident and trusted state.",
            "sort_order": 11,
            "requirements": [
                {
                    "code": "CIS.11.1",
                    "title": "Establish and Maintain a Data Recovery Process",
                    "description": "Establish and maintain a data recovery process covering scope of data recovery activities, recovery prioritization, and the security of backup data.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CIS.11.1a", "title": "Data recovery process is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.11.2",
                    "title": "Perform Automated Backups",
                    "description": "Perform automated backups of in-scope enterprise assets, running weekly or more frequently based on the sensitivity and criticality of the data.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CIS.11.2a", "title": "Automated backups are performed at least weekly", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.11.3",
                    "title": "Protect Recovery Data",
                    "description": "Protect recovery data with equivalent controls to the original data, including encryption of backup data.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CIS.11.3a", "title": "Backup data is encrypted and access-controlled", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.11.4",
                    "title": "Establish and Maintain an Isolated Instance of Recovery Data",
                    "description": "Establish and maintain an isolated instance of recovery data using versioning and an offline, cloud, or off-site system or service.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CIS.11.4a", "title": "Isolated recovery data instance exists", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CIS.12",
            "name": "Network Infrastructure Management",
            "description": "Establish and maintain the secure management of the enterprise's network infrastructure, including both physical and virtual network devices.",
            "sort_order": 12,
            "requirements": [
                {
                    "code": "CIS.12.1",
                    "title": "Ensure Network Infrastructure is Up-to-Date",
                    "description": "Ensure network infrastructure is kept up-to-date, including firmware and operating systems on network devices.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CIS.12.1a", "title": "Network infrastructure is patched and up-to-date", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.12.2",
                    "title": "Establish and Maintain a Secure Network Architecture",
                    "description": "Establish and maintain a secure network architecture, including network segmentation and security zone definitions.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CIS.12.2a", "title": "Network architecture includes segmentation", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.12.4",
                    "title": "Establish and Maintain Architecture Diagram(s)",
                    "description": "Establish and maintain architecture diagram(s) and/or other network system documentation showing all enterprise assets, network boundaries, and key infrastructure elements.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CIS.12.4a", "title": "Network architecture diagrams are maintained", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CIS.13",
            "name": "Network Monitoring and Defense",
            "description": "Operate processes and tooling to establish and maintain comprehensive network monitoring and defense against security threats across the enterprise's network infrastructure and user base.",
            "sort_order": 13,
            "requirements": [
                {
                    "code": "CIS.13.1",
                    "title": "Centralize Security Event Alerting",
                    "description": "Centralize security event alerting across enterprise assets for log correlation and analysis using a SIEM or equivalent tool.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CIS.13.1a", "title": "Security event alerting is centralized", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.13.3",
                    "title": "Deploy a Network Intrusion Detection Solution",
                    "description": "Deploy a network intrusion detection solution on enterprise assets where appropriate.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CIS.13.3a", "title": "Network intrusion detection is deployed", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.13.6",
                    "title": "Collect Network Traffic Flow Logs",
                    "description": "Collect network traffic flow logs and/or network traffic to review and alert upon from network devices.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CIS.13.6a", "title": "Network traffic flow logs are collected and analyzed", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CIS.14",
            "name": "Security Awareness and Skills Training",
            "description": "Establish and maintain a security awareness program to influence behavior among the workforce to be security conscious and properly skilled to reduce cybersecurity risks to the enterprise.",
            "sort_order": 14,
            "requirements": [
                {
                    "code": "CIS.14.1",
                    "title": "Establish and Maintain a Security Awareness Program",
                    "description": "Establish and maintain a security awareness program covering phishing, pre-texting, social engineering, credential theft, and other relevant threats.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CIS.14.1a", "title": "Security awareness program is established", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.14.2",
                    "title": "Train Workforce Members to Recognize Social Engineering Attacks",
                    "description": "Train workforce members to recognize social engineering attacks, such as phishing, pre-texting, and tailgating.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CIS.14.2a", "title": "Social engineering awareness training is delivered", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.14.3",
                    "title": "Train Workforce Members on Authentication Best Practices",
                    "description": "Train workforce members on authentication best practices, including MFA, password composition, and credential management.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CIS.14.3a", "title": "Authentication best practices training is provided", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CIS.15",
            "name": "Service Provider Management",
            "description": "Develop a process to evaluate service providers who hold sensitive data, or are responsible for an enterprise's critical IT platforms or processes, to ensure these providers are protecting those platforms and data appropriately.",
            "sort_order": 15,
            "requirements": [
                {
                    "code": "CIS.15.1",
                    "title": "Establish and Maintain an Inventory of Service Providers",
                    "description": "Establish and maintain an inventory of service providers including classification by sensitivity of data handled and criticality of services provided.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CIS.15.1a", "title": "Service provider inventory is maintained", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.15.2",
                    "title": "Establish and Maintain a Service Provider Management Policy",
                    "description": "Establish and maintain a service provider management policy that covers classification, assessment, and monitoring of service providers.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CIS.15.2a", "title": "Service provider management policy is documented", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.15.4",
                    "title": "Ensure Service Provider Contracts Include Security Requirements",
                    "description": "Ensure service provider contracts include security requirements, including minimum security program requirements, security incident and/or data breach notification, and data encryption requirements.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CIS.15.4a", "title": "Service provider contracts include security requirements", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CIS.16",
            "name": "Application Software Security",
            "description": "Manage the security life cycle of in-house developed, hosted, or acquired software to prevent, detect, and remediate security weaknesses before they can impact the enterprise.",
            "sort_order": 16,
            "requirements": [
                {
                    "code": "CIS.16.1",
                    "title": "Establish and Maintain a Secure Application Development Process",
                    "description": "Establish and maintain a secure application development process including secure coding standards and peer code review.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CIS.16.1a", "title": "Secure development process is documented and followed", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.16.4",
                    "title": "Establish and Manage an Inventory of Third-Party Software Components",
                    "description": "Establish and manage an updated inventory of third-party components used in development (bill of materials), including libraries, frameworks, and dependencies.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CIS.16.4a", "title": "Third-party software component inventory (SBOM) is maintained", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.16.9",
                    "title": "Train Developers in Application Security Concepts and Secure Coding",
                    "description": "Ensure all software development personnel receive training in writing secure code for their specific development environment and responsibilities.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CIS.16.9a", "title": "Developer secure coding training is provided", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CIS.17",
            "name": "Incident Response Management",
            "description": "Establish a program to develop and maintain an incident response capability (e.g., policies, plans, procedures, defined roles, training, and communications) to prepare, detect, and quickly respond to an attack.",
            "sort_order": 17,
            "requirements": [
                {
                    "code": "CIS.17.1",
                    "title": "Designate Personnel to Manage Incident Handling",
                    "description": "Designate one key person, and at least one backup, who will manage the enterprise's incident handling process.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CIS.17.1a", "title": "Incident handling personnel are designated", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.17.2",
                    "title": "Establish and Maintain Contact Information for Reporting Security Incidents",
                    "description": "Establish and maintain contact information for parties that need to be informed of security incidents including legal, compliance, and management.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CIS.17.2a", "title": "Incident notification contact list is maintained", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.17.3",
                    "title": "Establish and Maintain an Enterprise Process for Reporting Incidents",
                    "description": "Establish and maintain an enterprise process for the workforce to report security incidents, including a mechanism for anonymous reporting.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CIS.17.3a", "title": "Incident reporting process is established", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.17.4",
                    "title": "Establish and Maintain an Incident Response Process",
                    "description": "Establish and maintain an incident response process that addresses roles and responsibilities, compliance requirements, and a communication plan, and is tested annually at minimum.",
                    "sort_order": 4,
                    "objectives": [
                        {"code": "CIS.17.4a", "title": "Incident response process is documented and tested annually", "sort_order": 1},
                    ],
                },
            ],
        },
        {
            "code": "CIS.18",
            "name": "Penetration Testing",
            "description": "Test the effectiveness and resiliency of enterprise assets through identifying and exploiting weaknesses in controls and simulating the objectives and actions of an attacker.",
            "sort_order": 18,
            "requirements": [
                {
                    "code": "CIS.18.1",
                    "title": "Establish and Maintain a Penetration Testing Program",
                    "description": "Establish and maintain a penetration testing program appropriate to the size, complexity, and maturity of the enterprise, including a defined scope, frequency, and remediation approach.",
                    "sort_order": 1,
                    "objectives": [
                        {"code": "CIS.18.1a", "title": "Penetration testing program is established", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.18.2",
                    "title": "Perform Periodic External Penetration Tests",
                    "description": "Perform periodic external penetration tests based on program requirements, no less than annually, covering the external perimeter and testing for both technical and business logic flaws.",
                    "sort_order": 2,
                    "objectives": [
                        {"code": "CIS.18.2a", "title": "External penetration tests are performed annually", "sort_order": 1},
                    ],
                },
                {
                    "code": "CIS.18.3",
                    "title": "Remediate Penetration Test Findings",
                    "description": "Remediate penetration test findings based on the enterprise's policy for remediation scope and prioritization.",
                    "sort_order": 3,
                    "objectives": [
                        {"code": "CIS.18.3a", "title": "Penetration test findings are remediated per policy", "sort_order": 1},
                    ],
                },
            ],
        },
    ],
}


async def seed_cis_framework(db):
    """Seed the CIS Controls v8 framework."""
    from sqlalchemy import select
    from app.models.framework import Framework
    from app.models.framework_domain import FrameworkDomain
    from app.models.framework_requirement import FrameworkRequirement
    from app.models.control_objective import ControlObjective

    # Check if already seeded
    existing = await db.execute(
        select(Framework).where(Framework.name == CIS_FRAMEWORK["name"])
    )
    if existing.scalar_one_or_none():
        print("  -> CIS Controls framework already seeded, skipping.")
        return

    fw_data = CIS_FRAMEWORK
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
    print(f"  Seeded CIS Controls: {req_count} requirements, {obj_count} objectives.")
    return framework
