from fastapi import APIRouter, HTTPException, Depends, Body
from playwright.async_api import Page
import asyncio
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



async def return_html(url: str, page: Page):

    await page.goto(url)
    await page.wait_for_selector('h1.text-heading-xlarge', timeout=30000)

    name_element = page.locator('h1.text-heading-xlarge')
    name = await name_element.inner_text()

    return {'url': url, 'name': name}

async def process_profile(url_list, browser):
    page = await browser.new_page()
    try:
        await login_to_linkedin(page)
        results = []
        for url in url_list:
            name = await return_html(url, page)
            results.append(name)
            await asyncio.sleep(3) 
        
        return results
    finally:
        await page.close()



@router.post('/')
async def scrape_profiles(urls= Body(...), browser = Depends(get_browser)):
    results = await process_profile(urls, browser)
    return results



