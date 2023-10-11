import requests

url_list = [
    'https://www.linkedin.com/in/nibin-b-521609218/',
    'https://www.linkedin.com/in/sandeep-parajuli-48274a238/',
    'https://www.linkedin.com/in/nibin-b-521609218/',
    'https://www.linkedin.com/in/sandeep-parajuli-48274a238/',
    'https://www.linkedin.com/in/nibin-b-521609218/',
    'https://www.linkedin.com/in/sandeep-parajuli-48274a238/',
    'https://www.linkedin.com/in/nibin-b-521609218/',
    'https://www.linkedin.com/in/sandeep-parajuli-48274a238/',
]

response = requests.post('http://127.0.0.1:8000/scrape/', json=url_list)
print(response.json())