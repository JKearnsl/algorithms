import os

from prettytable import PrettyTable

import core
from src.core.utils import chunk_string


def request_filepath(request_text: str = "\n\nВведите путь к файлу") -> str | None:
    print(request_text)
    filepath = input("Путь: ")
    if not os.path.exists(filepath):
        print("Файл не найден")
        return
    return filepath


def encode_interval_lz78():
    filepath = request_filepath("\n\nВведите путь к файлу, который нужно закодировать")

    with open(filepath, "r") as file:
        data = file.read()

    result_interval_coding = core.ic.encode(data)
    result_lz78 = core.lz78.encode(result_interval_coding.hex())

    table_lz78 = PrettyTable()
    table_lz78.field_names = ["Символ", "Код", "Индекс"]
    for symbol, (code, index) in result_lz78[1].items():
        table_lz78.add_row([symbol, code, index])
    print(table_lz78)

    encode_filepath = filepath + ".encode"
    with open(encode_filepath, "wb") as file:
        file.write(result_lz78[0])

    print("Файл успешно закодирован")
    print("Результат сохранен в файл: ", encode_filepath)


def decode_interval_lz78():
    filepath = request_filepath("\n\nВведите путь к файлу, который нужно раскодировать")

    with open(filepath, "rb") as file:
        raw_data = file.read()

    result_lz78 = core.lz78.decode(raw_data)
    data = b""
    try:
        data = bytes.fromhex(result_lz78[0])
    except ValueError:
        for code in chunk_string(result_lz78[0], 2):
            try:
                data += bytes.fromhex(code)
            except ValueError:
                continue
    result_interval_coding = core.ic.decode(data)
    table = PrettyTable()
    table.field_names = ["Индекс", "Символ", "Код"]
    for index, (symbol, code) in result_lz78[1].items():
        table.add_row([index, symbol, code])
    print(table)

    decode_filepath = filepath + ".decode"
    with open(decode_filepath, "w") as file:
        file.write(result_interval_coding)

    print("Файл успешно раскодирован")
    print("Результат сохранен в файл: ", decode_filepath)


def encode_interval():
    filepath = request_filepath("\n\nВведите путь к файлу, который нужно закодировать")

    with open(filepath, "r") as file:
        data = file.read()

    result_interval_coding = core.ic.encode(data)

    encode_filepath = filepath + ".encode"
    with open(encode_filepath, "wb") as file:
        file.write(result_interval_coding)

    print("Файл успешно закодирован")
    print("Результат сохранен в файл: ", encode_filepath)


def decode_interval():
    filepath = request_filepath("\n\nВведите путь к файлу, который нужно раскодировать")

    with open(filepath, "rb") as file:
        raw_data = file.read()

    result_interval_coding = core.ic.decode(raw_data)

    decode_filepath = filepath + ".decode"
    with open(decode_filepath, "w") as file:
        file.write(result_interval_coding)

    print("Файл успешно раскодирован")
    print("Результат сохранен в файл: ", decode_filepath)


def encode_lz78():
    filepath = request_filepath("\n\nВведите путь к файлу, который нужно закодировать")

    with open(filepath, "r") as file:
        data = file.read()

    result_lz78 = core.lz78.encode(data)

    table = PrettyTable()
    table.field_names = ["Символ", "Код", "Индекс"]
    for symbol, (code, index) in result_lz78[1].items():
        table.add_row([symbol, code, index])
    print(table)

    encode_filepath = filepath + ".encode"
    with open(encode_filepath, "wb") as file:
        file.write(result_lz78[0])

    print("Файл успешно закодирован")
    print("Результат сохранен в файл: ", encode_filepath)


def decode_lz78():
    filepath = request_filepath("\n\nВведите путь к файлу, который нужно раскодировать")

    with open(filepath, "rb") as file:
        raw_data = file.read()

    result_lz78 = core.lz78.decode(raw_data)

    table = PrettyTable()
    table.field_names = ["Индекс", "Символ", "Код"]
    for index, (symbol, code) in result_lz78[1].items():
        table.add_row([index, symbol, code])
    print(table)

    decode_filepath = filepath + ".decode"
    with open(decode_filepath, "w") as file:
        file.write(result_lz78[0])

    print("Файл успешно раскодирован")
    print("Результат сохранен в файл: ", decode_filepath)


def main():
    while True:
        print("\n\nЧто вы хотите сделать?")
        print("1. Закодировать файл [Интервальное + LZ78]")
        print("2. Раскодировать файл [Интервальное + LZ78]")
        print("3. Закодировать файл [Интервальное]")
        print("4. Раскодировать файл [Интервальное]")
        print("5. Закодировать файл [LZ78]")
        print("6. Раскодировать файл [LZ78]")
        print("7. Выход")
        choice = input("Ваш выбор: ")
        if choice == "1":
            encode_interval_lz78()
        elif choice == "2":
            decode_interval_lz78()
        elif choice == "3":
            encode_interval()
        elif choice == "4":
            decode_interval()
        elif choice == "5":
            encode_lz78()
        elif choice == "6":
            decode_lz78()
        elif choice == "7":
            break
        else:
            print("Неверный ввод")


if __name__ == "__main__":
    main()
