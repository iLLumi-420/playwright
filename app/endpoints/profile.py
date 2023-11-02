from bs4 import BeautifulSoup
import json

with open('liprofile.html', 'r') as file:
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

summary_section = soup.find('section', class_='summary')
about = return_text(summary_section, 'core-section-container__content')

articles_section = soup.find_all('section', class_='activities')

articles_li = articles_section[0].find_all('li')

articles = []
for li in articles_li:
    title = return_text(li, 'base-main-card__title')
    date = li.find('span', class_='base-main-card__metadata-item').get_text(strip=True)
    link = li.find('a', class_='base-card')['href']
    
    articles.append({'title':title,'date':date,'link':link})



activities_li = articles_section[1].find_all('li')
print(activities_li[0])

activities = []
for li in activities_li:
    title = return_text(li, 'base-main-card__title')
    link = li.find('a', class_='base-card__full-link')['href']
    
    activities.append({'title':title,'link':link})

data = {
    'name': name,
    'desc': desc,
    'address': address,
    'followers': followers,
    'connection': connections,
    'about': about,
    'articles': articles,
    'activities': activities
}

with open('linkedin_profile_data.json', 'w') as file:
    json.dump(data, file, indent=4)






