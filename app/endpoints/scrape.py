from app.config import EMAIL, PASSWORD
from linkedin_api import Linkedin
from urllib.parse import quote
import time
from scrape_functions import get_reactions_details, search_posts


api = Linkedin(EMAIL, PASSWORD)


    

# post_id = '7119530037011185664'
# 

# data = get_reactions_details(api, post_id, query_id)

data = search_posts(api, 'python')
print(data)


