from PyQt6.QtCore import Qt

from src.view import FSPView


class FSPController:
    """
    Класс FSPController представляет реализацию контроллера.
    Согласовывает работу представления с моделью.
    """

    def __init__(self, model):
        self.model = model
        self.view = FSPView(self, self.model)

        self.view.show()

    def input_alg_type(self):
        _ = self.view.ui.algType.currentData(Qt.ItemDataRole.UserRole)
        self.model.algorithm_type = _

    def input_view_graph_as(self):
        _ = self.view.ui.viewGraphAs.currentData(Qt.ItemDataRole.UserRole)
        self.model.show_graph_as = _

    def input_search_vertex(self):
        value = self.view.ui.searchValue.text()
        self.model.search_vertex = value

    def input_start_vertex(self):
        value = self.view.ui.startValue.text()
        self.model.start_vertex = value

    def add_link(self):
        self.model.add_link('0', '0', 0)

    def remove_link(self):
        self.model.remove_link()

    def graph_data_changed(self, data):
        index, _from, _to, _weight = data
        data = self.model.graph
        data[index] = dict(from_node=_from, to_node=_to, weight=_weight)
        self.model.graph = data

    def update_graph_canvas(self):
        self.model.notify_observers()
