from typing import Any
from .base import BaseClient

class ScannerClient(BaseClient):
    def health(self):
        return self._request("GET", "/health")

    def list_assets(self, **params: Any):
        return self._request("GET", "/assets", params=params or None)

    def get_asset(self, asset_id: int):
        return self._request("GET", f"/assets/{asset_id}")

    def create_asset(self, payload: dict):
        return self._request("POST", "/assets", json=payload)

    def update_asset(self, asset_id: int, payload: dict):
        return self._request("PUT", f"/assets/{asset_id}", json=payload)

    def deactivate_asset(self, asset_id: int):
        return self._request("DELETE", f"/assets/{asset_id}")

    def run_scan(self, payload: dict):
        return self._request("POST", "/scans", json=payload)

    def list_scans(self, **params: Any):
        return self._request("GET", "/scans", params=params or None)

    def get_scan(self, scan_id: int):
        return self._request("GET", f"/scans/{scan_id}")
