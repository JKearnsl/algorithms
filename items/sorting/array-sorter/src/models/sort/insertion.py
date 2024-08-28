from src.config import InIConfig
from src.models.sort import BaseSortModel
from src.models.sort import MenuItem


class InsertionSortModel(BaseSortModel):
    id: MenuItem = MenuItem.INSERTION
    title: str = 'Сортировка Вставками'
    complexity: str = 'O(n^2)'

    def __init__(self, config: InIConfig, theme):

        self.config = config
        self.theme = theme

        # список наблюдателей
        self._mObservers = []

    def sort(self) -> None:
        array = self.input_list.copy()

        for i in range(1, len(array)):
            key = array[i]
            j = i - 1
            while j >= 0 and key < array[j]:
                array[j + 1] = array[j]
                j -= 1
            array[j + 1] = key

        self.output_list = array
