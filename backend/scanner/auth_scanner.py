from backend.scanner.request_engine import send_request
from backend.models.finding import Finding
from backend.results.scan_results import add_finding


def scan_authentication(
    endpoint="/profile",
    method="GET"
):
    """
    Checks whether an endpoint returns a successful response
    without an authentication token.

    IMPORTANT:
    Use this scanner only against an authorized sandbox/test API.
    """

    print("\n" + "=" * 50)
    print("       AUTHENTICATION SECURITY TEST")
    print("=" * 50)

    # Request WITHOUT authentication token
    result = send_request(
        method=method,
        path=endpoint,
        token=None
    )

    print("\nEndpoint:")
    print(result["url"])

    print("\nStatus:")
    print(result["status_code"])

    # Connection/request failure
    if result["status_code"] == 0:

        print("\n❌ Unable to connect to target API.")

        if result.get("error"):
            print("Error:", result["error"])

        return None

    # If API returns 200 without authentication,
    # it may be missing authentication protection.
    if result["status_code"] == 200:

        finding = Finding(
            title="Missing Authentication",
            vulnerability_type="Authentication Bypass",
            severity="HIGH",
            endpoint=f"{method.upper()} {endpoint}",
            description=(
                "The endpoint returned a successful response "
                "without requiring authentication."
            ),
            evidence=(
                f"{method.upper()} {endpoint} was requested "
                "without an Authorization header and returned "
                f"HTTP {result['status_code']}."
            ),
            recommendation=(
                "Require valid authentication before allowing "
                "access to protected resources."
            )
        )

        print("\n🚨 VULNERABILITY FOUND")
        print("-" * 40)

        print("Type:")
        print(finding.vulnerability_type)

        print("\nSeverity:")
        print(finding.severity)

        print("\nEndpoint:")
        print(finding.endpoint)

        print("\nDescription:")
        print(finding.description)

        print("\nEvidence:")
        print(finding.evidence)

        print("\nRecommendation:")
        print(finding.recommendation)

        # Save finding to central results
        add_finding(finding)

        print("\n✅ Finding saved successfully.")

        return finding

    print("\n✅ AUTHENTICATION CHECK PASSED")

    return None


if __name__ == "__main__":

    scan_authentication()
