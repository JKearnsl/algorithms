from src.config import InIConfig
from src.models.sort import BaseSortModel
from src.models.sort import MenuItem


class HeapSortModel(BaseSortModel):
    id: MenuItem = MenuItem.HEAP
    title: str = 'Пирамидальная Сортировка'
    complexity: str = 'O(nlog(n))'

    def __init__(self, config: InIConfig, theme):

        self.config = config
        self.theme = theme

        # список наблюдателей
        self._mObservers = []

    def sort(self) -> None:
        array = self.input_list.copy()

        # Создаём Max Heap из списка
        # 2-й аргумент означает остановку алгоритма перед элементом -1, то есть
        # перед первым элементом списка
        # 3-й аргумент означает повторный проход по списку в обратном направлении,
        # уменьшая счётчик i на 1
        for i in range(len(array), -1, -1):
            heapify(array, len(array), i)

        # Перемещаем корень Max Heap в самый конец списка
        for i in range(len(array) - 1, 0, -1):
            array[i], array[0] = array[0], array[i]
            heapify(array, i, 0)

        self.output_list = array


def heapify(nums, heap_size, root_index):
    # Индекс наибольшего элемента считается корневым индексом
    largest = root_index
    left_child = (2 * root_index) + 1
    right_child = (2 * root_index) + 2

    # Если левый потомок корня — это допустимый индекс, а элемент больше,
    # чем текущий наибольший, то мы обновляем наибольший элемент
    if left_child < heap_size and nums[left_child] > nums[largest]:
        largest = left_child

    # То же самое и для правого потомка корня
    if right_child < heap_size and nums[right_child] > nums[largest]:
        largest = right_child

    # Если наибольший элемент уже не корневой, они меняются местами
    if largest != root_index:
        nums[root_index], nums[largest] = nums[largest], nums[root_index]
        heapify(nums, heap_size, largest)
