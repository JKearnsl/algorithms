import random

from src.config import InIConfig
from src.models import BaseModel


class MatrixModel(BaseModel):
    id: int
    title: str
    data: list[list[float]]
    is_locked_rows: bool
    is_locked_cols: bool

    def __init__(self, config: InIConfig, theme, id: int, title: str):
        self.config = config
        self.theme = theme

        self.id = id
        self.title = title
        self.data = [[0]]
        self.is_locked_rows = False
        self.is_locked_cols = False

        # список наблюдателей
        self._mObservers = []

    @property
    def rows(self) -> int:
        return len(self.data)

    @property
    def columns(self) -> int:
        return len(self.data[0])

    @rows.setter
    def rows(self, count: int) -> None:
        if (count == self.rows) or (count <= 0):
            return

        if count > self.rows:
            empty_row = [0 for _ in range(self.columns)]
            for i in range(count - self.rows):
                self.data.append(empty_row.copy())
        elif count < self.rows:
            self.data = self.data[:count]

        self.notify_observers()

    @columns.setter
    def columns(self, count: int) -> None:
        if (count == self.columns) or (count <= 0):
            return

        delta = count - self.columns
        if count > self.columns:
            empty_delta_row = [0 for _ in range(delta)]
            for i in range(self.rows):
                self.data[i].extend(empty_delta_row.copy())
        elif count < self.columns:
            local_delta = self.columns + delta
            for i in range(self.rows):
                self.data[i] = self.data[i][:local_delta]

        self.notify_observers()

    def change_value(self, row_index: int, column_index: int, value: float):
        self.data[row_index][column_index] = value
        self.notify_observers()

    def randomize(self):
        for i in range(self.rows):
            for j in range(self.columns):
                random_value = random.randint(-999, 999)
                if random_value != 0:
                    random_value = random_value / 2
                self.data[i][j] = random_value
        self.notify_observers()

    def lock_rows(self):
        self.is_locked_rows = True
        self.notify_observers()

    def lock_columns(self):
        self.is_locked_cols = True
        self.notify_observers()

    @classmethod
    def multiply(cls, a: 'MatrixModel', b: 'MatrixModel') -> 'MatrixModel':
        m = len(a.data)  # a: m × n
        n = len(b.data)  # b: n × k
        k = len(b.data[0])

        c = [[None for __ in range(k)] for __ in range(m)]  # c: m × k

        for i in range(m):
            for j in range(k):
                c[i][j] = sum(a.data[i][kk] * b.data[kk][j] for kk in range(n))

        result = MatrixModel(a.config, a.theme, 0, "A * B")
        result.data = c
        return result
