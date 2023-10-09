from playwright.sync_api import Page, expect
from fastapi.testclient import TestClient
from app.main import app

import sys
sys.path.append('/home/sandeep/Desktop/ankamala/fastapi_playwright')


client = TestClient(app)

def test_get_started_link(page: Page):
    page.goto("https://playwright.dev/")

    # Click the get started link.
    page.get_by_role("link", name="Get started").click()

    # Expects page to have a heading with the name of Installation.
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()

def test_endpoints(page:Page):
    response = client.get('/')
    assert response.status_code == 200

    page.goto("http://localhost:8000/")
        
    content = page.content()


        
    assert "hello" in content
    assert "world" in content
        
       