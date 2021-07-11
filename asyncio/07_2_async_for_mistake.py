import asyncio

"""
Данный код не является True параллельным, некторые начинающие программисты ошибочно
полагают что с помощью async for можно добиться True пареллельного выполнения процессов... .
Но в действительности паралельны эти процессы лишь с точки зрения OI-bound.
_______________________________________________________________________________________________
Коротко говоря async for позволяется пройтись циклом по асинхронному генератору!
_______________________________________________________________________________________________
Еще проще - с помощью async for мы проходися по корутине которая что-то асинхронно генерирует... .
"""


class AsyncIterator:

    def __init__(self, n):
        self.i = 0
        self.n = n

    def __aiter__(self):
        return self

    async def __anext__(self):
        print(f'Start {self.i}')
        await asyncio.sleep(1)
        print(f'end {self.i}')

        if self.i >= self.n:
            raise StopAsyncIteration
        self.i += 1
        return self.i


async def main():
    async for n in AsyncIterator(10):
        print(f'Finally {n}')


if __name__ == '__main__':
    asyncio.run(main())
