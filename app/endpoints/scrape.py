from fastapi import APIRouter, HTTPException, Depends, Body
from playwright.async_api import Page
import asyncio
from app.config import EMAIL, PASSWORD
from linkedin_api import Linkedin
from urllib.parse import quote


api = Linkedin(EMAIL, PASSWORD)
# profile = api.get_profile('rujan-singh-b18a807a')
# print(profile)

        

def get_reactions(url, urn_id):

    

    url_params = {
                "count": min(5, 10),
                "start": 0,
                "q": "memberShareFeed",
                "moduleKey": "member-shares:phone",
                "includeLongTermHistory": True,
            }

    profile_urn = f"urn:li:fsd_profile:{urn_id}"
    
    url_params["profileUrn"] = profile_urn

    res = api.client.session.get(url, params=url_params)
    print(res.status_code)
    print(res.text)
    return res.json()


url = 'https://www.linkedin.com/voyager/api/voyagerSocialDashReactions?threadUrn=urn%3Ali%3AugcPost%3A7083331764475072512'          


test = get_reactions(url, 'hosneara-smrity-74b3b6146')
print(test)





# router = APIRouter()


# @router.get('/get_profile/{profile_id}')



# def get_browser():
#     from ..main import browser 
#     return browser

# async def login_to_linkedin(page: Page):

#     await page.goto('https://www.linkedin.com/login')

#     await page.fill('input[name="session_key"]', EMAIL)
#     await page.fill('input[name="session_password"]', PASSWORD)

#     await page.click("button[type='submit']")



# async def return_html(url: str, page: Page):

#     await page.goto(url)
#     await page.wait_for_selector('h1.text-heading-xlarge', timeout=30000)

#     name_element = page.locator('h1.text-heading-xlarge')
#     name = await name_element.inner_text()

#     return {'url': url, 'name': name}

# async def process_profile(url_list, browser):
#     page = await browser.new_page()
#     try:
#         await login_to_linkedin(page)
#         results = []
#         for url in url_list:
#             name = await return_html(url, page)
#             results.append(name)
#             await asyncio.sleep(5) 
        
#         return results
#     finally:
#         await page.close()



# @router.post('/')
# async def scrape_profiles(urls= Body(...), browser = Depends(get_browser)):
#     results = await process_profile(urls, browser)
#     return results

