"""

    Упорядоченное разбиение множества заданий

"""
import math

from lab1.algorithms.hdmt import distribute


def main(matrix: list[list[int]]):
    if (steps := math.log2(len(matrix[0]))) % 1 != 0:
        print("Ошибка. Число процессоров должно быть степенью двойки")
        return

    tasks = [0] * len(matrix)
    for i in range(len(matrix)):
        tasks[i] = matrix[i][0]
    tasks.sort(reverse=True)

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = tasks[i]

    print("\nОтсортированная матрица:")
    for row in matrix:
        print("\t".join(map(str, row)))

    processors = [tasks]
    buffer = []
    for step in range(1, int(steps) + 1):
        for processor in processors:
            buffer.extend(distribute(processor, 2))
        processors = buffer
        buffer = []

        print(f"\nШаг {step}:")
        for i, processor in enumerate(processors):
            print(f"Процессор {i + 1}: {processor}", "\t", sum(processor))

    print(f"Максимальная нагрузка: {max(sum(processor) for processor in processors)}")


if __name__ == "__main__":
    data = [
        [22, 22, 22, 22, 22, 22, 22, 22],
        [18, 18, 18, 18, 18, 18, 18, 18],
        [18, 18, 18, 18, 18, 18, 18, 18],
        [18, 18, 18, 18, 18, 18, 18, 18],
        [16, 16, 16, 16, 16, 16, 16, 16],
        [11, 11, 11, 11, 11, 11, 11, 11],
        [10, 10, 10, 10, 10, 10, 10, 10],
        [8, 8, 8, 8, 8, 8, 8, 8],
        [7, 7, 7, 7, 7, 7, 7, 7],
        [2, 2, 2, 2, 2, 2, 2, 2],
    ]

    main(data)
