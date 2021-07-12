"""
Имеются два отсортированных числовых массива длины М и N,
элементы в каждом массиве могут повторяться.
Необходимо найти длину к наибольшей общей последовательности.
Какова вычислительная сложность данной задачи?

a = [111, 122, 144, 145, 145, 167, 167, 167, 200, 201]
b = [1, 4, 7677, 78, 78, 113, 132, 145, 145, 145, 167, 167, 167, 200, 250, 290]

a = [111, 122, 144, 145, 145, 167, 167, 167, 200, 201]
b = [1, 4, 76, 77, 78, 78, 113, 132, 145, 145, 145, 167, 167, 167, 200, 250, 290]

a = [0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 3]
b = [0, 1, 1, 2, 3, 3, 3, 3]

a = [5, 5, 5, 5, 5, 6 ,6, 6, 8, 8]
b = [5, 5, 5, 6, 7, 8, 8]

a = [-2, 0, 0, 0, 0, 2, 3]
b = [-2, 0, 0, 2, 3]

a = [0, 4, 10, 12, 35]
b = [-2, 0, 4, 6, 7, 8, 10, 10]

a = [1, 2, 2, 2, 3, 5, 5]
b = [-1, 0, 0, 1, 2, 2, 3, 3, 5, 5]

a = [1, 2, 2, 3, 3]
b = [2, 3, 3, 4]

a = [1, 2, 3, 4, 4, 5, 6, 7]
b = [-3, -2, 1, 2, 3, 3, 3, 4, 4, 5, 5, 6, 7, 7, 7, 7 ,7]

a = [1, 5, 10, 15, 20]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 16, 20]

Условие: - решение должно быть линейным ; - максимальная сложность Big O((N * N) * lonN)
"""
from typing import List
from decoratorsmy.decorators import big_o_test

arr_main = [111, 122, 144, 145, 145, 167, 167, 167, 200, 201]
arr_nominal = [1, 4, 76, 77, 78, 78, 113, 132, 145, 145, 145, 167, 167, 167, 200, 250, 290]


def lcs_len(arr_m: List[int], arr_n: List[int]):
    current = [0] * (1 + len(arr_n))

    for arr_m_elem in arr_m:
        prev = current[:]
        for n_i, n_elem in enumerate(arr_n):
            if arr_m_elem == n_elem:
                current[n_i + 1] = prev[n_i] + 1
            else:
                current[n_i + 1] = max(current[n_i], prev[n_i + 1])
    return current


@big_o_test
def general_subsequence(arr_m: List[int], arr_n: List[int]) -> List[int]:
    """
    Задача решена с помощью Алгоритма Хишберга (Hirschberg).
    :param arr_m: List[int]
    :param arr_n: List[int]
    :return: List[int]
    """
    arr_m_len = len(arr_m)
    if arr_m_len == 0:
        return []
    elif arr_m_len == 1:
        if arr_m[0] in arr_n:
            return [arr_m[0]]
        else:
            return []
    else:
        i = arr_m_len // 2
        arr_mb, arr_me = arr_m[:i], arr_m[i:]
        len_arr_n = lcs_len(arr_mb, arr_n)
        len_arr_m = reversed(lcs_len(arr_me[::-1], arr_n[::-1]))
        sum_arrays = (l1 + l2 for l1, l2 in zip(len_arr_n, len_arr_m))
        _, j = max((sum_val, sum_i) for sum_i, sum_val in enumerate(sum_arrays))
        nb, ne = arr_n[:j], arr_n[j:]
        return general_subsequence(arr_mb, nb) + general_subsequence(arr_me, ne)


print('Длина к наибольшей общей последовательности:',
      len(general_subsequence(arr_main, arr_nominal)),
      '. Наибольшая общая последовательность:',
      general_subsequence(arr_main, arr_nominal))

"""
y_matchlist = {}

for index, elem in enumerate(y):
    indexes = y_matchlist.setdefault(elem, [])
    indexes.append(index)
    y_matchlist[elem] = indexes

m_length, y_length = len(x), len(y)
min_length = min(m_length, y_length)
THRESH = list(itertools.repeat(y_length, min_length + 1))
LINK_s1 = list(itertools.repeat(None, min_length + 1))
LINK_s2 = list(itertools.repeat(None, min_length + 1))
THRESH[0], t = -1, 0

for x_index, x_elem in enumerate(x):
    y_indexes = y_matchlist.get(x_elem, [])
    for y_index in reversed(y_indexes):
        k_start = bisect_left(THRESH, y_index, 1, t)
        k_end = bisect_right(THRESH, y_index, k_start, t)
        for k in range(k_start, k_end + 2):
            if THRESH[k - 1] < y_index < THRESH[k]:
                THRESH[k] = y_index
                LINK_x[k] = (x_index, LINK_x[k - 1])
            if k > t:
                t = k
"""
