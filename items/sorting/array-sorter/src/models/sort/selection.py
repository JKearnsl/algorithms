from src.config import InIConfig
from src.models.sort import BaseSortModel
from src.models.sort import MenuItem


class SelectionSortModel(BaseSortModel):
    id: MenuItem = MenuItem.SELECT
    title: str = 'Сортировка Выбором'
    complexity: str = 'O(n^2)'

    def __init__(self, config: InIConfig, theme):

        self.config = config
        self.theme = theme

        self._list = []

        # список наблюдателей
        self._mObservers = []

    def sort(self) -> None:
        array = self.input_list.copy()

        for i in range(0, len(array) - 1):
            smallest = i
            for j in range(i + 1, len(array)):
                if array[j] < array[smallest]:
                    smallest = j
            array[i], array[smallest] = array[smallest], array[i]

        self.output_list = array
