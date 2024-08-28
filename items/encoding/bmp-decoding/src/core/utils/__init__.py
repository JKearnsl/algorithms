import itertools

from .kaitaibmp import Bmp


def align_to_four_bytes(length: int) -> int:
    remainder = length % 4
    if remainder == 0:
        return length
    else:
        return length - (4 - remainder)


def partition(l, size):
    for i in range(0, len(l), size):
        yield list(itertools.islice(l, i, i + size))
