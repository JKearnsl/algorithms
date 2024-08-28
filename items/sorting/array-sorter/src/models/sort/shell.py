import math

from src.config import InIConfig
from src.models.sort import BaseSortModel
from src.models.sort import MenuItem


class ShellSortModel(BaseSortModel):
    id: MenuItem = MenuItem.SHELL
    title: str = 'Сортировка Шелла'
    complexity: str = 'O(n^2)'

    def __init__(self, config: InIConfig, theme):

        self.config = config
        self.theme = theme

        # список наблюдателей
        self._mObservers = []

    def sort(self) -> None:
        array = self.input_list.copy()

        n = len(array)
        k = int(math.log2(n))
        interval = 2 ** k - 1
        while interval > 0:
            for i in range(interval, n):
                temp = array[i]
                j = i
                while j >= interval and array[j - interval] > temp:
                    array[j] = array[j - interval]
                    j -= interval
                array[j] = temp
            k -= 1
            interval = 2 ** k - 1

        self.output_list = array
