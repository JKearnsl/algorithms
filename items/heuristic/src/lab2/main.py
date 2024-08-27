import random

from lab2.algorithms import (
    acsul
)


def main():
    while True:
        try:
            n = int(input("Введите число процессоров: "))
            break
        except ValueError:
            print("Введено неверное значение процессоров, повторите попытку")
            continue

    while True:
        try:
            m = int(input("Введите число заданий: "))
            break
        except ValueError:
            print("Введено неверное значение заданий, повторите попытку")
            continue

    while True:
        try:
            print("Введите диапазон значений через запятую, например: 1, 10")
            random_range = tuple(map(lambda x: int(x), input("Ввод: ").strip(" ").split(",")))
            if len(random_range) != 2:
                raise ValueError
            break
        except ValueError:
            print("Введен неверный диапазон, повторите попытку")
            continue

    matrix = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            matrix[i][j] = random.randint(*sorted(random_range))

    print("\nМатрица:")
    for row in matrix:
        print("\t".join(map(str, row)))

    while True:
        print("\nЧто будем делать?")
        print("1. Алгоритм построения расписания с произвольной загрузкой")
        print("4. Выход")

        request = input("Ввод: ")
        match request:
            case "1":
                acsul.main(matrix)
            case "4":
                break
            case _:
                print("Неверный ввод, повторите попытку")
                continue


if __name__ == "__main__":
    main()
