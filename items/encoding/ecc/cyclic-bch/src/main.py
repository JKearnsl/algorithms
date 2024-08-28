import logging

from src.core.utils import polynom_bch_table, DICT_POLYNOM_BCH
from src.core.bch import encode, decode


def encode_dialog():
    print("Выберите порождающий полином:")
    print(polynom_bch_table())
    index = int(input("Введите номер полинома: "))
    polynom = DICT_POLYNOM_BCH[index]
    print(f"Порождающий полином: {polynom[1]} / {polynom[2]}")
    to_encode = input(f"\nВведите bin строку для кодирования({polynom[3][1]} символов): ")
    assert len(to_encode) == polynom[3][1], "Неверная длина строки"
    print(f"Результат кодирования: {encode(to_encode, polynom[2])}\n")


def decode_dialog():
    print("Выберите порождающий полином:")
    print(polynom_bch_table())
    index = int(input("Введите номер полинома: "))
    polynom = DICT_POLYNOM_BCH[index]
    to_decode = input(f"\nВведите bin строку для декодирования({polynom[3][0]} символов): ")
    assert len(to_decode) == polynom[3][0], "Неверная длина строки"
    print(f"Порождающий полином: {polynom[1]} / {polynom[2]}")
    print(f"Результат декодирования: {decode(to_decode, polynom[2], polynom[3][2])}\n")


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
    )

    print("Что вы хотите сделать?")
    while True:
        print("1. Закодировать")
        print("2. Декодировать")
        print("3. Выйти")
        choice = input("Выберите действие: ")
        if choice == "1":
            encode_dialog()
        elif choice == "2":
            decode_dialog()
        elif choice == "3":
            break
        else:
            print("Неверный ввод")
        print()
