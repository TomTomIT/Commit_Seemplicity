def test_create_finding_persists_to_db(dashboard_client, db_client, finding_payload):
    create_resp = dashboard_client.create_finding(finding_payload)
    assert create_resp.status_code == 201, create_resp.text
    finding_id = create_resp.json()["id"]

    db_finding = db_client.get_finding(finding_id)
    assert db_finding is not None
    assert db_finding["id"] == finding_id
    assert db_finding["asset_id"] == finding_payload["asset_id"]
    assert db_finding["vulnerability_id"] == finding_payload["vulnerability_id"]
    assert db_finding["scanner"] == finding_payload["scanner"]
    assert db_finding["notes"] == finding_payload["notes"]
    assert db_finding["is_dismissed"] is False

def test_dismiss_finding_sets_is_dismissed_true(dashboard_client, db_client, finding_payload):
    create_resp = dashboard_client.create_finding(finding_payload)
    assert create_resp.status_code == 201, create_resp.text
    finding_id = create_resp.json()["id"]

    dismiss_resp = dashboard_client.dismiss_finding(finding_id)
    assert dismiss_resp.status_code == 204, dismiss_resp.text

    db_finding = db_client.get_finding(finding_id)
    assert db_finding is not None
    assert db_finding["is_dismissed"] is True

def test_finding_references_existing_asset_and_vulnerability(dashboard_client, db_client, finding_payload):
    create_resp = dashboard_client.create_finding(finding_payload)
    assert create_resp.status_code == 201, create_resp.text
    finding_id = create_resp.json()["id"]

    db_finding = db_client.get_finding(finding_id)
    assert db_finding is not None

    db_asset = db_client.get_asset(db_finding["asset_id"])
    db_vulnerability = db_client.get_vulnerability(db_finding["vulnerability_id"])

    assert db_asset is not None
    assert db_vulnerability is not None
    assert 0 <= float(db_vulnerability["cvss_score"]) <= 10
