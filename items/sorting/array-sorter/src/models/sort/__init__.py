import random
from abc import abstractmethod
from enum import Enum


from src.models import BaseModel


class InputType(int, Enum):
    INT32 = 2 ** 32
    INT64 = 2 ** 64


class MenuItem(str, Enum):
    # Sort
    EXCHANGE: str = "exchange"
    FAST: str = "fast"
    HEAP: str = "heap"
    INSERTION: str = "insertion"
    MERGE: str = "merge"
    SELECT: str = "select"
    SHELL: str = "shell"
    TREE: str = "tree"

    # Test
    TEST: str = "test"


class BaseSortModel(BaseModel):
    id: MenuItem
    title: str
    complexity: str

    _length: int = 10
    _input_type: InputType = InputType.INT32
    _input_list: list = []
    _output_list: list = []

    def gen_list(self) -> None:
        value = self._input_type.value // 2
        self._input_list = list([random.randint(-value, value) for _ in range(self._length)])
        self.notify_observers()
        self.sort()

    @property
    def length(self) -> int:
        return self._length

    @length.setter
    def length(self, value: int) -> None:
        self._length = value
        self.notify_observers()

    @property
    def input_type(self) -> int:
        return self._input_type

    @input_type.setter
    def input_type(self, value: InputType) -> None:
        self._input_type = value
        self.notify_observers()

    @property
    def output_list(self) -> list:
        return self._output_list

    @output_list.setter
    def output_list(self, value: list[int]) -> None:
        self._output_list = value
        self.notify_observers()

    @property
    def input_list(self) -> list:
        return self._input_list

    @input_list.setter
    def input_list(self, value: list[int]) -> None:
        self._input_list = value
        self._length = len(value)
        self.sort()

    @abstractmethod
    def sort(self) -> None:
        pass
