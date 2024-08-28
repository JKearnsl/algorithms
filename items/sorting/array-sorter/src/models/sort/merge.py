import operator

from src.config import InIConfig
from src.models.sort import BaseSortModel
from src.models.sort import MenuItem


class MergeSortModel(BaseSortModel):
    id: MenuItem = MenuItem.MERGE
    title: str = 'Сортировка Слиянием'
    complexity: str = 'O(nlog(n))'

    def __init__(self, config: InIConfig, theme):
        self.config = config
        self.theme = theme

        # список наблюдателей
        self._mObservers = []

    def sort(self) -> None:
        array = self.input_list.copy()
        self.output_list = merge_sort(array)


def merge_sort(array, compare=operator.lt):
    if len(array) < 2:
        return array[:]
    else:
        middle = int(len(array) / 2)
        left = merge_sort(array[:middle], compare)
        right = merge_sort(array[middle:], compare)
        return merge(left, right, compare)


def merge(left, right, compare):
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if compare(left[i], right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    return result
