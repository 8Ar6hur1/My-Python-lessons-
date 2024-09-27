import requests
from bs4 import BeautifulSoup

url = 'https://news.ycombinator.com'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    title_elements = soup.find_all('span', {'class': 'titleline'})
    
    limit = 1

    if title_elements:
        for index, title_element in enumerate(title_elements[:limit], start=1):
            a_tag = title_element.find('a')
            if a_tag:
                title = a_tag.text.strip()
                url = a_tag['href'].strip()
                print(f'{index} Заголовок: {title}')
                print(f'URL: {url}\n')
    else:
        print('Headers not found on the page')
    
else:
    print(f'Не вдалося завантажити сторінку, статусний код: {response.status_code}')

