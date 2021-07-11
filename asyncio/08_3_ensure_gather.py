import asyncio
import time
from typing import List

import aiohttp


"""
Если логика программы предпологает, что исключение не должно прерывать процессы исполнения Task-ов
с использованием gather и получить результаты из других Task-ов то второй параметр return_exceptions
нужно выставить в True.

Так же нужно внимательней отнестить к обработке Task-ов в колбеке который на него навешан...
"""


class Photo:
    def __init__(self, album_id, photo_id, title, url, thumbnail_url):
        self.thumbnail_url = thumbnail_url
        self.url = url
        self.title = title
        self.photo_id = photo_id
        self.album_id = album_id

    @classmethod
    def from_json(cls, obj):
        return Photo(obj['albumId'], obj['id'], obj['title'], obj['url'], obj['thumbnailUrl'])


def print_photo_title(photos):
    for photo in photos:
        print(f'{photo.title}', end='\n')


async def photo_by_album(task_name, album, session) -> List[Photo]:
    if not isinstance(album, int):
        raise RuntimeError('invalid album number')
    print(f'{task_name=}')
    url = f'https://jsonplaceholder.typicode.com/photos?albumId={album}'

    resource = await session.get(url)
    photo_json = await resource.json()

    return [Photo.from_json(photo) for photo in photo_json]


async def download_albums(albums):
    photos = []
    async with aiohttp.ClientSession() as session:
        for album in albums:
            photos.extend(await photo_by_album(f't{album}', album, session))
    return photos


async def main_gather():
    async with aiohttp.ClientSession() as session:
        tasks = [
            photo_by_album('t_1', 1, session),
            photo_by_album('t_2', 2, session),
            photo_by_album('t_a', 'a', session),
            photo_by_album('t_4', 4, session),
        ]
        photos = []
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for res in results:
            if isinstance(res, Exception):
                print(repr(res))
            else:
                photos.extend(res)

    print_photo_title(photos)

if __name__ == '__main__':
    asyncio.run(main_gather())

    time.sleep(3)
    print('main ended')
