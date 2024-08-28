"""

    Реализация алгоритма сжатия LZ78


"""


def encode(data: str) -> tuple[bytes, dict[str, tuple[str, int]]]:
    table = {
        "": ("", 0),
    }
    buffer = ''
    for symbol in data:
        prev_buffer = buffer
        buffer += symbol
        if buffer not in table:
            code = f"{table[prev_buffer][1]}{symbol}"
            table[buffer] = (
                code,
                len(table)
            )
            buffer = ''

    if buffer is not None:
        table[buffer + "NoN"] = (f"{table[prev_buffer][1]}{symbol}", len(table))

    return b'\xFF'.join(
        buffer[0].encode('utf8') for buffer in table.values() if buffer[0] != ""
    ), table


def decode(data: bytes) -> tuple[str, dict[int, tuple[str, str]]]:
    codes = []
    for token in data.split(b'\xFF'):
        try:
            decode_value = token.decode('utf8')
        except UnicodeDecodeError:
            continue
        index = decode_value[:-1]
        symbol = decode_value[-1]
        codes.append((index, symbol))

    # Декодирование

    table = {
        0: ("", "")
    }
    for code in codes:
        real_index = len(table)

        # Защита при некорректных данных
        try:
            index = int(code[0])
        except ValueError:
            index = 0

        if index not in table:
            table[index] = ("", "")

        # Декодирование
        symbol = code[1]
        table[real_index] = (
            table[index][0] + symbol,
            "".join(code)
        )

    return ''.join(
        buffer[1][0]
        for buffer
        in sorted(table.items(), key=lambda item: item[0])
        if buffer[1][0] != ""
    ), table
