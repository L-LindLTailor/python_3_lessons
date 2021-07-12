import asyncio
import time

"""
Пример того в каком случае мы можем получить результаты по мере их поступления.
"""


async def process_one():
    await asyncio.sleep(1)

    return 'first process result'


async def process_two():
    await asyncio.sleep(2)

    return 'second process result'


async def main():
    start_time_of_completion = time.perf_counter()

    task_1 = asyncio.create_task(process_one(), name='task_1')
    task_2 = asyncio.ensure_future(process_two())

    for i, t in enumerate(asyncio.as_completed((task_1, task_2)), start=1):
        result = await t

        elapsed = time.perf_counter() - start_time_of_completion

        print(f'Executed {i} in {elapsed:0.2f} seconds')
        print(result)


if __name__ == '__main__':
    asyncio.run(main())
