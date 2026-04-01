# BUG_REPORT.md

## 1. Dismissed finding remains accessible via detail endpoint
**Severity:** Medium

**Steps to reproduce**
1. Create a finding via `POST /findings`
2. Dismiss it via `DELETE /findings/{id}`
3. Request `GET /findings/{id}`

**Expected behavior**
Dismissed finding should no longer be returned by the detail endpoint.

**Actual behavior**
Endpoint still returns `200 OK` with dismissed finding details.

## 2. Invalid finding status transitions are allowed
**Severity:** Medium

**Steps to reproduce**
1. Create a finding
2. Update its status to `resolved`
3. Update it again back to `open`

**Expected behavior**
Resolved findings should not be allowed to transition back to `open` without an explicit reopen workflow.

**Actual behavior**
API accepts the status change and returns success.

## 3. Asset pagination skips the first record
**Severity:** High

**Steps to reproduce**
1. Create a new asset
2. Call `GET /assets?page=1&per_page=1`

**Expected behavior**
The first page with page size 1 should return the first asset in sorted order.

**Actual behavior**
The first asset is skipped because pagination offset is off by one.

## 4. Repeated scans create duplicate findings
**Severity:** High

**Steps to reproduce**
1. Create an asset
2. Run a scan with a vulnerability id
3. Run the same scan again for the same asset and vulnerability

**Expected behavior**
System should deduplicate existing findings or enforce uniqueness.

**Actual behavior**
Duplicate findings are created for the same asset and vulnerability pair.


## TEST OUTPUT

platform win32 -- Python 3.11.9, pytest-7.4.3, pluggy-1.6.0 -- 
cachedir: .pytest_cache
rootdir: 
configfile: pytest.ini
plugins: base-url-2.1.0, playwright-0.4.3
collected 15 items

tests/test_dashboard_api.py::test_dashboard_health PASSED
tests/test_dashboard_api.py::test_findings_create_read_update_dismiss_flow PASSED
tests/test_dashboard_api.py::test_update_finding_status_rejects_invalid_status PASSED
tests/test_dashboard_api.py::test_get_non_existing_finding_returns_404 PASSED
tests/test_dashboard_api.py::test_search_findings_returns_200 PASSED
tests/test_dashboard_api.py::test_dismissed_finding_should_not_be_accessible FAILED
tests/test_dashboard_api.py::test_resolved_finding_should_not_transition_back_to_open FAILED
tests/test_database_validation.py::test_create_finding_persists_to_db PASSED
tests/test_database_validation.py::test_dismiss_finding_sets_is_dismissed_true PASSED
tests/test_database_validation.py::test_finding_references_existing_asset_and_vulnerability PASSED
tests/test_integration.py::test_run_scan_creates_findings PASSED
tests/test_integration.py::test_assets_first_page_should_include_first_created_asset FAILED
tests/test_integration.py::test_repeated_scan_should_not_create_duplicate_findings FAILED
tests/test_ui_smoke.py::test_dashboard_page_loads[chromium] PASSED
tests/test_ui_smoke.py::test_update_finding_status_via_ui[chromium] PASSED

======================================================================================================== FAILURES ========================================================================================================
____________________________________________________________________________________ test_dismissed_finding_should_not_be_accessible _____________________________________________________________________________________
tests\test_dashboard_api.py:71: in test_dismissed_finding_should_not_be_accessible
    assert get_resp.status_code == 404, get_resp.text
E   AssertionError: {"id":143,"asset_id":1,"vulnerability_id":1,"status":"open","detected_at":"2026-04-01T08:53:34.139518","resolved_at":null,"scanner":"pytest","notes":"qa-test-1b619b5a","is_dismissed":true,"vulnerability":{"id":1,"cve_id":"CVE-2021-44228","title":"Log4Shell - Remote Code Execution in Apache Log4j","description":"Apache Log4j2 allows remote code execution via crafted log messages using JNDI lookups.","severity":"critical","cvss_score":10.0,"published_date":"2021-12-10T00:00:00","created_at":"2026-04-01T06:47:31.462989"},"asset_hostname":"prod-web-01"}
E   assert 200 == 404
E    +  where 200 = <Response [200]>.status_code
________________________________________________________________________________ test_resolved_finding_should_not_transition_back_to_open ________________________________________________________________________________
tests\test_dashboard_api.py:89: in test_resolved_finding_should_not_transition_back_to_open
    assert reopen_resp.status_code in (400, 409, 422), reopen_resp.text
