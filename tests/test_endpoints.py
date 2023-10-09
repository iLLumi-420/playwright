from playwright.sync_api import Page, expect
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_get_started_link(page: Page):
    page.goto("https://playwright.dev/")

    python_link = page.locator('a[href="https://playwright.dev/python/docs/intro"]')
    python_link.scroll_into_view_if_needed()

    page.screenshot(path="scoll_to_link.jpg")

    page.click('a[href="https://playwright.dev/python/docs/intro"]')
    page.wait_for_load_state("load")

    page.screenshot(path='new_page.jpg')

    page.go_back()
    page.wait_for_load_state("load")


    page.get_by_role("link", name="Get started").click()

    expect(page.get_by_role("heading", name="Installation")).to_be_visible()


def test_endpoints(page:Page):
    response = client.get('/')
    assert response.status_code == 200

    page.goto("http://localhost:8000/")

    page.screenshot(path="screenshot.jpg")
        
    content = page.content()


        
    assert "hello" in content
    assert "world" in content
        
