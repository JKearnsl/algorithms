import random

from src.config import InIConfig
from src.models.sort import BaseSortModel
from src.models.sort import MenuItem


class FastSortModel(BaseSortModel):
    id: MenuItem = MenuItem.FAST
    title: str = 'Быстрая Сортировка (Хоара)'
    complexity: str = 'O(nlog(n))'

    def __init__(self, config: InIConfig, theme):

        self.config = config
        self.theme = theme

        # список наблюдателей
        self._mObservers = []

    def sort(self) -> None:
        array = self.input_list.copy()
        self.output_list = quicksort(array)


def quicksort(array: list[int]):
    if len(array) <= 1:
        return array
    else:
        q = random.choice(array)
    l_array = [n for n in array if n < q]

    e_array = [q] * array.count(q)
    b_array = [n for n in array if n > q]
    return quicksort(l_array) + e_array + quicksort(b_array)
