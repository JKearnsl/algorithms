"""

    Реализация интервального кодирования


"""
import math
import pickle
from collections import Counter
from decimal import getcontext, Decimal

from src.core.utils import chunk_string


class Interval:
    def __init__(self, left: float | int | Decimal, right: float | int | Decimal):
        self.points: list[tuple[Decimal, str | None]] = [(Decimal(left), None), (Decimal(right), None)]
        self.points.sort(key=lambda item: item[0])
        self.label = None
        getcontext().prec = 10

    def __contains__(self, item: Decimal):
        return self.left <= item <= self.right or math.isclose(item, self.left) or math.isclose(item, self.right)

    @property
    def left(self) -> Decimal:
        return self.points[0][0]

    @left.setter
    def left(self, value: tuple[Decimal, str]):
        self.points[0] = value
        self.points.sort(key=lambda item: item[0])

    @property
    def right(self) -> Decimal:
        return self.points[-1][0]

    @right.setter
    def right(self, value: tuple[Decimal, str]):
        self.points[-1] = value
        self.points.sort(key=lambda item: item[0])

    def set_point(self, value: Decimal, label: str):
        if value not in self:
            raise ValueError(f"Point {value} not in {self}")

        if self.left <= value <= self.right:
            for point in self.points:
                if Decimal(point[0]) == Decimal(value):
                    index = self.points.index(point)
                    self.points.remove(point)
                    self.points.insert(index, (Decimal(value), label))
                    return
        elif self.right < value:
            self.right = value, label
            return
        elif value < self.left:
            self.left = value, label
            return

        self.points.append((Decimal(value), label))
        self.points.sort(key=lambda item: item[0])

    def get_interval(self, *, value: Decimal = None, label: str = None) -> "Interval | None":
        if value is None and label is None:
            raise ValueError("value or label must be not None")

        for interval in self.intervals():
            if value and value in interval:
                return interval
            if label and interval.label == label:
                return interval
        return None

    def intervals(self) -> 'list[Interval]':
        result = []
        for i in range(len(self.points) - 1):
            point_from = self.points[i]
            point_to = self.points[i + 1]
            interval = Interval(point_from[0], point_to[0])
            interval.label = self.points[i + 1][1]
            result.append(interval)
        return result

    def length(self) -> Decimal:
        return self.right - self.left

    def __str__(self):
        if len(self.points) > 2:
            return f"{self.__class__.__name__}{[interval for interval in self.intervals()]}]"
        return f"{self.label if self.label else ""}{tuple(point[0] for point in self.points)}"

    def __repr__(self):
        return str(self)


def get_alphabet(data: str) -> dict[str, Decimal]:
    return {alpha: Decimal(count) / Decimal(len(data)) for alpha, count in Counter(data).items()}


def pack(data: list[tuple[Decimal, int, dict[str, Decimal]]]) -> bytes:
    return b'\xFF'.join(pickle.dumps(item) for item in data)


def unpack(raw_data: bytes) -> list[tuple[Decimal, int, dict[str, Decimal]]]:
    data = raw_data.split(b'\xFF')
    chunks = []
    for item in data:
        try:
            chunks.append(pickle.loads(item))
        except (pickle.UnpicklingError, ValueError, UnicodeDecodeError) as error:
            print(f"Ошибочный чанк {item}", error)
            continue
        except EOFError:
            print(f"Ошибка EOF чанк {item}")
            continue
        except OverflowError as error:
            print(f"Ошибка {error} чанк {item}")
            continue
    return chunks


def encode(data: str) -> bytes:
    encode_scope = []
    for chunk in chunk_string(data, 10):
        alphabet = get_alphabet(chunk)
        last_alpha = [key for key in alphabet.keys()][-1]

        interval = Interval(0, 1)
        prev = Decimal(0)
        for alpha, prob in alphabet.items():
            prev += prob
            if alpha == last_alpha:
                # Из-за погрешности
                interval.right = prev, alpha
                break
            interval.set_point(prev, alpha)

        # Сжатие
        for symbol in chunk:
            interval = interval.get_interval(label=symbol)
            if chunk.index(symbol) == len(chunk) - 1:
                break

            prev = interval.left
            for alpha, prob in alphabet.items():
                prev += interval.length() * prob
                if alpha == last_alpha:
                    # Из-за погрешности
                    interval.right = prev, alpha
                    break
                interval.set_point(prev, alpha)
        encode_scope.append((
            Decimal((interval.left + interval.right) / 2),
            len(chunk),
            alphabet
        ))
    return pack(encode_scope)


def decode(raw_data: bytes) -> str:
    data_list = unpack(raw_data)
    decode_scope = []
    for data, length, alphabet in data_list:
        last_alpha = [key for key in alphabet.keys()][-1]

        interval = Interval(0, 1)
        prev = Decimal(0)
        for alpha, prob in alphabet.items():
            prev += prob
            if alpha == last_alpha:
                # Из-за погрешности
                interval.right = prev, alpha
                break
            interval.set_point(prev, alpha)

        buffer = []
        # Распаковка
        counter = 0
        while counter < length:
            for item in interval.intervals():
                if data in item:
                    interval = item
                    buffer.append(item.label)
                    break

            prev = interval.left
            for alpha, prob in alphabet.items():
                prev += interval.length() * prob
                if alpha == last_alpha:
                    # Из-за погрешности
                    interval.right = prev, alpha
                    break
                interval.set_point(prev, alpha)
            counter += 1
        decode_scope.append("".join(buffer))

    return "".join(decode_scope)


if __name__ == '__main__':
    # message = "abcdefghij"
    message = "Привет мир, я так рад тут находиться, что пишу это письмо прямо для вас!"
    print(message)
    encoded = encode(message)
    print(encoded)
    print(len(encoded))
    decoded = decode(encoded)
    print(decoded)
    print(message == decoded)
