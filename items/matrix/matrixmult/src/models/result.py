from functools import cache

from src.config import InIConfig
from src.models import BaseModel
from src.models.matrix import MatrixModel


class ResultModel(BaseModel):

    def __init__(self, config: InIConfig, theme: tuple[type[any], str, str], matrix_list: list[MatrixModel]):
        self.config = config
        self.theme = theme
        self.matrix_list = matrix_list
        self.steps = ""
        self.raw_steps = None
        self.result_matrix = None

        # список наблюдателей
        self._mObservers = []

    def count_of_matrix(self):
        return len(self.matrix_list)

    def mult_count(self) -> int:
        matrix_list_len = len(self.matrix_list)
        if matrix_list_len == 1:
            self.steps = "A"
            return 0
        elif matrix_list_len == 0:
            self.steps = ""
            return 0

        matrix_dims = []
        for i in range(matrix_list_len):
            matrix_dims.append(self.matrix_list[i].rows)
            if i == matrix_list_len - 1:
                matrix_dims.append(self.matrix_list[i].columns)
                break

        @cache
        def a(i, j):
            if i == j:
                return 0, self.matrix_list[i].title, self.matrix_list[i]
            min_count = float('inf')
            min_steps = ""
            raw_steps = None
            for k in range(i, j):
                count1, steps1, raw_step1 = a(i, k)
                count2, steps2, raw_step2 = a(k + 1, j)

                total_count = count1 + count2 + matrix_dims[i] * matrix_dims[k + 1] * matrix_dims[j + 1]
                if total_count < min_count:
                    min_count = total_count
                    min_steps = f"({steps1} x {steps2})"
                    raw_steps = (raw_step1, raw_step2)
            return min_count, min_steps, raw_steps

        min_count, steps, raw_steps = a(0, len(matrix_dims) - 2)
        self.steps = steps
        self.raw_steps = raw_steps
        return min_count

    def calculate(self):
        if self.raw_steps is None:
            return

        def process_tuple(t):
            if isinstance(t, MatrixModel):
                return t
            elif isinstance(t, tuple):
                elems = tuple(process_tuple(item) for item in t)
                is_only_matrix = all(isinstance(item, MatrixModel) for item in elems)
                if is_only_matrix:
                    return MatrixModel.multiply(elems[0], elems[1])
                return elems

        self.result_matrix = process_tuple(self.raw_steps)

        self.notify_observers()
