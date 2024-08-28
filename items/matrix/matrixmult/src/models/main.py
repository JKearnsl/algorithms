from src.config import InIConfig
from src.models import BaseModel
from src.models.matrix import MatrixModel


class MainModel(BaseModel):

    def __init__(self, config: InIConfig, theme: tuple[type[any], str, str]):
        self.config = config
        self.theme = theme

        self.matrix: list[MatrixModel] = []

        # список наблюдателей
        self._mObservers = []

    def new_matrix(self) -> None:
        new_id = len(self.matrix)
        matrix = MatrixModel(self.config, self.theme, id=new_id, title=f"Матрица #{new_id}")

        if len(self.matrix) > 0:
            matrix.rows = self.matrix[-1].columns
            matrix.is_locked_rows = True
            self.matrix[-1].is_locked_cols = True

        self.matrix.append(matrix)
        self.notify_observers()

    def matrix_count(self) -> int:
        return len(self.matrix)
