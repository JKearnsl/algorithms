import logging

from src.core import hamming


def encode():
    value = input("\n\nВведите последовательность бит: ")
    print("Результат: ", hamming.encode(value))


def decode():
    value = input("\n\nВведите последовательность бит: ")
    print("Результат: ", hamming.decode(value))


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s - %(message)s'
    )

    while True:
        print("\n\nЧто вы хотите сделать?")
        print("1. Закодировать последовательность")
        print("2. Раскодировать последовательность")
        print("3. Выход")
        choice = input("Ваш выбор: ")
        if choice == "1":
            encode()
        elif choice == "2":
            decode()
        elif choice == "3":
            break
        else:
            print("Неверный ввод")


if __name__ == "__main__":
    main()
