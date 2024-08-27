"""

    Метод Крона


"""
import random


def main(matrix: list[list[int]]):
    print("\nВхдная матрица:")
    for row in matrix:
        print("\t".join(map(str, row)))

    tasks = [row[0] for row in matrix]
    print("\nВектор T:", tasks)

    # Первичное распределение
    devices = [[] for _ in matrix[0]]
    for i, task in enumerate(tasks):
        devices[random.randint(0, len(devices) - 1)].append(task)


    k = 1
    while True:
        print(f"\nШаг {k}")
        k += 1

        max_len = max(len(str(device)) for device in devices)
        for i, device in enumerate(devices):
            start_str = f"[Устройство {(i + 1)}]:  "
            print(f"{start_str}{device}".ljust(max_len + len(start_str) + 5), f"Сумма: {sum(device)}")

        min_device = min([(sum(device), index) for index, device in enumerate(devices)], key=lambda x: x[0])
        max_device = max([(sum(device), index) for index, device in enumerate(devices)], key=lambda x: x[0])
        delta = max_device[0] - min_device[0]
        print(f"\nmin([Устройство {min_device[1] + 1}]) = {min_device[0]}")
        print(f"max([Устройство {max_device[1] + 1}]) = {max_device[0]}")
        print("[Δ]: ", delta)

        # Проверка
        is_founded_1 = False
        for i, task_time in enumerate(devices[max_device[1]]):
            if task_time < delta:
                print(
                    f"\n[1] (from max){task_time} < (Δ){delta} => Перераспределение "
                    f"{task_time} из [Устройство {max_device[1] + 1}] -> [Устройство {min_device[1] + 1}]"
                )
                devices[min_device[1]].append(task_time)
                devices[max_device[1]].pop(i)
                is_founded_1 = True
                break

        if not is_founded_1:
            is_founded_2 = False
            for i, one_from_max in enumerate(devices[max_device[1]]):
                for j, one_from_min in enumerate(devices[min_device[1]]):
                    if one_from_max <= one_from_min:
                        continue

                    if is_founded_2:
                        break

                    if one_from_max - one_from_min < delta:
                        # Обмен
                        (
                            devices[min_device[1]][j],
                            devices[max_device[1]][i]
                        ) = (
                            devices[max_device[1]][i],
                            devices[min_device[1]][j]
                        )
                        is_founded_2 = True
                        print(
                            f"\n[2] (from max){one_from_max} - (from min){one_from_min} < (Δ){delta} =>  "
                            f"Обмен {one_from_max} из [Устройство {max_device[1] + 1}] -> "
                            f"[Устройство {min_device[1] + 1}]"
                        )
            if not is_founded_2:
                break

    print("\nРезультат:")
    print("\t".join(map(str, [sum(device) for device in devices])),
          f"\t | Max: {max([sum(device) for device in devices])}")


if __name__ == "__main__":
    main(
        [
            [5, 5, 5, 5],
            [10, 10, 10, 10],
            [15, 15, 15, 15],
            [7, 7, 7, 7],
            [4, 4, 4, 4],
            [22, 22, 22, 22],
            [5, 5, 5, 5]
        ]
    )