E   AssertionError: {"id":144,"asset_id":1,"vulnerability_id":1,"status":"open","detected_at":"2026-04-01T08:53:34.315644","resolved_at":null,"scanner":"pytest","notes":"reopened by pytest","is_dismissed":false}
E   assert 200 in (400, 409, 422)
E    +  where 200 = <Response [200]>.status_code
_______________________________________________________________________________ test_assets_first_page_should_include_first_created_asset ________________________________________________________________________________
tests\test_integration.py:51: in test_assets_first_page_should_include_first_created_asset
    assert body["items"][0]["id"] == asset["id"], body
E   AssertionError: {'items': [{'asset_type': 'server', 'created_at': '2026-04-01T06:47:31.452611', 'environment': 'production', 'hostname': 'prod-web-02', ...}], 'page': 1, 'pages': 47, 'per_page': 1, ...}
E   assert 2 == 54
________________________________________________________________________________ test_repeated_scan_should_not_create_duplicate_findings _________________________________________________________________________________
tests\test_integration.py:78: in test_repeated_scan_should_not_create_duplicate_findings
    assert after == before + 1
E   assert 2 == (0 + 1)
========================================================================================================= PASSES =========================================================================================================
================================================================================================ short test summary info =================================================================================================
PASSED tests/test_dashboard_api.py::test_dashboard_health
PASSED tests/test_dashboard_api.py::test_findings_create_read_update_dismiss_flow
PASSED tests/test_dashboard_api.py::test_update_finding_status_rejects_invalid_status
PASSED tests/test_dashboard_api.py::test_get_non_existing_finding_returns_404
PASSED tests/test_dashboard_api.py::test_search_findings_returns_200
PASSED tests/test_database_validation.py::test_create_finding_persists_to_db
PASSED tests/test_database_validation.py::test_dismiss_finding_sets_is_dismissed_true
PASSED tests/test_database_validation.py::test_finding_references_existing_asset_and_vulnerability
PASSED tests/test_integration.py::test_run_scan_creates_findings
PASSED tests/test_ui_smoke.py::test_dashboard_page_loads[chromium]
PASSED tests/test_ui_smoke.py::test_update_finding_status_via_ui[chromium]
FAILED tests/test_dashboard_api.py::test_dismissed_finding_should_not_be_accessible - AssertionError: {"id":143,"asset_id":1,"vulnerability_id":1,"status":"open","detected_at":"2026-04-01T08:53:34.139518","resolved_at":null,"scanner":"pytest","notes":"qa-test-1b619b5a","is_dismissed":true,"vulnerabi...
FAILED tests/test_dashboard_api.py::test_resolved_finding_should_not_transition_back_to_open - AssertionError: {"id":144,"asset_id":1,"vulnerability_id":1,"status":"open","detected_at":"2026-04-01T08:53:34.315644","resolved_at":null,"scanner":"pytest","notes":"reopened by pytest","is_dismissed":false}
FAILED tests/test_integration.py::test_assets_first_page_should_include_first_created_asset - AssertionError: {'items': [{'asset_type': 'server', 'created_at': '2026-04-01T06:47:31.452611', 'environment': 'production', 'hostname': 'prod-web-02', ...}], 'page': 1, 'pages': 47, 'per_page': 1, ...}
FAILED tests/test_integration.py::test_repeated_scan_should_not_create_duplicate_findings - assert 2 == (0 + 1)
============================================================================================== 4 failed, 11 passed in 6.50s ==============================================================================================