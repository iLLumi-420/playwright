from fastapi import FastAPI
from .endpoints import crud, scrape
from playwright.async_api import async_playwright




app = FastAPI()



p = None
browser = None



@app.on_event("startup")
async def startup_event():
    global p, browser
    p = await async_playwright().start()
    browser = await  p.chromium.launch(headless=False)

@app.on_event("shutdown")
async def shutdown_event():
    global browser, p
    await browser.close()
    await p.stop()

app.include_router(crud.router, prefix='', tags=['users'])
app.include_router(scrape.router, prefix='/scrape', tags=['scrape'])