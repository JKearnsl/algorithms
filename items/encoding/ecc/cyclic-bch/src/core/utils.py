from prettytable import PrettyTable

DICT_POLYNOM_CYCLIC = {
    1: (1, "x + 1", "11", (3, 2)),
    2: (2, "x^2 + x + 1", "111", (3, 1)),
    3: (3, "x^3 + x^2 + 1", "1101", (7, 4)),
    4: (3, "x^3 + x + 1", "1011", (7, 4)),
    5: (4, "x^4 + x^3 + 1", "11001", (15, 11)),
    6: (4, "x^4 + x + 1", "10011", (15, 11)),
    7: (4, "x^4 + x^2 + x + 1", "10111", (7, 3)),
    8: (4, "x^4 + x^3 + x^2 + x + 1", "11101", (7, 3)),
    9: (5, "x^5 + x^2 + 1", "100101", (31, 26)),
    10: (5, "x^5 + x^3 + 1", "101001", (31, 26))
}

DICT_POLYNOM_BCH = {
    1: (3, "x^3 + x + 1", "1011", (7, 4, 1)),
    2: (8, "x^8 + x^7 + x^6  x^4 + 1", "111010001", (15, 7, 2)),
}


def polynom_cyclic_table() -> str:
    pretty_table = PrettyTable()
    pretty_table.field_names = ["№", "r-степень полинома", "Порождающий полином", "Запись по mod 2", "(n, k)"]
    pretty_table.align = "l"
    for index, values in DICT_POLYNOM_CYCLIC.items():
        pretty_table.add_row([index, values[0], values[1], values[2], values[3]])
    return pretty_table.get_string()


def polynom_bch_table() -> str:
    pretty_table = PrettyTable()
    pretty_table.field_names = ["№", "r-степень полинома", "Порождающий полином", "Запись по mod 2", "(n, k, t)"]
    pretty_table.align = "l"
    for index, values in DICT_POLYNOM_BCH.items():
        pretty_table.add_row([index, values[0], values[1], values[2], values[3]])
    return pretty_table.get_string()


def build_syndrome_cyclic_matrix(get_syndrome, polynom, k):
    n = len(polynom) - 1
    matrix = [[0] * n for _ in range(2 ** n - 1)]

    for i in range(2 ** n - 1):
        binary = "".join(map(lambda x: '1' if x[0] == i else '0', enumerate(['0'] * (n + k))))

        syndrome = get_syndrome(binary, polynom)

        matrix[i] = list(map(int, syndrome))

    matrix.reverse()
    return matrix


def syndrome_cyclic_table(get_syndrome, polynom):
    matrix = build_syndrome_cyclic_matrix(get_syndrome, polynom)

    pretty_table = PrettyTable()
    pretty_table.field_names = ["№ Ошибки", "Синдром"]
    pretty_table.align = "l"

    for i in range(len(matrix)):
        pretty_table.add_row([i, matrix[i]])

    return pretty_table.get_string()
