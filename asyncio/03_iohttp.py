import asyncio
from typing import List

import aiohttp as aiohttp

from decoratorsmy.decorators import async_measure_time


"""
Пример того как True асинхронно (многоядерно, параллельно) работать с http/https запросами.

Не забудьте в Edit Configuration, если вы пользуетесь PyCharm добавить галочку напротив параметра
Emulate terminal in output console, чтобы в OS Windows остановить run_forever() с помощью клавишь ctrl + c.
"""


def print_photo_title(photos):
    for photo in photos:
        print(f'{photo.title}', end='\n')


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


async def photo_by_album(task_name, album, session) -> List[Photo]:
    print(f'{task_name=}')
    url = f'https://jsonplaceholder.typicode.com/photos?albumId={album}'

    resource = await session.get(url)
    photo_json = await resource.json()

    return [Photo.from_json(photo) for photo in photo_json]


@async_measure_time
async def main():
    """
    Реализовано True parallel process running - то есть, данный пример является
    настоящим многоядерным параллельным программированием, в отличие от конкурентого
    thread программирования. Хотя стоит заметить, что thread добавляет интерактивности,
    позволяет выжать из конкретного ядра максимум, а так же менее трудозатрато и так далее.
    :return:
    """
    async with aiohttp.ClientSession() as session:
        photos_in_album = await asyncio.gather(*(photo_by_album(f'Task {i + 1}', album, session)
                                                 for i, album in enumerate(range(2, 30))))

        photos_count = sum([len(cur) for cur in photos_in_album])
        print(f'{photos_count}')


if __name__ == '__main__':
    # asyncio.run(main()) при данном вызове возникают ошибки, разработчики над этим работают

    loop_run = asyncio.get_event_loop()
    try:
        loop_run.create_task(main())
        loop_run.run_forever()
    except KeyboardInterrupt:
        print('Manually closed application')
    finally:
        loop_run.close()
