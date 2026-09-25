import json
from backend.results.scan_results import get_findings


def get_poc_request(finding):

    vulnerability_type = finding.vulnerability_type

    if vulnerability_type == "BOLA / IDOR":

        return (
            "GET /users/2 HTTP/1.1\n"
            "Host: 127.0.0.1:8000\n"
            "Authorization: Bearer token-user-1"
        )

    elif vulnerability_type == "Excessive Data Exposure":

        return (
            "GET /users/1 HTTP/1.1\n"
            "Host: 127.0.0.1:8000\n"
            "Authorization: Bearer token-user-1"
        )

    elif vulnerability_type == "Authentication Bypass":

        return (
            "GET /profile HTTP/1.1\n"
            "Host: 127.0.0.1:8000"
        )

    elif vulnerability_type == "Rate Limit":

        return (
            "POST /login?username=rahul&password=1234 HTTP/1.1\n"
            "Host: 127.0.0.1:8000\n"
            "Content-Type: application/json"
        )

    return "No PoC request available."


def generate_json_report():

    findings = get_findings()

    report = {
        "scanner": "SentinelAPI",
        "target": "http://127.0.0.1:8000",
        "total_vulnerabilities": len(findings),
        "findings": []
    }

    for finding in findings:

        report["findings"].append({
            "title": finding.title,
            "vulnerability_type": finding.vulnerability_type,
            "severity": finding.severity,
            "endpoint": finding.endpoint,
            "description": finding.description,
            "evidence": finding.evidence,
            "recommendation": finding.recommendation,
            "poc_request": get_poc_request(finding)
        })

    with open(
        "scan_report.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4
        )

    print("\n✅ JSON report generated successfully.")
    print("📄 File: scan_report.json")