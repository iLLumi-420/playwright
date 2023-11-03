from bs4 import BeautifulSoup
import json
import re

def text_to_number(text):
    text = text.replace(',', '')
    strings = text.split()
    result = re.match(r'\d+', strings[0])
    number = int(result.group())
    if 'M' in strings[0]:
        return number*1000000
    elif 'K' in strings[0]:
        return number*1000
    else:
        return number
    
def duration_to_number(text):
    split = text.strip().split()
    print(split)
    years, months = 0, 0

    if 'year' in split or 'years' in split:
        years_index = split.index('years') or split.index('year')
        years = int(split[years_index - 1]) if years_index > 0 else 0

    if 'month' in split or 'months' in split:
        months_index = split.index('months') or split.index('month')
        months = int(split[months_index - 1]) if months_index > 0 else 0

    decimal_value = years + months / 12.0
    return decimal_value

    
def return_text(element, classname):
    return element.select_one(f'.{classname}').get_text(strip=True)

def extract_data():

    with open('new.html', 'r') as file:
        html = file.read()

    soup = BeautifulSoup(html, 'html.parser')   

    name = return_text(soup,'top-card-layout__title')
    desc = return_text(soup,'top-card-layout__headline')
    address = soup.find('div', class_='top-card__subline-item').get_text(strip=True)

    top = soup.find('h3', class_='top-card-layout__first-subline')
    spans = top.find_all('span')

    followers = spans[0].get_text(strip=True)
    connections = spans[1].get_text(strip=True)

    followers = text_to_number(followers)
    connections = text_to_number(connections)


    summary_section = soup.find('section', class_='summary')
    about = return_text(summary_section, 'core-section-container__content')

    experience_section = soup.find('section', class_='experience')
    experience_lis = experience_section.find_all('li')

    experience = []
    for li in experience_lis:
        position = li.find('h3', class_='profile-section-card__title').get_text(strip=True)
        company = li.find('a', 'profile-section-card__subtitle-link')
        company_name = company.get_text(strip=True)
        link = company['href']
        time_span = li.find('span', class_='date-range')
        dates = time_span.find_all('time')
        range = f'{dates[0].text}-{dates[1].text}' if len(dates)>1 else f'{dates[0].text}-Present'
        duration = time_span.find('span').get_text(strip=True)
        duration = duration_to_number(duration)

        experience.append({'position':position,'company':company_name,'link':link,'date':range,'time_in_years':duration})


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


    sections_element = soup.find_all('section', class_='activities')

    sections = {}
    for section in sections_element:
        section_title = section.find('h2', class_='section-title').get_text(strip=True)
        li_list = section.find_all('li')

        if 'courses' in section_title.lower():
            sections['courses'] = []
            for li in li_list:
                link = li.find('a')['href']
                title = li.find('h3', class_='base-main-card__title').get_text(strip=True)
                subtitle = li.find('h4', class_='base-main-card__subtitle').get_text(strip=True)
                subtitle = subtitle.split(':')[1].strip()
                metadata = li.find('span', class_='base-main-card__metadata-item').get_text(strip=True)
                metadata = text_to_number(metadata)


                sections['courses'].append({'link':link,'course_name':title,'author':subtitle,'viewers':metadata})
        
        elif 'articles' in section_title.lower():
            sections['articles'] = []
            for li in li_list:
                link = li.find('a')['href']
                title = li.find('h3', class_='base-main-card__title').get_text(strip=True)
                subtitle = li.find('h4', class_='base-main-card__subtitle').get_text(strip=True)
                subtitle = subtitle.split('By ')[1].strip()
                metadata = li.find('span', class_='base-main-card__metadata-item').get_text(strip=True)
            


                sections['articles'].append({'link':link,'title':title,'author':subtitle,'date':metadata})

        elif 'activity' in section_title.lower():
            sections['activities'] = []
            for li in li_list:
                link = li.find('a')['href']
                title = li.find('h3', class_='base-main-card__title').get_text(strip=True)
                subtitle = li.find('h4', class_='base-main-card__subtitle').get_text(strip=True)

                sections['activities'].append({'link':link,'title':title,'subtitle':subtitle})
            
        else:
            print('Not found')
        

    data = {
        'name': name,
        'desc': desc,
        'address': address,
        'followers': followers,
        'connection': connections,
        'about': about,
        'experience': experience,
        'education': education,
        'courses': sections['courses'],
        'articles': sections['articles'],
        'activities': sections['activities'],
        'sidebar_profiles': sidebar_profiles
    }
    return data
    



if __name__=='__main__':
    data = extract_data()
    with open('linkedin_profile_data.json', 'w') as file:
        json.dump(data, file, indent=4)



