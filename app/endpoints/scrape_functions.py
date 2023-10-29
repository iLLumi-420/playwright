import time
from urllib.parse import quote
from linkedin_api import Linkedin

def get_reactions_details(api: Linkedin, post_urn: str): 

    count = 10
    start = 0
    thread_Urn = quote(f'urn:li:ugcPost:{post_urn}')
    query_id = 'voyagerSocialDashReactions.fa18066ba15b8cf41b203d2c052b2802'

    reactions_data = []
    reaction_count = {}

    while True:
        variables = f"(count:{count},start:{start},threadUrn:{thread_Urn})"
        uri = f'/graphql?variables={variables}&&queryId={query_id}'
        response = api._fetch(uri=uri)

        if response is None or response.status_code != 200:
            break

        response = response.json()
        elements = response.get('data', {}).get('socialDashReactionsByReactionType', {}).get('elements')

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


def search_posts(api : Linkedin, search_term: str):

    start = 0
    query_id = 'voyagerSearchDashClusters.522de52c041498ff853a0ecda602a0c0'
    origin = 'FACETED_SEARCH'

   

    search_data = []

    while True:

        if start == 30:
            break

        variables = f'(start:{start},origin:{origin},query:(keywords:{quote(search_term)},flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:datePosted,value:List(past-24h)),(key:resultType,value:List(CONTENT)),(key:sortBy,value:List(date_posted))),includeFiltersInResponse:false))'

        uri = f'/graphql?variables={variables}&&queryId={query_id}'

        response = api._fetch(uri=uri)

        if response is None or response.status_code != 200:
            break
        response_json = response.json()

        print(response_json)

        elements = response_json.get('data', {}).get('searchDashClustersByAll',{}).get('elements',{})

        search_data.append(elements)
        start = start + 10
        time.sleep(1)
        

    return search_data

   