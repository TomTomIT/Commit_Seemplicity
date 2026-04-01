def test_dashboard_health(dashboard_client):
    resp = dashboard_client.health()
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"

def test_findings_create_read_update_dismiss_flow(dashboard_client, finding_payload):
    create_resp = dashboard_client.create_finding(finding_payload)
    assert create_resp.status_code == 201, create_resp.text

    created = create_resp.json()
    finding_id = created["id"]
    assert created["asset_id"] == finding_payload["asset_id"]
    assert created["vulnerability_id"] == finding_payload["vulnerability_id"]
    assert created["scanner"] == finding_payload["scanner"]
    assert created["notes"] == finding_payload["notes"]
    assert "status" in created

    get_resp = dashboard_client.get_finding(finding_id)
    assert get_resp.status_code == 200, get_resp.text
    finding = get_resp.json()
    assert finding["id"] == finding_id
    assert finding["asset_id"] == finding_payload["asset_id"]
    assert finding["vulnerability_id"] == finding_payload["vulnerability_id"]
    assert finding["scanner"] == finding_payload["scanner"]
    assert finding["notes"] == finding_payload["notes"]
    assert "vulnerability" in finding
    assert "asset_hostname" in finding

    update_resp = dashboard_client.update_finding_status(
        finding_id,
        {"status": "confirmed", "notes": "verified by pytest"},
    )
    assert update_resp.status_code == 200, update_resp.text
    updated = update_resp.json()
    assert updated["id"] == finding_id
    assert updated["status"] == "confirmed"
    assert updated["notes"] == "verified by pytest"

    dismiss_resp = dashboard_client.dismiss_finding(finding_id)
    assert dismiss_resp.status_code == 204, dismiss_resp.text

def test_update_finding_status_rejects_invalid_status(dashboard_client):
    resp = dashboard_client.update_finding_status(
        1,
        {"status": "definitely_invalid", "notes": "pytest"},
    )
    assert resp.status_code == 400
    assert "Invalid status" in resp.text

def test_get_non_existing_finding_returns_404(dashboard_client):
    resp = dashboard_client.get_finding(99999999)
    assert resp.status_code == 404

def test_search_findings_returns_200(dashboard_client):
    resp = dashboard_client.search_findings("CVE")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list)
    assert len(body) > 0
    assert "cve_id" in body[0]

def test_dismissed_finding_should_not_be_accessible(dashboard_client, finding_payload):
    create_resp = dashboard_client.create_finding(finding_payload)
    assert create_resp.status_code == 201, create_resp.text
    finding_id = create_resp.json()["id"]

    dismiss_resp = dashboard_client.dismiss_finding(finding_id)
    assert dismiss_resp.status_code == 204, dismiss_resp.text

    get_resp = dashboard_client.get_finding(finding_id)
    assert get_resp.status_code == 404, get_resp.text


def test_resolved_finding_should_not_transition_back_to_open(dashboard_client, finding_payload):
    create_resp = dashboard_client.create_finding(finding_payload)
    assert create_resp.status_code == 201, create_resp.text
    finding_id = create_resp.json()["id"]

    resolve_resp = dashboard_client.update_finding_status(
        finding_id,
        {"status": "resolved", "notes": "resolved by pytest"},
    )
    assert resolve_resp.status_code == 200, resolve_resp.text

    reopen_resp = dashboard_client.update_finding_status(
        finding_id,
        {"status": "open", "notes": "reopened by pytest"},
    )
    assert reopen_resp.status_code in (400, 409, 422), reopen_resp.text
