import time

def test_run_scan_creates_findings(scanner_client, dashboard_client, db_client, asset_payload):
    asset_resp = scanner_client.create_asset(asset_payload)
    assert asset_resp.status_code == 201, asset_resp.text
    asset = asset_resp.json()
    asset_id = asset["id"]

    vuln_resp = dashboard_client.list_vulnerabilities()
    assert vuln_resp.status_code == 200, vuln_resp.text
    vulnerabilities = vuln_resp.json()
    assert isinstance(vulnerabilities, list)
    assert len(vulnerabilities) >= 1

    vuln_ids = [vulnerabilities[0]["id"]]
    if len(vulnerabilities) > 1:
        vuln_ids.append(vulnerabilities[1]["id"])

    before_count = db_client.count_findings_for_asset(asset_id)

    scan_resp = scanner_client.run_scan(
        {
            "asset_id": asset_id,
            "scanner_name": "pytest-scanner",
            "vulnerability_ids": vuln_ids,
        }
    )
    assert scan_resp.status_code == 201, scan_resp.text
    scan_data = scan_resp.json()
    assert scan_data["asset_id"] == asset_id
    assert scan_data["scanner_name"] == "pytest-scanner"
    assert scan_data["findings_count"] == len(vuln_ids)

    time.sleep(1)

    get_scan_resp = scanner_client.get_scan(scan_data["id"])
    assert get_scan_resp.status_code == 200, get_scan_resp.text

    after_count = db_client.count_findings_for_asset(asset_id)
    assert after_count >= before_count + len(vuln_ids)

def test_assets_first_page_should_include_first_created_asset(scanner_client, asset_payload):
    create_resp = scanner_client.create_asset(asset_payload)
    assert create_resp.status_code == 201, create_resp.text
    asset = create_resp.json()

    list_resp = scanner_client.list_assets(page=1, per_page=1)
    assert list_resp.status_code == 200, list_resp.text
    body = list_resp.json()
    assert body["items"], body
    assert body["items"][0]["id"] == asset["id"], body


def test_repeated_scan_should_not_create_duplicate_findings(scanner_client, dashboard_client, db_client, asset_payload):
    asset_resp = scanner_client.create_asset(asset_payload)
    assert asset_resp.status_code == 201, asset_resp.text
    asset_id = asset_resp.json()["id"]

    vuln_resp = dashboard_client.list_vulnerabilities()
    assert vuln_resp.status_code == 200, vuln_resp.text
    vuln_id = vuln_resp.json()[0]["id"]

    before = db_client.count_findings_for_asset_vulnerability(asset_id, vuln_id)

    payload = {
        "asset_id": asset_id,
        "scanner_name": "pytest-scanner",
        "vulnerability_ids": [vuln_id],
    }

    first_scan = scanner_client.run_scan(payload)
    assert first_scan.status_code == 201, first_scan.text

    second_scan = scanner_client.run_scan(payload)
    assert second_scan.status_code == 201, second_scan.text

    after = db_client.count_findings_for_asset_vulnerability(asset_id, vuln_id)
    assert after == before + 1
