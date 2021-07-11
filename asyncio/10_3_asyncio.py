import asyncio
import aiohttp
from decoratorsmy.decorators import async_measure_time

"""
Пример под номером 10 пошагово начиная с 1 по 3 показывает на сколько высока разница в скорости
между обычным поступательным запросом, threading запропросами с хешированием сессии и
наиболее высокопроизводительным asyncio (в данном случае aiohttp)!
"""

async def download_site(url, session):
    async with session.get(url) as response:
        print(f'Read {response.content.total_bytes} from {url}')


@async_measure_time
async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.create_task(download_site(url, session))
            tasks.append(task)

        try:
            print('before await')
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as ex:
            print(repr(ex))


if __name__ == '__main__':
    sites = [
        'https://www.engineerspock.com',
        'https://enterprisecraftsmanship.com/',
    ] * 80

    asyncio.run(download_all_sites(sites))
