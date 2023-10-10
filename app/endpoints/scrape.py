from fastapi import APIRouter, HTTPException, Depends
from playwright.async_api import Page
from dotenv import load_dotenv
from ..config import EMAIL, PASSWORD

router = APIRouter()

def get_browser():
    from ..main import browser 
    return browser

async def login_to_linkedin(page: Page):

    await page.goto('https://www.linkedin.com/login')

    await page.fill('input[name="session_key"]', EMAIL)
    await page.fill('input[name="session_password"]', PASSWORD)

    await page.click("button[type='submit']")



@router.get('/')
async def return_html(url: str, browser = Depends(get_browser)):

    page = await browser.new_page()
    print(page)
    try:
        await login_to_linkedin(page)
        await page.goto(url)
        await page.wait_for_selector('h1.text-heading-xlarge', timeout=30000)

        name_element = page.locator('h1.text-heading-xlarge')
        name = await name_element.inner_text()

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    finally:
        await page.close()
    
    return {'name': name}

