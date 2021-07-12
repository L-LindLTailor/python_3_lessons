import asyncio

from decoratorsmy.decorators import async_measure_time


"""
приставка async - перобразует функцию в корутин.
приставка await - нужна для асинхронного ожидания результата выполнения корутина.

Код после асинхронного вызова корутина с использованием await будет выполнен
после того как запущенный корутин завершит свое исполнение, т.е. это то что будет исполняться
после того как корутин завершится.

Так же отмечу, что он не является блокирующим, вследствии чего запущенная фн-я
исполняется за 1-у секунду, а не за 3-и...
"""


async def process():
    """
    Когда мы делаем вызов корутина - управление передается вызывающему коду.
    """
    print('first')
    await asyncio.sleep(1)
    print('second')


@async_measure_time
async def main():
    await asyncio.gather(process(), process(), process())

if __name__ == '__main__':
    asyncio.run(main())
