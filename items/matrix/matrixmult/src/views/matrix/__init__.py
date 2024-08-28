from typing import TypeVar

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget

from src.models.matrix import MatrixModel
from src.utils.observer import DObserver
from src.utils.ts_meta import TSMeta
from src.views.matrix.static_ui import UiMatrix
from src.views.widgets import Dialog

ViewWidget = TypeVar('ViewWidget', bound=QWidget)


class MatrixView(Dialog, DObserver, metaclass=TSMeta):

    def __init__(self, controller, model: MatrixModel, widgets_factory, parent: ViewWidget):
        theme_class = model.theme[0]
        super().__init__(
            third_background=theme_class.third_background,
            second_background=theme_class.second_background,
            hover=theme_class.hover,
            text_header=theme_class.text_header,
            parent=parent
        )
        self.controller = controller
        self.model = model
        self.widgets_factory = widgets_factory

        self.ui = UiMatrix()
        self.ui.setup_ui(self, self.model.theme[0], widgets_factory)

        self.ui.matrix.setModel(QStandardItemModel(1, 1))

        self.ui.rows_count_value.setMinimum(1)
        self.ui.rows_count_value.setMaximum(999)
        self.ui.columns_count_value.setMinimum(1)
        self.ui.columns_count_value.setMaximum(999)

        # Регистрация представлений
        self.model.add_observer(self)

        # События
        self.ui.matrix.model().itemChanged.connect(self.item_changed)
        self.ui.rows_count_value.valueChanged.connect(self.rows_changed)
        self.ui.columns_count_value.valueChanged.connect(self.columns_changed)
        self.ui.randomize_button.clicked.connect(self.controller.randomize)
        self.finished.connect(self.controller.close_matrix_modal)

    def model_changed(self):
        self.ui.rows_count_value.blockSignals(True)
        self.ui.columns_count_value.blockSignals(True)
        self.ui.rows_count_value.setValue(self.model.rows)
        self.ui.columns_count_value.setValue(self.model.columns)
        self.ui.rows_count_value.blockSignals(False)
        self.ui.columns_count_value.blockSignals(False)

        self.ui.matrix.model().setRowCount(self.model.rows)
        self.ui.matrix.model().setColumnCount(self.model.columns)

        for i in range(self.model.rows):
            for j in range(self.model.columns):
                self.ui.matrix.model().blockSignals(True)
                value = self.model.data[i][j]
                item = QStandardItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ui.matrix.model().setItem(i, j, item)
                self.ui.matrix.model().blockSignals(False)

        if self.model.is_locked_rows:
            self.ui.rows_count_value.setEnabled(False)

        if self.model.is_locked_cols:
            self.ui.columns_count_value.setEnabled(False)

    def model_loaded(self):
        self.model_changed()

    def rows_changed(self):
        self.controller.set_rows(self.ui.rows_count_value.value())

    def columns_changed(self):
        self.controller.set_columns(self.ui.columns_count_value.value())

    def item_changed(self, event: QStandardItem):
        item = event.index()
        row_index = item.row()
        column_index = item.column()
        value = event.text()
        if not value.replace("-", "").isdigit():
            value = 0
        else:
            value = float(value)
        self.controller.change_value(row_index, column_index, value)
