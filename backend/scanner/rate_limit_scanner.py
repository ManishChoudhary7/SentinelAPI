import time

from backend.scanner.request_engine import send_request
from backend.models.finding import Finding
from backend.results.scan_results import add_finding


def scan_rate_limit(
    endpoint="/login",
    method="POST",
    total_requests=10,
    delay=0.2
):
    """
    Controlled rate-limit test for an authorized sandbox/test API.

    endpoint:
        Target API endpoint, for example /login

    method:
        HTTP method, for example POST

    total_requests:
        Number of controlled requests.

    delay:
        Delay between requests in seconds.
    """

    print("\n" + "=" * 50)
    print("          RATE LIMIT SECURITY TEST")
    print("=" * 50)

    successful_requests = 0
    rate_limited_requests = 0

    print(
        f"\nSending {total_requests} controlled requests..."
    )

    for i in range(1, total_requests + 1):

        result = send_request(
            method=method,
            path=endpoint,
            token=None
        )

        status_code = result["status_code"]

        print(
            f"Request {i}: "
            f"HTTP {status_code}"
        )

        if status_code == 429:
            rate_limited_requests += 1
        elif status_code != 0:
            successful_requests += 1

        # Small delay to avoid stressing the test API
        time.sleep(delay)

    print(
        "\nSuccessful requests:",
        successful_requests
    )

    print(
        "Rate-limited requests:",
        rate_limited_requests
    )

    # If none of the controlled requests received 429,
    # the endpoint may not have rate limiting.
    if rate_limited_requests == 0 and successful_requests == total_requests:

        finding = Finding(
            title="Missing Rate Limiting",
            vulnerability_type="Rate Limit",
            severity="MEDIUM",
            endpoint=f"{method.upper()} {endpoint}",
            description=(
                "The endpoint accepted multiple consecutive "
                "controlled requests without returning HTTP 429."
            ),
            evidence=(
                f"{successful_requests} out of {total_requests} "
                "controlled requests were accepted without "
                "rate limiting."
            ),
            recommendation=(
                "Implement server-side rate limiting for "
                "sensitive or abuse-prone endpoints."
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

        print("\nEvidence:")
        print(finding.evidence)

        print("\nRecommendation:")
        print(finding.recommendation)

        # Save finding to central results
        add_finding(finding)

        print("\n✅ Finding saved successfully.")

        return finding

    elif rate_limited_requests > 0:

        print(
            "\n✅ RATE LIMITING DETECTED"
        )

    else:

        print(
            "\n⚠️ Rate-limit test could not be completed."
        )

    return None


if __name__ == "__main__":

    scan_rate_limit()
