import asyncio
import time
from typing import List

import aiohttp

"""
Если не обернуть async for в Try: Except:, то выполнение процесса прервется выброшенным исключением,
если же обернуть, то мы получить сообщение об исключении,
а так же выполним весь процесс до момента возникновения ошибки...

Так же важно понимать, что Try: Except: внутри цикла не решает проблемы, так как само исключение пробрасывается
еще на стадии самого вхождения в цикл, то есть до Try: Except: внутри async for...
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
    print(f'{task_name=}')
    url = f'https://jsonplaceholder.typicode.com/photos?albumId={album}'

    resource = await session.get(url)
    photo_json = await resource.json()

    return [Photo.from_json(photo) for photo in photo_json]


async def download_albums(albums):
    async with aiohttp.ClientSession() as session:
        for album in albums:
            if not isinstance(album, int):
                raise RuntimeError('invalid album number')
            yield await photo_by_album(f't{album}', album, session)


async def main():
    try:
        async for photos in download_albums([1, 2, 'a', 4]):
            print_photo_title(photos)
    except Exception as ex:
        print(repr(ex))


if __name__ == '__main__':
    asyncio.run(main())

    time.sleep(3)
    print('main ended')
