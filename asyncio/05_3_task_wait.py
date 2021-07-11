import asyncio
from collections import namedtuple

import aiohttp

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

services = (
    Service('ipify', 'https://api.ipify.org?forman=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'jquery'),
)


async def get_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def fetch_ip(service):
    print(f'Fetching IP from {service.name}')

    json_response = await get_json(service.url)
    ip = json_response[service.ip_attr]

    return f'{service.name} finished with result: {ip}'


async def main():
    coroutines = [fetch_ip(service) for service in services]

    done, pending = await asyncio.wait(coroutines)

    for i in done:
        print(i.result())


if __name__ == '__main__':
    loop_run = asyncio.get_event_loop()
    try:
        loop_run.create_task(main())
        loop_run.run_forever()
    except KeyboardInterrupt:
        print('Manually closed application')
    finally:
        loop_run.close()
