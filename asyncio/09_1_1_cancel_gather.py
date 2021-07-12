import asyncio
import threading
import time
from typing import List

import aiohttp

"""
В примере показано как отмены на тасках не приводят к верной логике программы - 
то когда нам к примеру необходимо пробрасывание ошибки, то отмена на future может проигноривать
исключение или ошибку.

В случае же отмены таски, поведение процесса исполнения программы становится на много более предсказуемым...
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

    sleeping_period = 3 if task_name == 't_3' else 1
    print(f'{task_name=} sleeping')
    await asyncio.sleep(sleeping_period)
    print(f'{task_name=} finished sleeping')

    print(f'Finished task={task_name}')
    return [Photo.from_json(photo) for photo in photo_json]


def get_coros(session):
    return [
        photo_by_album('t_1', 1, session),
        photo_by_album('t_2', 2, session),
        photo_by_album('t_3', 3, session),
        photo_by_album('t_4', 4, session),
    ]


async def download_albums(albums):
    photos = []
    async with aiohttp.ClientSession() as session:
        for album in albums:
            photos.extend(await photo_by_album(f't{album}', album, session))
    return photos


def cancel_tasks(tasks, after):
    def inner_cancel():
        print('sleeping before future cancel')
        time.sleep(after)
        for i, t in enumerate(tasks, start=1):
            print(f'cancel {i}, {t}')
            print(t.cancel())

    t = threading.Thread(target=inner_cancel())
    t.start()


async def main_gather_cancel_on_tasks():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(c) for c in get_coros(session)]
        future = asyncio.gather(*tasks)

        cancel_tasks(tasks, 2)

        try:
            print('Await future')
            result = await future
        except asyncio.exceptions.CancelledError as ex:
            print(f'Excepted at await {repr(ex)}')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        loop.create_task(main_gather_cancel_on_tasks())
        loop.run_forever()
    finally:
        print('Closing loop')
        loop.close()
