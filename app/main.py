from fastapi import FastAPI
from .endpoints import crud, scrape



app = FastAPI()

app.include_router(crud.router, prefix='', tags=['users'])
app.include_router(scrape.router, prefix='/scrape', tags=['scrape'])



