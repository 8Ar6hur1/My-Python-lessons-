import aiohttp
import asyncio
import os
from os import makedirs
from time import time

async def get_file(session, url):
    async with session.get(url) as response:
        return await response.read(), str(response.url)

async def write_file(index, content, url, directory):
    filename = f'{index}_{url.split("/")[-1]}'
    filepath = os.path.join(directory, filename)
    with open(filepath, 'wb') as file:
        file.write(content)

async def main():
    t0 = time()

    url = 'https://c4.wallpaperflare.com/wallpaper/613/894/500/movie-pride-and-prejudice-keira-knightley-wallpaper-preview.jpg'

    directory = 'image'
    makedirs(directory, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 101):
            tasks.append(get_file(session, url))
        
        responses = await asyncio.gather(*tasks)
        
        for i, (content, response_url) in enumerate(responses, start=1):
            await write_file(i, content, response_url, directory)

    print(f'{time() - t0:.2f}')
    

if __name__ == '__main__':
    asyncio.run(main())

# 0.39 sec
