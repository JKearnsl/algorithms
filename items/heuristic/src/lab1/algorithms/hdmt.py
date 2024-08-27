"""

    Алгоритм половинного деления множества заданий

"""


def distribute(tasks: list[int], processors: int) -> list[list[int]]:
    processors = [[] for _ in range(processors)]
    for task in tasks:
        min_load_processor = min(range(len(processors)), key=lambda index: sum(processors[index]))
        processors[min_load_processor].append(task)
    return processors


def main(matrix: list[list[int]]):
    if len(matrix[0]) % 2 != 0:
        print("Ошибка. Число процессоров должно быть четным")
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

    step1_processors = distribute(tasks, 2)
    print("1 уровень:")
    for processor, title in zip(step1_processors, ["A", "B"]):
        print(f"Процессор {title}: {processor}", "\t", sum(processor))

    print("\n2 уровень:")
    step2_processors = []
    proc_number = 1
    for processor in step1_processors:
        sub_processors = distribute(processor, len(matrix[0]) // 2)
        step2_processors.extend(sub_processors)
        for sub_processor in sub_processors:
            print(f"Процессор {proc_number}: {sub_processor}", "\t", sum(sub_processor))
            proc_number += 1
    print(f"Максимальная нагрузка: {max(sum(processor) for processor in step2_processors)}")
