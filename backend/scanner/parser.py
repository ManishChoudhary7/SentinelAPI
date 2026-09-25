import json


def parse_openapi(file_path):
    """
    OpenAPI JSON file ko read karke
    API ke endpoints extract karta hai.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        api_data = json.load(file)

    endpoints = []

    for path, methods in api_data.get("paths", {}).items():

        for method, details in methods.items():

            if method.lower() not in [
                "get",
                "post",
                "put",
                "delete",
                "patch"
            ]:
                continue

            endpoints.append({
                "path": path,
                "method": method.upper(),
                "summary": details.get("summary", ""),
                "parameters": details.get("parameters", [])
            })

    return endpoints


if __name__ == "__main__":

    file_path = "test_api/openapi.json"

    endpoints = parse_openapi(file_path)

    print("\n===== API ENDPOINTS =====\n")

    for endpoint in endpoints:
        print(
            endpoint["method"],
            endpoint["path"]
        )