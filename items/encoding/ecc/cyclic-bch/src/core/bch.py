import logging

from src.core.cyclic import encode as cyclic_encode, calc_syndrome, BinStr

"""

Описание алгоритма БЧХ
Пусть информационный полином P(x) был закодирован образующим полиномом G(x) и была получена кодовая комбинация C(x). 
Если при делении кодовой комбинации на образующий полином получился ненулевой остаток, то значит существует ошибка, 
которую можно исправить следующим алгоритмом:
1. Получить остаток R(x) при делении кодовой комбинации C(x) на образующий полином G(x).
2. Подсчитать количество единиц в остатке.
3. Если количество единиц в остатке больше, чем количество t исправляемых данным образующим многочленом ошибок, 
то произвести циклический сдвиг кодовой комбинации C(x) влево на один бит. Перейти на шаг 1.
4. Прибавить по модулю два к кодовой комбинации C(x) остаток R(x).
5. Выполнить циклический сдвиг кодовой комбинации C(x) вправо на столько же бит, на сколько она перед этим была сдвинута 
влево.
Порождающий полином G(x) = 1011. 
Информационный код P(x) = 1010. 
Параметры порождающего полинома: 
n = 7 - количество бит в кодовой комбинации,
k = 4 - количество бит в информационном коде,
t = 1 - количество исправляемых ошибок.

Построим систематизированный код:
1. Степень G(x) равна 3, поэтому P(x) * 1000 = 1010 * 1000 = 1010000
2. Остаток R(x) = 1010000 mod G(x) = 1010000 mod 1011 = 11
3. Кодовая комбинация C(x) = 1010000 + R(x) = 1010011
Теперь для проверки нахождения и исправления ошибок внесём в кодовую комбинацию ошибку: С(x) = 0010011.
Производим декодирование:
1. R(x) := C(x) mod G(x) = 101
2. Количество единиц в остатке R(x) больше, чем t. Производим циклический сдвиг влево:
3. C(x) := 0100110
4. R(x) := C(x) mod G(x) = 1
5. Количество единиц в остатке R(x) равно t. Произведём сложение по модулю 2:
6. C(x) := C(x) + 1 = 0100111
7. Производим циклический сдвиг C(x) обратно вправо:
8. C(x) := 1010011


"""


def encode(to_encode: BinStr, polynom: BinStr):
    """
    :param to_encode:
    :param polynom:
    :return:
    """
    return cyclic_encode(to_encode, polynom)


def decode(to_decode: str, polynom: str, t: int):
    shifts = 0

    while True:
        syndrome = calc_syndrome(to_decode, polynom)

        if syndrome.count('1') > t:
            to_decode = to_decode[1:] + to_decode[0]
            shifts += 1
            logging.info(
                f"[Декодирование] [Сдвигов: {shifts}] Кол-во единиц в синдроме больше t ({syndrome.count('1')} > {t})"
                f" Сдвиг влево ( Синдром = {syndrome!r} Исправленная строка = {to_decode!r})"
            )
        else:
            to_decode = xor_polynomials(to_decode, syndrome)
            logging.info(
                f"[Декодирование] [Сдвигов: {shifts}] Кол-во единиц в синдроме меньше или равно t "
                f"({syndrome.count('1')} <= {t}) "
                f"( Синдром = {syndrome!r} Исправленная строка = {to_decode!r})"
            )
            break

    logging.info(f"[Декодирование] Побитовый сдвиг вправо на {shifts} позиций")
    for _ in range(shifts):
        to_decode = to_decode[len(to_decode) - 1] + to_decode[:len(to_decode) - 1]
        logging.info(f"[Декодирование] [{_ + 1}/{shifts}] {to_decode!r}")

    logging.info(f"[Декодирование] Декодирование завершено! Итоговая строка = {to_decode!r}")
    return to_decode[:-len(polynom) + 1]


def xor_polynomials(poly1: BinStr, poly2: BinStr):
    s1 = len(poly1)
    s2 = len(poly2)

    if s1 > s2:
        poly2 = ('0' * (s1 - s2)) + poly2
    elif s2 > s1:
        poly1 = ('0' * (s2 - s1)) + poly1

    result = ['0'] * s1

    for i in range(s1):
        result[i] = '1' if poly1[i] != poly2[i] else '0'

    return ''.join(result)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
    )
    message = '1101010'
    polynom = '111010001'
    t = 2

    encoded_message = encode(message, polynom)
    print(f"Закодированное сообщение: {encoded_message}")

    encoded_message = '000101011110010'

    decoded_message = decode(encoded_message, polynom, t)
    print(f"Декодированное сообщение: {decoded_message}")

    assert decoded_message == message
