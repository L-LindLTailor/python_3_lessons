import asyncio
import aiohttp
from asyncio import FIRST_EXCEPTION
from typing import List

"""
В этом примере работа процессов async await не прерывается выбросом ошибки, все отрабатывает до конца.
Данный пример показывает как можно логично и грамотно обрабатывать исключения при необходимости их логирования
и необходимости в продолжении отрабатывания всех параллельных процессов...
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


async def main_await():
    async with aiohttp.ClientSession() as session:
        tasks = [
            photo_by_album('t_1', 1, session),
            photo_by_album('t_2', 2, session),
            photo_by_album('t_3', 3, session),
            photo_by_album('t_a', 'a', session),
            photo_by_album('t_4', 4, session),
        ]
    photos = []

    # done_tasks, pending_tasks = await asyncio.wait(tasks, return_when=FIRST_EXCEPTION)
    done_tasks, pending_tasks = await asyncio.wait(tasks)

    for pending_task in pending_tasks:
        print(f'cancelled {pending_task}')
        print(pending_task.cancel())

    for done in done_tasks:
        try:
            result = done.result()
            photos.extend(result)
        except Exception as ex:
            print(repr(ex))

    print_photo_title(photos)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        loop.create_task(main_await())
        loop.run_forever()
    finally:
        print('Closing loop')
        loop.close()
