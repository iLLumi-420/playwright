from bs4 import BeautifulSoup
import json
import re

def convert_count(text):
    strings = text.split()
    result = re.match(r'\d+', strings[0])
    print(result.group())
    number = int(result.group())
    if 'M' in strings[0]:
        return number*1000000
    elif 'K' in strings[0]:
        return number*1000
    else:
        return number


with open('new.html', 'r') as file:
    html = file.read()

soup = BeautifulSoup(html, 'html.parser')

def return_text(element, text):
    return element.select_one(f'.{text}').get_text(strip=True)

name = return_text(soup,'top-card-layout__title')
desc = return_text(soup,'top-card-layout__headline')

top = soup.find('h3', class_='top-card-layout__first-subline')

address = top.find('div', class_='top-card__subline-item').get_text(strip=True)

spans = top.find_all('span')
followers = spans[0].get_text(strip=True)
connections = spans[1].get_text(strip=True)


followers_count = convert_count(followers)
connections_count = convert_count(connections)


summary_section = soup.find('section', class_='summary')
about = return_text(summary_section, 'core-section-container__content')


articles_section = soup.find_all('section', class_='activities')

articles_li = articles_section[0].find_all('li')

articles = []
for li in articles_li:
    title = return_text(li, 'base-main-card__title')
    date = li.find('span', class_='base-main-card__metadata-item').get_text(strip=True)
    link = li.find('a')['href']
    
    articles.append({'title':title,'date':date,'link':link})


activities_li = articles_section[1].find_all('li')


activities = []
for li in activities_li:
    title = return_text(li, 'base-main-card__title')
    link = li.find('a')['href']
    
    activities.append({'title':title,'link':link})



experience_section = soup.find('section', class_='experience')
experience_lis = experience_section.find_all('li')

experience = []
for li in experience_lis:
    position = li.find('h3', class_='profile-section-card__title').get_text(strip=True)
    company = li.find('a', 'profile-section-card__subtitle-link')
    company_name = company.get_text(strip=True)
    link = company['href']
    time_span = li.find('span', class_='date-range')
    time = time_span.find('span').get_text(strip=True)

    experience.append({'position':position,'company':company_name,'link':link,'time':time})

education_section = soup.find('section', class_='education')
education_lis = education_section.find_all('li')

education = []
for li in education_lis:
    institution_a = li.find('a', class_='profile-section-card__title-link')
    institution = institution_a.get_text(strip=True)
    link = institution_a['href']
    info_spans = li.find_all('span', class_='education__item')
    level = info_spans[0].get_text(strip=True)
    degree = info_spans[1].get_text(strip=True)


    education.append({'instituion':institution,'link':link,'level':level,'degree':degree})


related_profiles_div = soup.find('div', class_='aside-profiles-list')
related_profile_li = related_profiles_div.find_all('li')

sidebar_profiles = []
for li in related_profile_li:
    name = li.find('h3', class_='base-aside-card__title').get_text(strip=True)
    desc = li.find('p', class_='base-aside-card__subtitle').get_text(strip=True)
    link = li.find('a', class_='base-card')['href']
    sidebar_profiles.append({'name':name,'desc':desc,'link':link})

print(experience)
data = {
    'name': name,
    'desc': desc,
    'address': address,
    'followers': followers_count,
    'connection': connections_count,
    'about': about,
    'experience': experience,
    'education': education,
    'articles': articles,
    'activities': activities,
    'sidebar_profiles': sidebar_profiles
}

with open('linkedin_profile_data.json', 'w') as file:
    json.dump(data, file, indent=4)







