import json

from backend.scanner.request_engine import send_request
from backend.models.finding import Finding
from backend.results.scan_results import add_finding


# Fields that may contain sensitive information
SENSITIVE_FIELDS = [
    "password",
    "password_hash",
    "api_key",
    "token",
    "secret",
    "credit_card",
    "ssn",
    "authorization",
    "access_token",
    "refresh_token"
]


def _find_sensitive_fields(data, parent_key=""):
    """
    JSON response ke andar recursively sensitive fields search karta hai.
    Nested objects aur lists dono support karta hai.
    """

    found_fields = []

    if isinstance(data, dict):

        for key, value in data.items():

            key_lower = str(key).lower()

            if any(
                sensitive in key_lower
                for sensitive in SENSITIVE_FIELDS
            ):
                field_name = (
                    f"{parent_key}.{key}"
                    if parent_key
                    else str(key)
                )

                found_fields.append(field_name)

            # Nested object check
            if isinstance(value, (dict, list)):

                nested_key = (
                    f"{parent_key}.{key}"
                    if parent_key
                    else str(key)
                )

                found_fields.extend(
                    _find_sensitive_fields(
                        value,
                        nested_key
                    )
                )

    elif isinstance(data, list):

        for index, item in enumerate(data):

            if isinstance(item, (dict, list)):

                found_fields.extend(
                    _find_sensitive_fields(
                        item,
                        f"{parent_key}[{index}]"
                    )
                )

    return found_fields


def scan_data_exposure(
    endpoint="/users/1",
    method="GET",
    token="token-user-1"
):
    """
    Given endpoint par response data exposure test karta hai.

    endpoint:
        API ka authorized/sandbox endpoint.

    method:
        HTTP method.

    token:
        Optional authentication token.
    """

    print("\n" + "=" * 50)
    print("       DATA EXPOSURE SECURITY TEST")
    print("=" * 50)

    result = send_request(
        method=method,
        path=endpoint,
        token=token
    )

    print("\nEndpoint:")
    print(result["url"])

    print("\nStatus:")
    print(result["status_code"])

    # Request fail hone par stop
    if result["status_code"] == 0:

        print("\n❌ Unable to connect to target API.")

        if result.get("error"):
            print("Error:", result["error"])

        return None

    # API response ko JSON mein convert karo
    try:
        data = json.loads(result["response"])

    except json.JSONDecodeError:

        print("\nResponse JSON format mein nahi hai.")
        return None

    # Sensitive fields recursively search karo
    found_fields = _find_sensitive_fields(data)

    # Duplicate fields remove karo
    found_fields = list(dict.fromkeys(found_fields))

    # Vulnerability found
    if found_fields:

        finding = Finding(
            title="Sensitive Data Exposure",
            vulnerability_type="Excessive Data Exposure",
            severity="HIGH",
            endpoint=f"{method.upper()} {endpoint}",
            description=(
                "The API response contains fields that may "
                "contain sensitive information."
            ),
            evidence=(
                "Potentially sensitive fields detected: "
                + ", ".join(found_fields)
            ),
            recommendation=(
                "Return only the fields required by the client "
                "and remove sensitive information from API responses."
            )
        )

        print("\n🚨 VULNERABILITY FOUND")
        print("-" * 40)

        print("Type:")
        print(finding.vulnerability_type)

        print("\nSeverity:")
        print(finding.severity)

        print("\nSensitive Fields:")
        print(", ".join(found_fields))

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

    print("\n✅ NO SENSITIVE DATA EXPOSURE DETECTED")

    return None


if __name__ == "__main__":

    scan_data_exposure()
