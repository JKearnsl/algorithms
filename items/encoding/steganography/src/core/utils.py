from itertools import islice


def chunks(iterable, size):
    iterator = iter(iterable)
    while chunk := list(islice(iterator, size)):
        yield chunk


DEGREE_BIT_MASK_REVERSE = {
    0: 0b11111111,
    1: 0b11111110,
    2: 0b11111100,
    3: 0b11111000,
    4: 0b11110000,
    5: 0b11100000,
    6: 0b11000000,
    7: 0b10000000,
    8: 0b00000000,
}  # 2 ** (8 - i) - 1
