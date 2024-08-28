from src.views.matrix import MatrixView


class MatrixController:

    def __init__(self, model: 'MatrixModel', widgets_factory, parent):
        self.model = model
        self.view = MatrixView(self, self.model, widgets_factory, parent)

        self.view.model_loaded()
        self.view.exec()

    def set_rows(self, count: int):
        self.model.rows = count

    def set_columns(self, count: int):
        self.model.columns = count

    def change_value(self, row_index: int, column_index: int, value: float):
        self.model.change_value(row_index, column_index, value)

    def randomize(self):
        self.model.randomize()

    def close_matrix_modal(self):
        self.model.remove_observer(self.view)
