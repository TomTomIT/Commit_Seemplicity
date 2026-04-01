from playwright.sync_api import expect


def test_dashboard_page_loads(page):
    page.goto("http://localhost:8000/")
    page.wait_for_load_state("networkidle")
    expect(page.locator("body")).to_be_visible()
    expect(page.locator("text=Vulnerability Dashboard")).to_be_visible()
    expect(page.locator("#findings-table")).to_be_visible()


def test_update_finding_status_via_ui(page, dashboard_client, finding_payload):
    create_response = dashboard_client.create_finding(finding_payload)
    assert create_response.status_code == 201
    finding_id = create_response.json()["id"]

    page.goto("http://localhost:8000/")
    page.wait_for_load_state("networkidle")

    row = page.locator("#findings-table tr", has=page.locator(f"text=#{finding_id}"))
    expect(row).to_be_visible()

    row.locator("select.status-select").select_option("confirmed")
    expect(page.locator("#findings-message")).to_contain_text(f"Finding #{finding_id} updated to confirmed")

    page.get_by_role("button", name="Refresh").click()
    page.wait_for_load_state("networkidle")

    refreshed_row = page.locator("#findings-table tr", has=page.locator(f"text=#{finding_id}"))
    expect(refreshed_row).to_be_visible()
    expect(refreshed_row).to_contain_text("confirmed")
