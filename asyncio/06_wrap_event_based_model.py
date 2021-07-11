import asyncio
import threading
import time


"""
Создаем и управляем future комбинируя точки входа
многопоточного и асинхронного (True параллельного) программирования.
"""


class Terminal:

    async def start(self):
        loop = asyncio.get_running_loop()
        future = loop.create_future()

        task = threading.Thread(target=self.run_cmd, args=(loop, future))
        task.start()

        return await future

    def run_cmd(self, loop, future):
        time.sleep(3)
        loop.call_soon_threadsafe(future.set_result, 1)


async def main():
    process = Terminal()

    result = await process.start()
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
