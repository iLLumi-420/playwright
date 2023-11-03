from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

def parse_month_year_date(date_str):
    try:
        date = datetime.strptime(date_str, '%b %Y')
        return date.strftime('%Y/%m/%d')
    except ValueError:
        return None
    
def get_date():
    now = datetime.now()
    date_string = now.strftime('%Y-%m-%d')
    return date_string

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
    text = text.strip()
    if text == 'less than a year':
        return 0
    split = text.split()
    print(split)
    years, months = 0, 0

    if 'year' in split or 'years' in split:
        years_index = split.index('years') if 'years' in split else split.index('year')
        years = int(split[years_index - 1]) if years_index > 0 else 0

    if 'month' in split or 'months' in split:
        months_index = split.index('months') if 'months' in split else split.index('month')
        months = int(split[months_index - 1]) if months_index > 0 else 0

    decimal_value = years + months / 12.0
    return decimal_value

def seperate_actor_and_action(text):
    text = text.split('by')
    action = text[0].strip()
    actor = text[1].strip()
    return action, actor

    
def return_text(element, classname):
    result = element.select_one(f'.{classname}')
    if result:
        result = result.get_text(strip=True)
    else:
        result = None
    return result

def extract_data(filename):

    with open(filename, 'r') as file:
        html = file.read()

    soup = BeautifulSoup(html, 'html.parser')   

    name = return_text(soup,'top-card-layout__title')
    desc = return_text(soup,'top-card-layout__headline')
    address = soup.find('div', class_='top-card__subline-item')
    address = address.get_text(strip=True) if address else None

    top = soup.find('h3', class_='top-card-layout__first-subline')
    spans = top.find_all('span')

    followers = spans[0].get_text(strip=True)
    connections = spans[1].get_text(strip=True)

    followers = text_to_number(followers)
    connections = text_to_number(connections)


    summary_section = soup.find('section', class_='summary')
    
    about = return_text(summary_section, 'core-section-container__content') if summary_section else None
   

    experience_section = soup.find('section', class_='experience')
    if experience_section:
        experience_lis = experience_section.find_all('li')
        experience = []
        for li in experience_lis:
            position = li.find('h3', class_='profile-section-card__title')
            
            position = position.get_text(strip=True) if position else None
           
            company = li.find('a', 'profile-section-card__subtitle-link')
            if company:
                company_name = company.get_text(strip=True)
                link = company['href']
            else:
                link = None
                company_name = li.find('h4', class_='profile-section-card__subtitle').get_text(strip=True)
            time_span = li.find('span', class_='date-range')
            if time_span:
                dates = time_span.find_all('time')
                print(len(dates))
                
                date1 = parse_month_year_date(dates[0].text)

                date2 = get_date() if len(dates) < 2 else parse_month_year_date(dates[1].text) 
                duration = time_span.find('span').get_text(strip=True)
                duration = duration_to_number(duration)
            else:
                date1 = None
                date2 = None
                duration = None

            experience.append({'position':position,'company':company_name,'link':link,'date':f'{date1}-{date2}','time_in_years':duration})
    else:
        experience = []


    education_section = soup.find('section', class_='education')
    education = []
    if education_section:
        education_lis = education_section.find_all('li')

        for li in education_lis:
            level , degree= None, None
            institution_a = li.find('a', class_='profile-section-card__title-link')
            institution = institution_a.get_text(strip=True) if institution_a else None
            link = institution_a['href'] if institution_a else None
            info_spans = li.find_all('span', class_='education__item')
            if len(info_spans) > 1:
                level = info_spans[0].get_text(strip=True)
                degree = info_spans[1].get_text(strip=True)
            elif len(info_spans) == 1:
                degree = info_spans[0].get_text(strip=True)
                

            education.append({'instituion':institution,'link':link,'level':level,'degree':degree})


    related_profiles_div = soup.find('div', class_='aside-profiles-list')
    sidebar_profiles = []
    if related_profiles_div:

        related_profile_li = related_profiles_div.find_all('li')        
        for li in related_profile_li:
            name = li.find('h3', class_='base-aside-card__title').get_text(strip=True)
            link = li.find('a', class_='base-aside-card--link')['href']
            desc = li.find('p', class_='base-aside-card__subtitle')
            desc = desc.get_text(strip=True) if desc else None
           
            sidebar_profiles.append({'name':name,'desc':desc,'link':link})

    same_name_section = soup.find('section', class_='samename')   
    similar_profiles = []
    if same_name_section:
        same_name_lis = same_name_section.find_all('li')
        for li in same_name_lis:
            name = li.find('h3', class_='base-aside-card__title').get_text(strip=True)
            link = li.find('a', class_='base-aside-card--link')['href']
            desc = li.find('p', class_='base-aside-card__subtitle')
            desc = desc.get_text(strip=True) if desc else None
           
            similar_profiles.append({'name':name,'desc':desc,'link':link})



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
                action, actor = seperate_actor_and_action(subtitle)

                sections['activities'].append({'link':link,'title':title,'action':action, 'actor':actor})
            
        else:
            sections[section_title] = []
            for li in li_list:
                link = li.find('a')['href']
                title = li.find('h3', class_='base-main-card__title').get_text(strip=True)
                subtitle = li.find('h4', class_='base-main-card__subtitle').get_text(strip=True)
                metadata = li.find('span', class_='base-main-card__metadata-item')
               
                metadata = metadata.get_text(strip=True) if metadata else None
           


                sections[section_title].append({'link':link,'title':title,'subtitle':subtitle,'metadata':metadata})
    
    certification_section = soup.find('section', class_='certifications')
    certifications = []
    if certification_section:
        certification_lis = certification_section.find_all('li')

        for li in certification_lis:
            level , degree= None, None
            title = li.find('h3', class_='profile-section-card__title').get_text(strip=True)
            institution_a = li.find('a', class_='profile-section-card__title-link')
            institution = institution_a.get_text(strip=True) if institution_a else None
            link = institution_a['href'] if institution_a else None
            date = li.find('time')
            date = date.get_text(strip=True) if date else None
                
            date = parse_month_year_date(date)
            certification_id = li.find('div', 'certifications__credential-id')
            if certification_id:
                certification_id = certification_id.get_text(strip=True)
                certification_id = certification_id.split()[-1]
            else:
                certification_id = None

            certifications.append({'title':title,'instituion':institution,'link':link,'date':date,'certification_id':certification_id})

    
    more_activities_section = soup.find('section', class_='recommended-content')
    more_activities= []
    if more_activities_section:
        more_div = more_activities_section.find_all('div', class_='main-activity-card')
        for li in more_div:
            link = li.find('a')['href']
            title = li.find('h3', class_='base-main-card__title').get_text(strip=True)
            subtitle = li.find('h4', class_='base-main-card__subtitle').get_text(strip=True)

            action, actor = seperate_actor_and_action(subtitle)

            more_activities.append({'link':link,'title':title,'action':action, 'actor':actor})
        
    

    data = {
        'name': name,
        'desc': desc,
        'address': address,
        'followers': followers,
        'connection': connections,
        'about': about,
        'experience': experience,
        'education': education,
        'sections_data': sections,
        'sidebar_profiles': sidebar_profiles,
        'similar_profiles': similar_profiles,
        'certfications': certifications,
        'more_activity': more_activities
    }


    with open(f'linkedin_{filename.split(".")[0]}_data.json', 'w') as file:
        json.dump(data, file, default=str,indent=4)

    return data
    



if __name__=='__main__':

    file = 'profile200.html'
    data = extract_data(file)
    


