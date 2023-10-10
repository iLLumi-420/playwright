from fastapi import APIRouter, HTTPException
from playwright.sync_api import sync_playwright


router = APIRouter()

@router.get('/')
def return_html(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            page.goto(url)
            content = page.content()
        except Exception as e:
            return HTTPException(status_code=500, detail=str(e))
        finally:
            browser.close()
    
    return {'html': content}