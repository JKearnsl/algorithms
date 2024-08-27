"""

    Алгоритм критического пути

"""
import random


def main(matrix: list[list[int]]) -> None:
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

    column = [0] * len(matrix)
    for i in range(len(matrix)):
        column[i] = matrix[i][0]

    if sort_mode in [1, 2]:
        column.sort(reverse=sort_mode == 1)
    else:
        random.shuffle(column)

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = column[i]

    print("\nОтсортированная матрица:")
    for row in matrix:
        print("\t".join(map(str, row)))

    processors = [[] for _ in range(len(matrix[0]))]

    step = 0
    for time in column:
        step += 1
        min_load_processor = min(range(len(processors)), key=lambda index: sum(processors[index]))
        processors[min_load_processor].append(time)

        print(f"Шаг {step}:")
        for i, processor in enumerate(processors):
            print(f"Процессор {i + 1}: {processor}", "\t", sum(processor))
        print(f"Максимальная нагрузка: {max(sum(processor) for processor in processors)}, выполнено за {step} шагов")
