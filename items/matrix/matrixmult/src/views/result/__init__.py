from typing import TypeVar

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from src.utils.observer import DObserver
from src.utils.ts_meta import TSMeta
from src.views.result.static_ui import UiResult
from src.models.result import ResultModel
from src.views.widgets import WidgetsFactory

ViewWidget = TypeVar('ViewWidget', bound=QWidget)


class ResultView(QWidget, DObserver, metaclass=TSMeta):

    def __init__(self, controller, model: ResultModel, widgets_factory: WidgetsFactory, parent: ViewWidget):
        super().__init__(parent)
        self.controller = controller
        self.model = model
        self.widgets_factory = widgets_factory

        parent.ui.content_layout.addWidget(self)

        self.ui = UiResult()
        self.ui.setup_ui(self, self.model.theme[0], widgets_factory)
        self.ui.matrix.setModel(QStandardItemModel(0, 0))

        # Регистрация представлений
        self.model.add_observer(self)

        # События
        self.ui.show_steps_button.clicked.connect(self.show_steps)
        self.ui.calculate_button.clicked.connect(self.controller.calculate)

    def model_changed(self):
        self.ui.imo_count_value.setText(str(len(self.model.matrix_list)))
        self.ui.csm_count_value.setText(str(self.model.mult_count()))

        if self.model.result_matrix:
            self.ui.matrix.model().setRowCount(self.model.result_matrix.rows)
            self.ui.matrix.model().setColumnCount(self.model.result_matrix.columns)

            for i in range(self.model.result_matrix.rows):
                for j in range(self.model.result_matrix.columns):
                    self.ui.matrix.model().blockSignals(True)
                    value = self.model.result_matrix.data[i][j]
                    item = QStandardItem(str(value))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.ui.matrix.model().setItem(i, j, item)
                    self.ui.matrix.model().blockSignals(False)

    def model_loaded(self):
        self.model_changed()

    def show_steps(self):
        modal = self.widgets_factory.modal(self)
        modal.setFixedSize(400, 300)
        modal.setWindowTitle("Шаги умножения")

        layout = modal.layout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        customize_sheet = QWidget(modal)
        layout.addWidget(customize_sheet)

        central_layout = QVBoxLayout(customize_sheet)
        central_layout.setContentsMargins(20, 20, 20, 20)
        central_layout.setSpacing(20)
        central_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignTop)

        text = self.widgets_factory.textarea(modal)
        text.setPlainText(self.model.steps)
        text.setReadOnly(True)
        central_layout.addWidget(text)

        modal.exec()
