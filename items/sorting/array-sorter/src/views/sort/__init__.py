from typing import TypeVar

from PyQt6.QtWidgets import QWidget

from src.utils.observer import DObserver
from src.models.sort import MenuItem, InputType
from src.utils.ts_meta import TSMeta
from src.views.sort.static_ui import UiSort
from src.models.sort import BaseSortModel

ViewWidget = TypeVar('ViewWidget', bound=QWidget)


class SortView(QWidget, DObserver, metaclass=TSMeta):
    id: MenuItem

    def __init__(self, controller, model: BaseSortModel, widgets_factory, parent: ViewWidget):
        super().__init__(parent)
        self.id = model.id
        self.controller = controller
        self.model = model
        self.widgets_factory = widgets_factory

        parent.ui.content_layout.addWidget(self)
        parent.ui.content_layout.setCurrentWidget(self)

        self.ui = UiSort()
        self.ui.setup_ui(self, self.model.theme[0], widgets_factory)

        self.ui.sort_header.setText(self.model.title)
        self.ui.sort_complexity.setText(self.model.complexity)

        # Регистрация представлений
        self.model.add_observer(self)

        # События
        self.ui.input_widget.textChanged.connect(self.input_changed)
        self.ui.length_line_widget.textChanged.connect(self.length_changed)
        self.ui.input_type.currentIndexChanged.connect(self.input_type_changed)
        self.ui.generate_button.clicked.connect(self.generate_clicked)

    def model_changed(self):
        if self.model.input_list != self.ui.input_widget.array():
            self.ui.input_widget.blockSignals(True)
            self.ui.input_widget.set_array(self.model.input_list)
            self.ui.input_widget.blockSignals(False)

        self.ui.output_widget.setPlainText(", ".join(map(str, self.model.output_list)))

        self.ui.length_line_widget.blockSignals(True)
        self.ui.length_line_widget.setText(str(self.model.length))
        self.ui.length_line_widget.blockSignals(False)

        self.ui.input_type.blockSignals(True)
        self.ui.input_type.clear()
        current_theme_index = 0
        for input_type in InputType:
            self.ui.input_type.addItem(input_type.name, input_type)
            if input_type == self.model.input_type:
                current_theme_index = self.ui.input_type.count() - 1
        self.ui.input_type.setCurrentIndex(current_theme_index)
        self.ui.input_type.blockSignals(False)

    def input_changed(self):
        self.model.input_list = self.ui.input_widget.array()

    def length_changed(self):
        if self.ui.length_line_widget.text() != "":
            self.model.length = int(self.ui.length_line_widget.text())
        else:
            self.ui.length_line_widget.set_error()

    def input_type_changed(self):
        self.model.input_type = self.ui.input_type.currentData()

    def generate_clicked(self):
        self.model.gen_list()

    def model_loaded(self):
        self.model_changed()
