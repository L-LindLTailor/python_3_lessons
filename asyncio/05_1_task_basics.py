import asyncio


async def process():
    print('first')
    await asyncio.sleep(1)
    print('second')

    return 'first to second process result'


async def main():
    task_1 = asyncio.create_task(process(), name='task_1')
    task_2 = asyncio.ensure_future(process())

    result = await asyncio.gather(task_1, task_2)

    print(f'{task_1.get_name()}. Done = {task_1.done()}')
    print(f'{task_2.get_name()}. Done = {task_2.done()}')

    for i in result:
        print(i)

if __name__ == '__main__':
    asyncio.run(main())
