import httpx

from backend.models.finding import Finding
from backend.results.scan_results import add_finding
from backend.results.scan_results import get_findings


# Default target for the local SentinelAPI demo
BASE_URL = "http://127.0.0.1:8000"


def set_base_url(base_url):
    """
    Scanner ka target API URL dynamically set karta hai.
    Example:
        set_base_url("http://127.0.0.1:8000")
    """
    global BASE_URL

    if not base_url:
        return

    BASE_URL = base_url.rstrip("/")


def get_base_url():
    """
    Current target API URL return karta hai.
    """
    return BASE_URL


def send_request(method, path, token=None, headers=None, params=None, json_data=None):
    """
    Target API ko HTTP request bhejta hai.

    method      -> GET, POST, PUT, DELETE, PATCH
    path        -> /users/1
    token       -> optional Bearer token
    headers     -> optional custom headers
    params      -> optional query parameters
    json_data   -> optional JSON request body
    """

    # Agar complete URL diya gaya hai to wahi use karo,
    # warna configured BASE_URL ke saath path join karo.
    if path.startswith("http://") or path.startswith("https://"):
        url = path
    else:
        if not path.startswith("/"):
            path = "/" + path

        url = BASE_URL + path

    request_headers = {}

    if headers:
        request_headers.update(headers)

    # Authentication token available hai to Authorization header add karo
    if token:
        request_headers["Authorization"] = f"Bearer {token}"

    try:
        response = httpx.request(
            method=method.upper(),
            url=url,
            headers=request_headers,
            params=params,
            json=json_data,
            timeout=10.0
        )

        return {
            "method": method.upper(),
            "url": str(response.url),
            "status_code": response.status_code,
            "response": response.text,
            "headers": dict(response.headers)
        }

    except httpx.RequestError as error:
        return {
            "method": method.upper(),
            "url": url,
            "status_code": 0,
            "response": "",
            "headers": {},
            "error": str(error)
        }


def test_bola(user_id=1, other_user_id=2, token="token-user-1"):
    """
    BOLA / IDOR vulnerability test karta hai.

    IMPORTANT:
    Ye test tabhi use karo jab authorized sandbox/test API mein
    resource IDs aur test authentication available ho.
    """

    print("\n" + "=" * 50)
    print("        BOLA / IDOR SECURITY TEST")
    print("=" * 50)

    normal_path = f"/users/{user_id}"
    modified_path = f"/users/{other_user_id}"

    # ------------------------------------------------
    # STEP 1: User 1 apna resource access karta hai
    # ------------------------------------------------

    normal = send_request(
        method="GET",
        path=normal_path,
        token=token
    )

    print("\n[1] NORMAL REQUEST")
    print("-" * 30)
    print("URL:", normal["url"])
    print("Status:", normal["status_code"])
    print("Response:", normal["response"])

    # ------------------------------------------------
    # STEP 2: User 1, doosre user ka resource access karta hai
    # ------------------------------------------------

    modified = send_request(
        method="GET",
        path=modified_path,
        token=token
    )

    print("\n[2] MODIFIED REQUEST")
    print("-" * 30)
    print("URL:", modified["url"])
    print("Status:", modified["status_code"])
    print("Response:", modified["response"])

    # ------------------------------------------------
    # STEP 3: BOLA vulnerability check
    # ------------------------------------------------

    if modified["status_code"] == 200:

        finding = Finding(
            title="Broken Object Level Authorization",
            vulnerability_type="BOLA / IDOR",
            severity="HIGH",
            endpoint=f"GET /users/{{user_id}}",
            description=(
                "An authenticated user was able to access "
                "another user's resource by changing the "
                "object identifier."
            ),
            evidence=(
                f"Authenticated user token accessed "
                f"{modified_path} and the API returned "
                f"HTTP 200."
            ),
            recommendation=(
                "Implement server-side object ownership "
                "authorization for every requested resource."
            )
        )

        add_finding(finding)

        print("\n" + "!" * 50)
        print("🚨 VULNERABILITY FOUND")
        print("!" * 50)

        print("\nTitle:")
        print(finding.title)

        print("\nType:")
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

        print("\n✅ Finding saved successfully.")
        print("Total findings stored:", len(get_findings()))

        return finding

    print("\n" + "=" * 50)
    print("✅ BOLA / IDOR NOT DETECTED")
    print("=" * 50)

    return None


# ------------------------------------------------
# PROGRAM START
# ------------------------------------------------

if __name__ == "__main__":

    # Default local demo API test
    test_bola()
