"""
    Модуль сокрытия изображения в изображении путем изменения наименее значимых бит

    Используется метод LSB
"""
import os

from PIL import Image
from PIL.PyAccess import PyAccess

from src.core.utils import DEGREE_BIT_MASK_REVERSE, chunks

PathLike = str | os.PathLike


def hide(cover_path: PathLike, img_path: PathLike, output_dir: PathLike, degree_count: int) -> PathLike:
    if not (1 <= degree_count <= 8):
        raise ValueError("Степень должна быть от [1, 8]")

    container = Image.open(cover_path)
    data = Image.open(img_path)

    if container.format != "BMP":
        raise ValueError("Ошибка: Контейнер должен быть формата BMP")

    if data.format != "BMP":
        raise ValueError("Ошибка: Данные для скрытия должны быть формата BMP")

    container_pixels: PyAccess = container.load()
    data_pixels: PyAccess = data.load()

    result_path = os.path.join(output_dir, f"hidden_{degree_count}.png")

    data_byte_count = data.size[0] * data.size[1] * 3
    container_byte_count = (container.size[0] * container.size[1] * 3 * degree_count) // 8
    if data_byte_count > container_byte_count:
        raise ValueError(
            f"Размер данных для скрытия больше размера контейнера "
            f"{data_byte_count=} vs {container_byte_count=}"
        )

    chunked_data_bits = chunks(
        (
            bit
            for i in range(data.size[0])
            for j in range(data.size[1])
            for value in data_pixels[i, j]
            for bit in format(value, '08b')
        ),
        degree_count
    )
    for i in reversed(range(container.height)):
        for j in range(container.width):
            container_pixel = list(container_pixels[j, i])

            for channel in range(3):
                data_bits = next(chunked_data_bits, None)
                if data_bits is None:
                    break

                if len(data_bits) < degree_count:
                    data_bits += "0" * (degree_count - len(data_bits))

                container_pixel[channel] = (
                        container_pixel[channel] &
                        DEGREE_BIT_MASK_REVERSE[degree_count] +
                        int(f"0b{''.join(data_bits)}", 2)
                )
            container_pixels[j, i] = tuple(container_pixel)

    container.save(result_path, format="BMP")
    return result_path


def reveal(img_path: str, output_dir: str, degree_count: int) -> str:
    if not (1 <= degree_count <= 8):
        raise ValueError("Степень должна быть от [1, 8]")

    img = Image.open(img_path)
    img_pixels: PyAccess = img.load()

    if img.format != "BMP":
        raise ValueError("Ошибка: изображение должно быть типа BMP")

    reveal_path = os.path.join(output_dir, f"revealed_{degree_count}sl.png")
    buffer = []
    for i in reversed(range(img.height)):
        for j in range(img.width):
            img_pixel = list(img_pixels[j, i])

            for channel in range(3):
                buffer.append(format(img_pixel[channel], '08b')[-degree_count:])

    data_bits = (bit for bit in ''.join(buffer))
    data_bytes_iter = iter((int(''.join(bits), 2) for bits in chunks(data_bits, 8)))
    for i in reversed(range(img.height)):
        for j in range(img.width):
            img_pixel = list(img_pixels[j, i])

            for channel in range(3):
                color_byte = next(data_bytes_iter, None)
                if color_byte is None:
                    break
                img_pixel[channel] = color_byte
            img_pixels[j, i] = tuple(img_pixel)

    img.save(reveal_path, format="BMP")
    return reveal_path
