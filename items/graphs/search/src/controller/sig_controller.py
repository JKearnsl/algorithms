from PyQt6.QtCore import Qt

from src.view import SIGView


class SIGController:
    """
    Класс SIGController представляет реализацию контроллера.
    Согласовывает работу представления с моделью.
    """

    def __init__(self, model):
        self.model = model
        self.view = SIGView(self, self.model)

        self.view.show()

    def input_problem_type(self):
        _ = self.view.ui.problemType.currentData(Qt.ItemDataRole.UserRole)
        self.model.problem_type = _

    def input_graph_type(self):
        _ = self.view.ui.graphType.currentData(Qt.ItemDataRole.UserRole)
        self.model.graph_type = _

    def input_search_value(self):
        value = self.view.ui.searchValue.text()
        self.model.search_value = value

    def input_start_vertex(self):
        value = self.view.ui.startVertex.text()
        self.model.start_vertex = value

    def add_link(self):
        self.model.add_link('0', '0')

    def remove_link(self):
        self.model.remove_link()

    def graph_data_changed(self, data):
        index, _from, _to = data
        data = self.model.graph_links
        data[index] = (_from, _to)
        self.model.graph_links = data

    def update_graph_canvas(self):
        self.model.notify_observers()

    def input_show_as(self):
        _ = self.view.ui.showAs.currentData(Qt.ItemDataRole.UserRole)
        self.model.show_as = _
