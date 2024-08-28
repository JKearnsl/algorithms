import os

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from src.view.mfp_main import MFPMainView


class MFPMainController:

    def __init__(self, model: 'MFPModel'):
        self.model = model
        self.view = MFPMainView(self, self.model)

        self.view.show()

    def alg_changed(self):
        self.model.alg = self.view.ui.algInput.currentData(Qt.ItemDataRole.UserRole)

    def source_changed(self):
        self.model.source = self.view.ui.sourceInput.text()

    def target_changed(self):
        self.model.target = self.view.ui.targetInput.text()

    def graph_type_changed(self):
        self.model.graph_type = self.view.ui.graphType.currentData(Qt.ItemDataRole.UserRole)

    def show_as_changed(self):
        self.model.show_graph_as = self.view.ui.showAsBox.currentData(Qt.ItemDataRole.UserRole)

    def update_graph_link(self, data):
        index, _from, _to, _weight = data
        self.model.edit_link(index, _from, _to, _weight)

    def update_graph_clicked(self):
        self.model.notify_observers()

    def add_link_clicked(self):
        self.model.add_link(0, 0, 0)

    def remove_link_clicked(self):
        self.model.remove_link()

    def open_file(self):
        open_file_name = QtWidgets.QFileDialog.getOpenFileName(
            self.view,
            'Открыть файл',
            os.path.expanduser("~"),
            'Graph files (*.gph);;All files (*.*)'
        )[0]
        if not open_file_name:
            return

        result = self.model.load_file(open_file_name)
        if not result:
            self.view.show_error(f'Ошибка при чтении файла {open_file_name!r}')

    def save_file(self):
        save_file_name = QtWidgets.QFileDialog.getSaveFileName(
            self.view,
            'Сохранить файл',
            os.path.expanduser("~"),
            'Graph files (*.gph);;All files (*.*)'
        )[0]
        if not save_file_name:
            return

        result, msg = self.model.save_file(save_file_name)
        if not result:
            self.view.show_error(f'Ошибка при сохранении файла {save_file_name!r}:\n{msg}')
        else:
            self.view.show_info(f'Файл {save_file_name!r} успешно сохранен', 'Успех')

    def about(self):
        self.view.about()
