from src.config import InIConfig
from src.models.sort import BaseSortModel
from src.models.sort import MenuItem


class ExchangeSortModel(BaseSortModel):
    id: MenuItem = MenuItem.EXCHANGE
    title: str = 'Сортировка Обменом'
    complexity: str = 'O(n^2)'

    def __init__(self, config: InIConfig, theme):

        self.config = config
        self.theme = theme

        # список наблюдателей
        self._mObservers = []

    def sort(self) -> None:
        array = self.input_list.copy()

        # итерация по неотсортированным массивам
        for i in range(1, len(array)):

            # получаем значение элемента
            val = array[i]

            # записываем в hole индекс i
            hole = i

            # проходим по массиву в обратную сторону, пока не найдём элемент больше текущего
            while hole > 0 and array[hole - 1] > val:
                # переставляем элементы местами, чтобы получить правильную позицию
                array[hole] = array[hole - 1]

                # делаем шаг назад
                hole -= 1

            # вставляем значение на верную позицию
            array[hole] = val

        self.output_list = array
