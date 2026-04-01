import uuid
import pytest
from clients.dashboard import DashboardClient
from clients.scanner import ScannerClient
from db.postgres import PostgresClient
from config import settings

@pytest.fixture(scope="session")
def dashboard_client() -> DashboardClient:
    return DashboardClient(settings.dashboard_api)

@pytest.fixture(scope="session")
def scanner_client() -> ScannerClient:
    return ScannerClient(settings.scanner_api)

@pytest.fixture
def db_client():
    client = PostgresClient()
    yield client
    client.close()

@pytest.fixture
def finding_payload() -> dict:
    return {
        "asset_id": 1,
        "vulnerability_id": 1,
        "scanner": "pytest",
        "notes": f"qa-test-{uuid.uuid4().hex[:8]}",
    }

@pytest.fixture
def asset_payload() -> dict:
    suffix = uuid.uuid4().hex[:6]
    return {
        "hostname": f"pytest-host-{suffix}",
        "ip_address": f"10.0.99.{int(suffix[:2], 16) % 200 + 1}",
        "asset_type": "server",
        "environment": "production",
        "os": "Ubuntu 22.04",
    }
