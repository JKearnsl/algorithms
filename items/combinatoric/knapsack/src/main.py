import re

from src.core import discrete, continuous
from src.core.continuous import Item


def discrete_menu():
    print('Введите веса через запятую, например: 1,2,3,4,5')
    weights = list(map(int, input('Ввод: ').replace(' ', '').split(",")))
    print('Введите ценности через запятую, например: 1,2,3,4,5')
    values = list(map(int, input('Ввод: ').replace(' ', '').split(",")))
    print('Введите вместимость рюкзака')
    capacity = int(input('Ввод: '))
    print(
        '\nМаксимальная ценность предметов, которые можно унести в рюкзаке:',
        discrete.knapsack(weights, values, capacity),
        '\n'
    )


def continuous_menu():
    print('Введите вес и ценность каждого предмета в формате: [вес, ценность], например: [1,2],[3,4],[5,6]')
    items = [Item(*map(int, match)) for match in re.findall(r'\[(\d+),(\d+)]', input('Ввод: '))]
    print('Введите вместимость рюкзака')
    capacity = int(input('Ввод: '))
    print(
        '\nМаксимальная ценность предметов, которые можно унести в рюкзаке:',
        continuous.knapsack(items, capacity),
        '\n'
    )


if __name__ == '__main__':
    while True:
        print('Выберите тип задачи:')
        print('1. Дискретная')
        print('2. Непрерывная')
        print('3. Выход')
        choice = int(input('Ввод: '))
        if choice == 1:
            discrete_menu()
        elif choice == 2:
            continuous_menu()
        elif choice == 3:
            break
        else:
            print('Неверный ввод!')
