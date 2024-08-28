from typing import Sequence, List, TypeVar

T = TypeVar('T')


def find(a0: Sequence[T], a1: Sequence[T]) -> List[T]:
    # Создаем матрицу для хранения длин LCS
    m = len(a0)
    n = len(a1)
    matrix = [[0] * (n + 1) for _ in range(m + 1)]

    # Заполняем матрицу снизу вверх
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                matrix[i][j] = 0
            elif a0[i - 1] == a1[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1] + 1
            else:
                matrix[i][j] = max(matrix[i - 1][j], matrix[i][j - 1])

    # Теперь matrix[m][n] содержит длину LCS a0[0..m-1] и a1[0..n-1]

    # Создаем массив символов для хранения самого LCS
    lcs = [''] * (matrix[m][n] + 1)
    lcs[matrix[m][n]] = ''

    # Начинаем с правого нижнего угла и
    # по одному сохраняем символы в lcs[]
    i = m
    j = n
    while i > 0 and j > 0:
        # Если текущий символ в a0[] и a1[] одинаков, то
        # текущий символ является частью LCS
        if a0[i - 1] == a1[j - 1]:
            lcs[matrix[i][j] - 1] = a0[i - 1]
            i -= 1
            j -= 1
        # Если не совпадают, то находим большее из двух и
        # идем в направлении большего значения
        elif matrix[i - 1][j] > matrix[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return lcs[:-1]


if __name__ == '__main__':
    sequence1 = [1, 2, 3, 4, 5, 6]
    sequence2 = [2, 3]

    result = find(sequence1, sequence2)
    print("Наибольшая общая подпоследовательность: ", result)
