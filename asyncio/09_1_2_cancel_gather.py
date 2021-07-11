import asyncio

"""
Пример того что вешать cancel() на future опасно с точки зрения отрабатывания кода.
В данном случае cancel() вешается на таски что позволяет успешно пробросить информацию
об исключениях или ошибках...
"""


class ErrorThatShouldCancelOtherTasks(Exception):
    pass


async def my_sleep(secs):
    print(f'task {secs}')
    await asyncio.sleep(secs)
    print(f'task {secs} finished sleeping')

    if secs == 5:
        raise ErrorThatShouldCancelOtherTasks('5 is forbidden')
    print(f'Slept for {secs} secs')


async def main_cancel_future():
    tasks = [asyncio.create_task(my_sleep(secs)) for secs in [2, 5, 7]]
    sleepers = asyncio.gather(*tasks)
    print('awaiting')
    try:
        await sleepers
    except ErrorThatShouldCancelOtherTasks:
        print('Fatal error. Cancelling...')
        for t in tasks:
            print(f'Cancelling {t}')
            print(t.cancel())
    finally:
        await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(main_cancel_future())