import requests

url_list = [
    'https://www.linkedin.com/in/yogesh-kandel-86b46223b/',
    'https://www.linkedin.com/in/praful-thapa-33811a12b/',
    'https://www.linkedin.com/in/rajan-koirala-362283205/',
    'https://www.linkedin.com/in/yogesh-kandel-86b46223b/',
    'https://www.linkedin.com/in/praful-thapa-33811a12b/',
    'https://www.linkedin.com/in/rajan-koirala-362283205/',
]

response = requests.post('http://127.0.0.1:8000/scrape/', json=url_list)
print(response.json())