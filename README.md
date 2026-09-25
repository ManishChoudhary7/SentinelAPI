SentinelAPI

Zero-Trust API Security Testing Platform

SentinelAPI is an automated, zero-trust API security testing platform
designed to analyze an API's OpenAPI/Swagger specification, discover API
endpoints, perform automated security tests, analyze API responses,
identify potential security vulnerabilities, rank findings by severity,
and generate clear security reports.

1. Team

Name                  Role

Neha Sharma           Team Leader
Manish Choudhary      Backend Developer
Aryan Yadav           Frontend Developer
Jaishree Dholpuriya   Presentation

2. Problem Statement

Modern software applications depend on APIs to communicate between
systems, services, and databases. APIs can create security weaknesses
when they are not designed or configured properly. Examples include
unauthorized access to another user's data, excessive information
exposure, and weak authentication.

Many startups and medium-sized companies still perform API security
checks manually and only occasionally. SentinelAPI addresses this need
through automated API security testing that helps identify risks
earlier.

3. Proposed Solution

SentinelAPI analyzes an API's OpenAPI/Swagger specification,
automatically discovers endpoints, performs security tests, analyzes
responses, and converts the results into clear, severity-ranked security
findings.

OpenAPI / Swagger
        |
        v
Endpoint Discovery
        |
        v
Automated Security Testing
        |
        v
Authorization Testing
        |
        v
Response Analysis
        |
        v
Vulnerability Analysis
        |
        v
Severity Ranking
        |
        v
Evidence / Reproduction
        |
        v
Security Dashboard
        |
        v
Report Generation

4. Solution Steps

OpenAPI/Swagger Ingestion

Automated Security Testing Engine

Authorization Testing

Response Analysis & Data Exposure Detection

Vulnerability Analysis & Severity Ranking

Proof-of-Concept / Reproduction

Security Dashboard

Report Generation

AI-Assisted Security Testing / Security Copilot

5. Key Features

OpenAPI/Swagger-based automated testing

Automated security scanning

Vulnerability detection

Severity assessment

Evidence and reproduction information

Security testing dashboard

Automated report generation

Target API integration

Security Copilot for scan explanation and remediation guidance

Current security checks include possible BOLA/IDOR, sensitive data
exposure, authentication misconfiguration, and rate-limit issues.

6. System Architecture

                    +----------------------+
                    |        USER          |
                    | Developer / Security |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |   SentinelAPI UI     |
                    |      Streamlit       |
                    +----------+-----------+
                               |
              +----------------+----------------+
              |                |                |
              v                v                v
       +------------+   +-------------+   +--------------+
       |  OpenAPI / |   | API Scanner |   | AI Security  |
       |  Swagger   |   |   Engine    |   |   Copilot    |
       +-----+------+   +------+------+   +------+-------+
             |                 |                 |
             v                 v                 v
       +------------+   +-------------+   +--------------+
       |  Endpoint  |   | Vulnerability|   |  Gemini API |
       | Extraction |   |  Detection  |   |              |
       +------------+   +------+------+   +--------------+
                               |
                               v
                      +-----------------+
                      | Findings / Risk |
                      | Score / Evidence|
                      +--------+--------+
                               |
                               v
                      +-----------------+
                      | Security Report |
                      |    JSON + UI    |
                      +-----------------+

7. Technology Stack

Technology          Purpose

Python              Core application and security logic
Streamlit           Web dashboard and UI
OpenAPI / Swagger   API specification and endpoint discovery
HTTPX               HTTP request/response testing
Pydantic            Structured finding models
JSON                API specifications and reports
Gemini API          AI Security Copilot

8. Project Workflow

User provides an OpenAPI/Swagger URL or JSON specification.

SentinelAPI discovers API endpoints.

The scanner sends security test requests.

API responses are analyzed.

Security checks generate findings.

Findings are assigned severity and risk information.

Evidence and reproduction information are recorded.

Results are displayed in the dashboard.

A structured security report is generated.

The Security Copilot explains the available findings and suggests
remediation.

9. Vulnerability Checks

BOLA / IDOR

The scanner can identify possible object-level authorization problems by
comparing behavior for different object identifiers. Possible findings
should be manually verified before being treated as confirmed
vulnerabilities.

Sensitive Data Exposure

The scanner checks API responses for potentially sensitive information
such as password-related fields, API keys, and other security-relevant
data.

Authentication Misconfiguration

The scanner checks configured API behavior for authentication-related
weaknesses supported by the current scanning logic.

Rate Limit

The scanner checks API behavior for insufficient rate limiting,
especially on sensitive endpoints such as login.

10. Security Findings

A finding can contain:

Vulnerability name

Severity

Affected endpoint

Evidence

Impact

Recommendation

Proof-of-concept information

Severity levels:

HIGH

MEDIUM

LOW

11. Security Dashboard

The Streamlit dashboard provides:

API configuration

OpenAPI/Swagger discovery

