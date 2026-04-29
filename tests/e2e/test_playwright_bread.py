from uuid import uuid4

import pytest


@pytest.mark.e2e
def test_bread_positive_flow(page, fastapi_server):
    base_url = fastapi_server.rstrip("/")
    username = f"bread_{uuid4().hex[:10]}"
    email = f"{username}@example.com"
    password = "SecurePass123!"

    # Register via UI
    page.goto(f"{base_url}/register")
    page.fill("#username", username)
    page.fill("#email", email)
    page.fill("#first_name", "Bread")
    page.fill("#last_name", "User")
    page.fill("#password", password)
    page.fill("#confirm_password", password)
    page.click("button[type='submit']")
    page.wait_for_url("**/login")

    # Login via UI
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("#loginForm button[type='submit']")
    page.wait_for_url("**/dashboard")

    # Add (POST /calculations)
    page.select_option("#calcType", "addition")
    page.fill("#calcInputs", "2, 3, 4")
    page.click("#calculationForm button[type='submit']")
    page.wait_for_selector("text=Calculation complete")

    # Browse (GET /calculations)
    page.wait_for_selector("#calculationsTable tr")
    page.locator("#calculationsTable tr").filter(has_text="Addition").first.wait_for()

    # Read (GET /calculations/{id})
    first_view_link = page.locator("a[href^='/dashboard/view/']").first
    first_view_link.click()
    page.wait_for_url("**/dashboard/view/**")
    calc_id = page.url.rstrip("/").split("/")[-1]
    page.wait_for_selector("#calculationCard:not(.hidden)")

    # Edit (PUT /calculations/{id})
    page.click("#editLink")
    page.wait_for_url("**/dashboard/edit/**")
    page.fill("#calcInputs", "10, 5")
    page.click("#editCalculationForm button[type='submit']")
    page.wait_for_url("**/dashboard/view/**")
    page.wait_for_selector("text=15")

    # Delete (DELETE /calculations/{id})
    page.once("dialog", lambda dialog: dialog.accept())
    page.click("#deleteBtn")
    page.wait_for_url("**/dashboard")
    assert page.locator(f"a[href='/dashboard/view/{calc_id}']").count() == 0


@pytest.mark.e2e
def test_bread_negative_invalid_input(page, fastapi_server):
    base_url = fastapi_server.rstrip("/")
    username = f"neg_{uuid4().hex[:10]}"
    email = f"{username}@example.com"
    password = "SecurePass123!"

    page.goto(f"{base_url}/register")
    page.fill("#username", username)
    page.fill("#email", email)
    page.fill("#first_name", "Neg")
    page.fill("#last_name", "Case")
    page.fill("#password", password)
    page.fill("#confirm_password", password)
    page.click("button[type='submit']")
    page.wait_for_url("**/login")

    page.fill("#username", username)
    page.fill("#password", password)
    page.click("#loginForm button[type='submit']")
    page.wait_for_url("**/dashboard")

    # Invalid token in comma list should be rejected on client side.
    page.fill("#calcInputs", "1, bad, 3")
    page.click("#calculationForm button[type='submit']")
    page.wait_for_selector("#errorAlert:not(.hidden)")
    assert "Invalid number" in page.locator("#errorMessage").inner_text()

    # Division by zero should be blocked on client side.
    page.select_option("#calcType", "division")
    page.fill("#calcInputs", "100, 0")
    page.click("#calculationForm button[type='submit']")
    page.wait_for_selector("#errorAlert:not(.hidden)")
    assert "Division by zero" in page.locator("#errorMessage").inner_text()


@pytest.mark.e2e
def test_bread_negative_unauthorized_and_not_found(page, fastapi_server):
    base_url = fastapi_server.rstrip("/")

    # Unauthorized dashboard access should redirect to login.
    page.goto(f"{base_url}/dashboard")
    page.wait_for_url("**/login")

    # Login and request a non-existent calculation to verify not-found handling.
    username = f"nf_{uuid4().hex[:10]}"
    email = f"{username}@example.com"
    password = "SecurePass123!"

    page.goto(f"{base_url}/register")
    page.fill("#username", username)
    page.fill("#email", email)
    page.fill("#first_name", "Not")
    page.fill("#last_name", "Found")
    page.fill("#password", password)
    page.fill("#confirm_password", password)
    page.click("button[type='submit']")
    page.wait_for_url("**/login")

    page.fill("#username", username)
    page.fill("#password", password)
    page.click("#loginForm button[type='submit']")
    page.wait_for_url("**/dashboard")

    page.goto(f"{base_url}/dashboard/view/00000000-0000-0000-0000-000000000000")
    page.wait_for_selector("#errorState:not(.hidden)")
    page.wait_for_selector("text=Calculation Not Found")
