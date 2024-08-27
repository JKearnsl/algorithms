import os

from src.core import steganography


def request_int(request_text: str = "\n\nВведите число") -> int | None:
    print(request_text)
    value = input("Ввод: ")
    if not value.isdigit():
        print("Значение не является числом")
        return None
    return int(value)


def request_filepath(request_text: str = "\n\nВведите путь к файлу") -> str | None:
    print(request_text)
    filepath = input("Путь: ")
    if not os.path.exists(filepath):
        print("Файл не найден")
        return
    return filepath


def encode_file():
    pass


def decode_file():
    pass


def hide_image():
    filepath_cover = request_filepath("\n\nВведите путь к изображению-контейнеру [BMP]")
    filepath_img = request_filepath("Введите путь к изображению, которое нужно спрятать [BMP]")
    degree_count = request_int("Введите степень записи:")
    output_dir = os.path.dirname(filepath_img)

    result_path = steganography.hide(
        cover_path=filepath_cover,
        img_path=filepath_img,
        output_dir=output_dir,
        degree_count=degree_count
    )
    print("Файл успешно спрятан")
    print("Результат сохранен в файл: ", result_path)


def reveal_image():
    filepath_img = request_filepath("\n\nВведите путь к изображению, которое нужно раскрыть")
    degree_count = request_int("Введите степень записи:")
    output_dir = os.path.dirname(filepath_img)

    if not (1 <= degree_count <= 8):
        print("Ошибка: Степень должна быть от [1, 8]")
        return

    result_path = steganography.reveal(img_path=filepath_img, output_dir=output_dir, degree_count=degree_count)
    print("Файл успешно раскрыт")
    print("Результат сохранен в файл: ", result_path)


def main():
    while True:
        print("\n\nЧто вы хотите сделать?")
        print("1. Закодировать изображение")
        print("2. Раскодировать изображение")
        print("3. Скрыть изображение")
        print("4. Раскрыть изображение")
        print("5. Выход")
        choice = input("Ваш выбор: ")
        if choice == "1":
            encode_file()
        elif choice == "2":
            decode_file()
        elif choice == "3":
            hide_image()
        elif choice == "4":
            reveal_image()
        elif choice == "5":
            break
        else:
            print("Неверный ввод")


if __name__ == "__main__":
    main()