API specification upload

Security scan controls

Vulnerability findings

Risk information

Security report

Security Copilot

12. AI Security Copilot

The Security Copilot helps developers understand scan results.

Example questions:

What vulnerabilities were found in this scan?

Explain the HIGH severity findings.

How can I fix these vulnerabilities?

Which endpoints are affected?

Explain the possible BOLA/IDOR finding.

Generate a remediation checklist.

The scanner findings and evidence remain the primary source of security
information. The Copilot explains the available scan context and should
distinguish possible findings from confirmed findings.

13. Demo API

For controlled demonstration, the project can use a local vulnerable
API.

OpenAPI:

http://127.0.0.1:8001/openapi.json

Swagger UI:

http://127.0.0.1:8001/docs

Use only controlled or authorized APIs for security testing.

14. Installation

Requirements

Python 3.x

pip

Web browser

OpenAPI/Swagger specification

Install dependencies

pip install -r requirements.txt

Run SentinelAPI

streamlit run dashboard.py

Run for LAN access

streamlit run dashboard.py --server.address=0.0.0.0 --server.port=8501

15. Current Demo URL

http://10.2.157.70:8501

This is the LAN demo URL shown in the project presentation. It is not a
permanent public deployment URL and requires the host machine and
Streamlit server to be running on a reachable network.

16. How to Use

Open the SentinelAPI dashboard.

Enter an OpenAPI/Swagger URL or upload an OpenAPI JSON file.

Click Discover.

Review discovered endpoints.

Configure authentication if required.

Click Scan Selected API.

Review findings, severity, evidence and recommendations.

Use the Security Copilot to ask questions about the scan.

Review or export the security report.

17. Report

The security report can contain:

Target API

Total endpoints

Total vulnerabilities

HIGH count

MEDIUM count

LOW count

Risk score

Findings

Evidence

Recommendations

PoC information

18. Repository Structure

SentinelAPI/
├── dashboard.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── backend/
│   ├── ai/
│   │   └── security_chat.py
│   ├── scanner/
│   │   └── request_engine.py
│   ├── models/
│   │   └── finding.py
│   └── results/
│       └── scan_results.py
│
├── demo_api/
│   ├── main.py
│   └── __init__.py
│
├── diagrams/
├── screenshots/
└── reports/

19. Security and Responsible Testing

SentinelAPI should only be used against APIs that you own or are
explicitly authorized to test.

The controlled demo API is recommended for demonstrations and
development testing.

20. Limitations

It does not detect every possible API vulnerability.

Some findings require manual verification.

Complex authentication and authorization flows may require
additional configuration.

Automated scanning does not replace a complete security assessment.

AI-assisted explanations depend on the scan information available to
the Copilot.

21. Future Scope

AI-Based Continuous Security Monitoring

Use AI/ML to monitor API behavior, learn normal activity, and detect
unusual requests or possible attacks in real time.

Automatic Vulnerability Detection and Fix Suggestions

Automatically identify possible causes and suggest fixes. Future
versions could generate secure code or configuration changes for
developer review.

Software Development Integration

Integrate SentinelAPI with GitHub, GitLab, CI/CD pipelines, and cloud
platforms so APIs can be security checked before production.

Real-Time API Protection

Extend the platform to monitor API requests, detect suspicious behavior,
block potentially harmful requests, and alert security teams.

22. Team Contributions

Neha Sharma --- Team Leader

Team coordination

Project management

Overall project direction

Manish Choudhary --- Backend Developer

Backend and scanner development

API testing logic

Security finding implementation

Backend integration

Aryan Yadav --- Frontend Developer

User interface

Dashboard presentation

Frontend integration

Jaishree Dholpuriya --- Presentation

Presentation preparation

Project explanation

Demo presentation support

23. Hackathon Deliverables

GitHub Repository

Source Code

Architecture Diagram

Deployment / Demo Link

README Documentation

Team Contribution Details

Presentation

Demo Screenshots

Live Product Demonstration

24. Demo Flow

User
  |
  v
OpenAPI / Swagger Input
  |
  v
Endpoint Discovery
  |
  v
Security Scan
  |
  v
Vulnerability Findings
  |
  v
Severity + Evidence
  |
  v
Security Report
  |
  v
AI Security Copilot
  |
  v
Remediation Guidance

25. Project Links

GitHub Repository:

https://github.com/ManishChoudhary7/SentinelAPI

Clone Repository

gh repo clone ManishChoudhary7/SentinelAPI

26. Conclusion

SentinelAPI combines OpenAPI/Swagger-based endpoint discovery, automated
API security testing, vulnerability analysis, severity assessment,
evidence, reporting, and AI-assisted security guidance in one
developer-friendly workflow.

The goal is to help developers identify API security risks earlier and
understand how those findings can be addressed.

27. Disclaimer

SentinelAPI is a security testing and educational project. Use it only
against APIs for which you have proper authorization.

Team: Innov Coders