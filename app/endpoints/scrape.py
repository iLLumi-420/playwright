from fastapi import APIRouter, HTTPException, Depends, Body
from playwright.async_api import Page
import asyncio
from app.config import EMAIL, PASSWORD
from linkedin_api import Linkedin
from urllib.parse import quote
import time


api = Linkedin(EMAIL, PASSWORD)

def get_reactions_details(): 

    count = 10
    start = 0
    thread_Urn = quote('urn:li:activity:7117792651705274368')
    queryId = "voyagerSocialDashReactions.fa18066ba15b8cf41b203d2c052b2802"

    reactions_data = []
    reaction_count = {}

    while True:
        variables = f"(count:{count},start:{start},threadUrn:{thread_Urn})"
        uri = f'/graphql?variables={variables}&queryId={queryId}'
        response = api._fetch(uri=uri)

        if response is None or response.status_code != 200:
            break

        print(response.text)
        response = response.json()
    
        elements = response.get('data', {}).get('socialDashReactionsByReactionType', {}).get('elements')
        print(response)  

        if not elements:
            break


        
        for item in elements:
            reaction_type = item["reactionType"]
            name = item["reactorLockup"]["title"]["text"]
            description = None
            if item.get("reactorLockup") and item["reactorLockup"].get("subtitle") and item["reactorLockup"]["subtitle"].get("text"):
                description = item["reactorLockup"]["subtitle"]["text"]
            print(name, description, reaction_type)
            reactions_data.append({
                "name": name,
                "desc": description,
                "reaction": reaction_type
            })
            reaction_count[reaction_type] = reaction_count.get(reaction_type, 0) + 1
        
        
        start = start + 10
        time.sleep(1)

    return {'data':reactions_data, 'count':reaction_count}
    

data = get_reactions_details()
print(data)

