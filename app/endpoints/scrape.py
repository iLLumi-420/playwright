from app.config import EMAIL, PASSWORD
from linkedin_api import Linkedin
from scrape_functions import get_reactions_details, search_posts
import json




api = Linkedin(EMAIL, PASSWORD)



data = search_posts(api, 'we are hiring')


with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)




