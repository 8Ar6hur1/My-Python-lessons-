import os
import random
import aiohttp
import asyncio
import aiofiles
from time import perf_counter, time

SITE = "https://thispersondoesnotexist.com"
IMAGE_COUNTE = 50

async def generate_filename(file_extension):
    temp = str(int(time()))
    for _ in range(5):
        temp += chr(random.randint(65, 75))
    return f'{temp}.{file_extension}'

async def download_image(image_num):
    async with aiohttp.ClientSession() as session:
        async with session.get(SITE) as response:
            extension = response.headers['content-type'].split('/')[-1]
            filename = os.path.join('async_images', await generate_filename(extension))

            os.makedirs(os.path.dirname(filename), exist_ok=True)

            async with aiofiles.open(filename, mode='wb') as file:
                async for chunk in response.content.iter_chunked(64 * 1024):
                    await file.write(chunk)

async def main():
    image_tasks = []

    for image_num in range(IMAGE_COUNTE):
        image_tasks.append(asyncio.create_task(download_image(image_num)))     
    await asyncio.gather(*image_tasks)   

if __name__ == '__main__':
    start = perf_counter()
    asyncio.run(main())
    print(f'time: {(perf_counter() - start):.02f}')
