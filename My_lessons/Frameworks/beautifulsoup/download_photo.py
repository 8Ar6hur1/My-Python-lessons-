import os
from fake_useragent import UserAgent
import requests
import time
from bs4 import BeautifulSoup

ua = UserAgent()
random_user_agent = ua.random

url = 'https://www.pexels.com'

download_folder = 'wallpapern'

if not os.path.exists(download_folder):
    os.makedirs(download_folder)

headers = {
    'User-Agent': random_user_agent
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    img_elements = soup.find_all('img')
    
    if img_elements:
        print('start' + 1)
        for index, img_element in enumerate(img_elements):
            img_url = img_element.get('src')
            if img_url:
                img_data = requests.get(img_url).content
                img_name = os.path.join(download_folder, f'image_{index}.jpg')
                with open(img_name, 'wb') as img_file:
                    img_file.write(img_data)
                print(f'Завантажено зображення {index}: {img_name}')
                time.sleep(1)
    else:
        print('IMG elements not found on the page')
else:
    print(f'Не вдалося завантажити сторінку, статусний код: {response.status_code}')
