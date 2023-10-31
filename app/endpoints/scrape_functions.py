import time
from urllib.parse import quote
from linkedin_api import Linkedin
import json

import datetime

def convert_relative_time(relative_time):
    # Split the relative time expression
    units = {
        'm': 'minutes',
        'h' : 'hours',
        'd' : 'days'
    }
    time_parts = relative_time.split()
    print(time_parts)
    if len(time_parts) != 3:
        return relative_time  # Not a recognized format, return as is

    # Extract the quantity and unit
    quantity = int(time_parts[0])
    unit = time_parts[1]

    # Define a mapping of units to time deltas
    unit_to_delta = {
        "minute": datetime.timedelta(minutes=1),
        "hour": datetime.timedelta(hours=1),
        "day": datetime.timedelta(days=1)
    }

    # Calculate the absolute timestamp
    delta = unit_to_delta.get(unit)
    if delta:
        absolute_time = datetime.datetime.utcnow() - (delta * quantity)
        return absolute_time.isoformat()

    return relative_time  # Unknown unit, return as is






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

        if start == 20:
            break

        variables = f'(start:{start},origin:{origin},query:(keywords:{quote(search_term)},flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:datePosted,value:List(past-24h)),(key:resultType,value:List(CONTENT))),includeFiltersInResponse:false))'
        uri = f'/graphql?variables={variables}&&queryId={query_id}'

        response = api._fetch(uri=uri)

        if response is None or response.status_code != 200:
            break
        response_json = response.json()

        elements = response_json.get('data', {}).get('searchDashClustersByAll',{}).get('elements',{})
       
        for element in elements:
            items = element['items'] if len(element['items']) > 1 else None
            if items:
                break


        for each in items:

            data = get_required_data(each)
            search_data.append(data)


        start = start + 10
        time.sleep(1)
        

    return search_data


def get_required_data(each):
    
    data = {}
    item = each['item']['entityResult']

    data['post_id'] = item['trackingUrn']

    data['post_url'] = item['navigationUrl']

    social_activity = item['insightsResolutionResults'][0]['socialActivityCountsInsight']
    data['comments'] = social_activity['numComments']
    data['reactions'] = social_activity['numLikes']
    
    data['reaction_type'] = []
    reactions_type = social_activity.get('reactionTypeCounts', {})

    if reactions_type:
        for reaction in reactions_type:
            data['reaction_type'].append({
                'type': f'{reaction["reactionType"]}',
                'count': f'{reaction["count"]}'
            })

    if len(item['title']['attributesV2']) > 0:
        data['hashtag'] = item['title']['attributesV2'][0]['detailData']['hashtag']
    else:
        data['hashtag'] = None

    data['media'] = item['image']['attributes'][0]['detailData']['imageUrl']

    data['text'] = item['summary']['text']

    data['publisher'] = item['title']['text']
    if data['publisher'] == 'Anshu Raj':
        with open('anshuraj.json', 'w') as file:
            json.dump(item, file, indent=4)
    data['publisher_url'] = item['actorNavigationUrl']

    # data["posted_at"] = convert_relative_time(item["secondarySubtitle"]['text'])
    
    return data
    
        