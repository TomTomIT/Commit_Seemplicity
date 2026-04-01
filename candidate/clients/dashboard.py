from typing import Any
from .base import BaseClient

class DashboardClient(BaseClient):
    def health(self):
        return self._request("GET", "/health")

    def list_findings(self, **params: Any):
        return self._request("GET", "/findings", params=params or None)

    def get_finding(self, finding_id: int):
        return self._request("GET", f"/findings/{finding_id}")

    def create_finding(self, payload: dict):
        return self._request("POST", "/findings", json=payload)

    def update_finding_status(self, finding_id: int, payload: dict):
        return self._request("PUT", f"/findings/{finding_id}/status", json=payload)

    def dismiss_finding(self, finding_id: int):
        return self._request("DELETE", f"/findings/{finding_id}")

    def search_findings(self, query: str):
        return self._request("GET", "/findings/search", params={"q": query})

    def list_vulnerabilities(self, **params: Any):
        return self._request("GET", "/vulnerabilities", params=params or None)

    def get_vulnerability(self, vuln_id: int):
        return self._request("GET", f"/vulnerabilities/{vuln_id}")
