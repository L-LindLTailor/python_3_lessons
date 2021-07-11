import asyncio

from decoratorsmy.decorators import async_measure_time


"""
async - используется чтобы сделать функцию корутином.
await - нужен для асинхронного ожидания результат от выполнения корутина.

Код после асинхронного вызова корутина с использованием await будет выполнен
после того как запущенный корутин завершит свое исполнение, т.е. это то что будет исполняться
после того как корутин завершится.

Так же отмечу, что он не является блокирующий, вследствии чего запущенная фн-я
исполняется за 1-у секунду, а не за 3-ы...
"""


async def process():
    """
    Когда мы делаем вызов корутина управление передается вызывающему коду.
    :return:
    """
    print('first')
    await asyncio.sleep(1)
    print('second')


@async_measure_time
async def main():
    await asyncio.gather(process(), process(), process())

if __name__ == '__main__':
    asyncio.run(main())
