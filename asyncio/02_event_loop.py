import asyncio


"""
async / await - должны быть вызваны по всей связанной системе корутинов, иначе
по окончаюнию работы нити, последующий(е) процесс(ы), прекратят исполняться.
await - по сути - awaitable-object.
"""


async def process():
    """
    Когда мы делаем вызов корутина управление передается вызывающему коду.
    Можно так же отследить состояние самого loop.
    :return:
    """
    print('first')
    await asyncio.sleep(1)
    print('second')

    loop_run = asyncio.get_running_loop()
    if loop_run.is_running():
        print('loop is still running')


async def main():
    """
    awaitable-object в данном случае возвращается gather(), а не корутином.
    Так же мы можем отследить состояние event loop задач.
    :return:
    """
    awaitable_object = asyncio.gather(process(), process(), process())

    for task in asyncio.all_tasks():
        print(task, end='\n')

    await awaitable_object

if __name__ == '__main__':
    """
    Можно так же управлять потоками в ручную, пример в комментариях ниже.
    """
    loop = asyncio.get_event_loop()
    try:
        # loop.create_task(main())
        # loop.run_forever()
        loop.run_until_complete(main())
        print('coroutines have finished')
    # except KeyboardInterrupt: тут мы можем прервать бесконечный цикл вызова например ctrl + c в консоли
        # print('Manually closed application')
    finally:
        loop.close()
        print('loop is closed')
        # print('loop is closed = {loop.is_closed()}')
