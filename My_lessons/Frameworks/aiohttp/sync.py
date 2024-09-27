import os
import random
import requests
from time import perf_counter, time

SITE = "https://thispersondoesnotexist.com"
IMAGE_COUNT = 50

def generate_filename(file_extension):
    temp = str(int(time()))
    for _ in range(5):
        temp += chr(random.randint(65, 75))
    return f'{temp}.{file_extension}'

def main():
    os.makedirs('sync_images', exist_ok=True)  # Ensure the directory exists
    for image_num in range(IMAGE_COUNT):
        response = requests.get(SITE)
        extension = response.headers.get('content-type', 'image/jpeg').split('/')[-1]
        filename = generate_filename(extension)

        with open(os.path.join('sync_images', filename), 'wb') as file:
            file.write(response.content)
        print(f'image: {image_num + 1} finished.')

if __name__ == '__main__':
    start = perf_counter()
    main()
    print(f'time: {(perf_counter() - start):.02f}')
