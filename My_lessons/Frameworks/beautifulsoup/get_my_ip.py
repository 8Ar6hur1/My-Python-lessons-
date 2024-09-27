import requests
from bs4 import BeautifulSoup

url = 'https://2ip.ua/ru/'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    ip_element = soup.find('div', {'class': 'ip'})

    if ip_element:
        ip_address = ip_element.contents[0].strip()
        print(f'Your IP: {ip_address}')
    else:
        print('Your IP address not found on the page.')
else:
    print(f'Failed to load the page, status code: {response.status_code}')
