import asyncio
import time
from typing import List

import aiohttp

"""
В данном примере выброс исключения и его отлавливание записано в духе логики программы - корректно,
что позволяет выполнить весь main процесс до конца, то есть пробросив искоючение мы не останавливаем
процесс, а продолжаем его выполнение после отлавнивания проблемного участка...

Нагляднее: 1 процесс, 2 процесс, Исключение, 4 процесс и тд.
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
    async with aiohttp.ClientSession() as session:
        for album in albums:
            try:
                yield await photo_by_album(f't{album}', album, session)
            except Exception as ex:
                print(repr(ex))


async def main():
    async for photos in download_albums([1, 2, 'a', 4]):
        print_photo_title(photos)


if __name__ == '__main__':
    asyncio.run(main())

    time.sleep(3)
    print('main ended')
