# All detected vulnerabilities will be stored here

scan_results = []


def add_finding(finding):
    """
    Add a vulnerability finding to the scan results.
    """

    scan_results.append(finding)


def get_findings():
    """
    Return all vulnerability findings.
    """

    return scan_results


def clear_findings():
    """
    Clear previous scan results.
    """

    scan_results.clear()