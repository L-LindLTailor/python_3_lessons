import sys
import time
from functools import wraps
from numpy import size


def async_measure_time(func):
    """
    Определяет время исполнения асинхронной функции от ее стартовой позиции до окончания
    :param func:
    :return:
    """

    @wraps(func)
    async def wrap(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f'Execute {func} in {elapsed:0.2f} seconds')
        return result

    return wrap


def measure_time(func):
    """
    Определяет время исполнения функции от ее стартовой позиции до окончания
    :param func:
    :return:
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f'Execute {func} in {elapsed:0.2f} seconds')
        return result

    return wrap


def big_o_test(func):
    """
    Определяет вычислительную сложность функции по требованиям Big O
    :param func:
    :return:
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        parametrs_size = 0
        for i in args:
            parametrs_size += len(i)
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        wrap.count += 1
        if wrap.count / parametrs_size < 1:
            big_o_result = f"""The number of processes divided by the length of the parameters {wrap.count / parametrs_size}.
         Computational complexity Big O(logN)"""
        elif 1 <= wrap.count / parametrs_size <= 2:
            big_o_result = f"""The number of processes divided by the length of the parameters {wrap.count / parametrs_size}.
         Computational complexity Big O(N)"""
        elif 2 < wrap.count / parametrs_size <= 4:
            big_o_result = f"""The number of processes divided by the length of the parameters {wrap.count / parametrs_size}.
         Computational complexity Big O(N * N) or O((N * N)logN)"""
        elif wrap.count**2 <= parametrs_size:
            big_o_result = f"""The number of processes divided by the length of the parameters {wrap.count / parametrs_size}.
         Computational complexity Big O(N^2)"""
        else:
            big_o_result = f"""The number of processes divided by the length of the parameters {wrap.count / parametrs_size}.
         Computational complexity Big O(N!)"""
        print(f"""Execute {func} in {elapsed:0.2f} seconds,
         iterations count: {wrap.count},
         func memory count: {sys.getsizeof(result)} bytes,
         {big_o_result}""")
        return result

    wrap.count = 0
    return wrap
