from app.config import EMAIL, PASSWORD
from linkedin_api import Linkedin
from urllib.parse import quote
import time
from scrape_functions import get_reactions_details, search_posts
from bs4 import BeautifulSoup
import json




api = Linkedin(EMAIL, PASSWORD)



data = search_posts(api, 'We’ve just updated our Page')
print(data)

with open('data.json', 'w') as file:
    json.dump(data, file)




