import requests
from time import time
import os
from os import makedirs


def get_file(url):
    r = requests.get(url, allow_redirects=True)
    return r, url


def write_file(index, response, url, directory):
    filename = f'{index}_{response.url.split("/")[-1]}'
    filepath = os.path.join(directory, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def main():
    t0 = time()

    url = 'https://c4.wallpaperflare.com/wallpaper/613/894/500/movie-pride-and-prejudice-keira-knightley-wallpaper-preview.jpg'

    directory = 'image'
    makedirs(directory, exist_ok=True)

    for i in range(1, 101):
        response, file_url = get_file(url)
        write_file(i, response, file_url, directory)

    print(f'{time() - t0:.2f}')

if __name__ == '__main__':
    main()

# 12.76 sec
