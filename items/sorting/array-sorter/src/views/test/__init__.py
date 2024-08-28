import random
import time
from typing import TypeVar

from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from apscheduler.schedulers.qt import QtScheduler

from src.models import BaseModel
from src.utils.observer import DObserver
from src.models.sort import MenuItem
from src.utils.ts_meta import TSMeta
from src.views.test.static_ui import UiTest

# Models
from src.models.sort.exchange import ExchangeSortModel
from src.models.sort.fast import FastSortModel
from src.models.sort.heap import HeapSortModel
from src.models.sort.insertion import InsertionSortModel
from src.models.sort.merge import MergeSortModel
from src.models.sort.selection import SelectionSortModel
from src.models.sort.shell import ShellSortModel
from src.models.sort.tree import TreeSortModel

ViewWidget = TypeVar('ViewWidget', bound=QWidget)
MenuItemModel = TypeVar('MenuItemModel', bound=BaseModel)


class TestView(QWidget, DObserver, metaclass=TSMeta):
    id: MenuItem

    def __init__(self, controller, model: MenuItemModel, widgets_factory, parent: ViewWidget):
        super().__init__(parent)
        self.id = model.id
        self.controller = controller
        self.model = model
        self.widgets_factory = widgets_factory

        parent.ui.content_layout.addWidget(self)
        parent.ui.content_layout.setCurrentWidget(self)

        self.ui = UiTest()
        self.ui.setup_ui(self, self.model.theme[0], widgets_factory)

        self.scheduler = QtScheduler()
        self.scheduler.start()
        self.ui.test_header.setText(self.model.title)

        # Регистрация представлений
        self.model.add_observer(self)

        # События
        self.ui.start_button.clicked.connect(self.start_button_clicked)

    def model_changed(self):
        pass

    def model_loaded(self):
        self.model_changed()

    def start_button_clicked(self):
        # todo: Утечка памяти
        self.scheduler.add_job(
            self.run_test,
            trigger='date',
            run_date=None,
        )

    def run_test(self):
        self.ui.table.clearContents()
        self.ui.process_label.clear()
        self.ui.start_button.setDisabled(True)
        self.ui.start_button.setText("Загрузка...")
        self.ui.process_label.setVisible(True)

        # Testing
        per_item = 2 ** 32
        els = [5000, 10000, 100000, 150000]
        samples = {
            count: {
                "unsorted": [random.randint(-per_item // 2, per_item // 2) for _ in range(count)],
                "sorted": []
            } for count in els
        }

        for sample in samples.values():
            sample["sorted"] = sorted(sample["unsorted"])

        models = [
            ExchangeSortModel,
            FastSortModel,
            HeapSortModel,
            InsertionSortModel,
            MergeSortModel,
            SelectionSortModel,
            ShellSortModel,
            TreeSortModel
        ]

        self.ui.table.setRowCount(len(models) * len(els))

        index = 0
        for model in models:
            self.ui.process_label.setText(f"{model.id.value} [{models.index(model) + 1}/{len(models)}]")
            for count, sample in samples.items():
                _ = model(config=self.model.config, theme=self.model.theme)

                title = QTableWidgetItem(_.id.value)
                title.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.ui.table.setItem(index, 0, title)

                working_time = QTableWidgetItem("...")
                working_time.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.ui.table.setItem(index, 1, working_time)

                length = QTableWidgetItem(str(count))
                length.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.ui.table.setItem(index, 2, length)

                valid = QTableWidgetItem("...")
                valid.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.ui.table.setItem(index, 3, valid)

                start_time = time.time()
                _.input_list = sample["unsorted"]
                end_time = time.time()

                working_time.setText(f"{end_time - start_time:.5f}")
                valid.setText(str(_.output_list == sample["sorted"]))
                index += 1

        self.ui.start_button.setText("Начать")
        self.ui.start_button.setDisabled(False)
        self.ui.process_label.setVisible(False)
