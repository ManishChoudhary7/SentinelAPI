from backend.results.report_generator import generate_json_report
from backend.scanner.request_engine import test_bola, set_base_url, get_base_url
from backend.scanner.exposure_scanner import scan_data_exposure
from backend.scanner.auth_scanner import scan_authentication
from backend.scanner.rate_limit_scanner import scan_rate_limit
from backend.results.scan_results import get_findings, clear_findings


DEFAULT_BASE_URL = "http://127.0.0.1:8000"


def run_full_scan(base_url=None):
    """
    SentinelAPI ka complete security scan run karta hai.

    base_url:
        Target API ka authorized/sandbox URL.
        Agar URL nahi diya gaya to local demo API use hogi.
    """

    # ------------------------------------------------
    # Target API configure karo
    # ------------------------------------------------

    if base_url:
        set_base_url(base_url)
    else:
        set_base_url(DEFAULT_BASE_URL)

    target = get_base_url()

    # ------------------------------------------------
    # Previous scan results clear karo
    # ------------------------------------------------

    clear_findings()

    print("\n")
    print("=" * 60)
    print("              🛡 SENTINEL API")
    print("          ZERO-TRUST API SCANNER")
    print("=" * 60)

    print("\nStarting security scan...")
    print("Target:", target)

    # ------------------------------------------------
    # 1. BOLA / IDOR
    # ------------------------------------------------

    print("\n\n[1/4] Running BOLA / IDOR Scanner...")

    try:
        test_bola()
    except Exception as error:
        print("BOLA scanner error:", error)

    # ------------------------------------------------
    # 2. Data Exposure
    # ------------------------------------------------

    print("\n\n[2/4] Running Data Exposure Scanner...")

    try:
        scan_data_exposure()
    except Exception as error:
        print("Data Exposure scanner error:", error)

    # ------------------------------------------------
    # 3. Authentication
    # ------------------------------------------------

    print("\n\n[3/4] Running Authentication Scanner...")

    try:
        scan_authentication()
    except Exception as error:
        print("Authentication scanner error:", error)

    # ------------------------------------------------
    # 4. Rate Limit
    # ------------------------------------------------

    print("\n\n[4/4] Running Rate Limit Scanner...")

    try:
        scan_rate_limit()
    except Exception as error:
        print("Rate Limit scanner error:", error)

    # ------------------------------------------------
    # Final Security Report
    # ------------------------------------------------

    findings = get_findings()

    high_count = 0
    medium_count = 0
    low_count = 0

    for finding in findings:

        if finding.severity == "HIGH":
            high_count += 1

        elif finding.severity == "MEDIUM":
            medium_count += 1

        elif finding.severity == "LOW":
            low_count += 1

    print("\n\n")
    print("=" * 60)
    print("             FINAL SECURITY REPORT")
    print("=" * 60)

    print(f"\nTarget API           : {target}")
    print(f"Total Vulnerabilities : {len(findings)}")
    print(f"HIGH Severity         : {high_count}")
    print(f"MEDIUM Severity       : {medium_count}")
    print(f"LOW Severity          : {low_count}")

    print("\n" + "=" * 60)
    print("                 FINDINGS")
    print("=" * 60)

    for index, finding in enumerate(findings, start=1):

        print(f"\n[{index}] {finding.title}")
        print("-" * 50)

        print(f"Type           : {finding.vulnerability_type}")
        print(f"Severity       : {finding.severity}")
        print(f"Endpoint       : {finding.endpoint}")
        print(f"Description    : {finding.description}")
        print(f"Evidence       : {finding.evidence}")
        print(f"Recommendation : {finding.recommendation}")

    # ------------------------------------------------
    # Generate JSON report
    # ------------------------------------------------

    generate_json_report()

    print("\n")
    print("=" * 60)
    print("             SCAN COMPLETED")
    print("=" * 60)

    return {
        "target": target,
        "total_vulnerabilities": len(findings),
        "high": high_count,
        "medium": medium_count,
        "low": low_count,
        "findings": findings
    }


if __name__ == "__main__":
    run_full_scan()
