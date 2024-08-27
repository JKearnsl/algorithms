"""

    Алгоритм построения расписания с нестабильной загрузкой


"""
import random
import unicodedata
from typing import Callable, Any


def calc_column(matrix: list[list], col_index: int, key: Callable[[Any], int | float] = lambda x: x):
    return sum(key(row[col_index]) for row in matrix if key(row[col_index]) is not None)


def to_unicode_power(n: int) -> str:
    unicode_powers = {
        0: 'SUPERSCRIPT ZERO',
        1: 'SUPERSCRIPT ONE',
        2: 'SUPERSCRIPT TWO',
        3: 'SUPERSCRIPT THREE',
        4: 'SUPERSCRIPT FOUR',
        5: 'SUPERSCRIPT FIVE',
        6: 'SUPERSCRIPT SIX',
        7: 'SUPERSCRIPT SEVEN',
        8: 'SUPERSCRIPT EIGHT',
        9: 'SUPERSCRIPT NINE'
    }
    result = ''
    for digit in str(n):
        if int(digit) in unicode_powers:
            result += unicodedata.lookup(unicode_powers[int(digit)])
        else:
            raise ValueError("Unicode does not support this power")
    return result


def main(matrix: list[list[int]]):
    while True:
        try:
            sort_mode = int(
                input(
                    "Как отсортировать?"
                    "\n - 1: По убыванию;"
                    "\n - 2. По возрастанию;"
                    "\n - 3. Случайный порядок "
                    "\n\nВведите номер: "
                )
            )
            if sort_mode not in [1, 2, 3]:
                raise ValueError
            break
        except ValueError:
            print("Ошибка ввода, попробуйте снова")

    if sort_mode in [1, 2]:
        matrix.sort(key=lambda x: sum(x), reverse=sort_mode == 1)
    else:
        random.shuffle(matrix)

    print("\nОтсортированная матрица:")
    for row in matrix:
        print("\t".join(map(str, row)), f"\t | Сумма: {sum(row)}")

    distribut_matrix = [[[None, 0] for _ in range(len(matrix[0]))] for _ in range(len(matrix))]

    print("\nРешение:")
    for row_index, row in enumerate(matrix):
        col_index = min(
            [(distribut_matrix[row_index][i][1] + row[i], i) for i in range(len(row))],
            key=lambda x: x[0]
        )[1]
        minimum = row[col_index]

        distribut_matrix[row_index][col_index][0] = minimum
        for i in range(row_index + 1, len(matrix)):
            distribut_matrix[i][col_index][1] += row[col_index]

    print("\nМатрица:")
    for row in distribut_matrix:
        formatted_row = []
        for element in row:
            if element[0] is not None:
                formatted_element = f"\033[1;31m{element[0]}\033[0m"
            else:
                formatted_element = "\033[0m0\033[0m"
            formatted_element += to_unicode_power(element[1])
            formatted_row.append(formatted_element.ljust(len(formatted_element) - formatted_element.count('\033') + 5))
        print("\t".join(formatted_row))

    result = [calc_column(distribut_matrix, i, lambda x: x[0]) for i in range(len(distribut_matrix[0]))]
    print("\nРезультат:")
    print("\t".join(map(str, result)), f"\t | Max: {max(result)}")


if __name__ == "__main__":
    main(
        [[60, 47, 8, 15],
         [59, 11, 32, 78],
         [32, 31, 91, 6],
         [81, 85, 16, 61],
         [54, 67, 6, 25],
         [82, 1, 61, 71],
         [32, 73, 46, 51],
         [93, 80, 25, 88],
         [18, 37, 82, 85],
         [72, 88, 6, 16]]
    )
