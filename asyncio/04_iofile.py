import asyncio

import aiofiles


"""
В данном примере асинхронное и синхронное чтение файла по понятным причинам имеет одну и туже скорость,
но не стоит забывать что при асинхронном чтении у нас есть возможность разгрузить ожидание ответа от множества
потоков исполняемых файлов, на много проще работать с вводом/выводом и так далее...
"""


def read_large_file():
    with open('..\\big_file.txt', 'r') as f:
        return f.read()


async def async_read_large_file():
    async with aiofiles.open('..\\big_file.txt', 'r') as f:
        return await f.read()


def count_words(text):
    return len(text.split(' '))


async def async_main():
    text = await async_read_large_file()
    print(count_words(text))


def main():
    text = read_large_file()
    print(count_words(text))


if __name__ == '__main__':
    asyncio.run(async_main())
    main()
