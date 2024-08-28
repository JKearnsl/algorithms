from src import lcs


if __name__ == '__main__':
    print("Введите две последовательности чисел, например: 1, 2, 3, 4... ")
    sequence1 = list(map(int, input("[1] Ввод: ").replace(' ', '').split(',')))
    sequence2 = list(map(int, input("[2] Ввод: ").replace(' ', '').split(',')))

    result = lcs.find(sequence1, sequence2)
    print("Наибольшая общая подпоследовательность: ", result)
