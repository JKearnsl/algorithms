from src.controllers.settings import SettingsController
from src.controllers.sort import SortController
from src.controllers.test import TestController

from src.models.sort.exchange import ExchangeSortModel
from src.models.sort.fast import FastSortModel
from src.models.sort.heap import HeapSortModel
from src.models.sort.merge import MergeSortModel
from src.models.sort.selection import SelectionSortModel
from src.models.sort.shell import ShellSortModel
from src.models.sort.tree import TreeSortModel
from src.models.sort.insertion import InsertionSortModel

from src.models.settings import SettingsModel
from src.models.main import MainModel
from src.models.sort import MenuItem
from src.models.test import TestModel
from src.views.main import MainView


class MainController:

    def __init__(self, model: 'MainModel', widgets_factory: 'WidgetsFactory'):
        self.model = model
        self.widgets_factory = widgets_factory
        self.view = MainView(self, self.model, widgets_factory)

        self.view.show()
        self.view.model_loaded()

    def show_settings(self):
        controller = SettingsController(
            SettingsModel(self.model.config, self.model.theme), self.widgets_factory, self.view
        )

    def show_sort(self, sort_id):
        match sort_id:
            case MenuItem.SELECT:
                model = SelectionSortModel(self.model.config, self.model.theme)
            case MenuItem.INSERTION:
                model = InsertionSortModel(self.model.config, self.model.theme)
            case MenuItem.SHELL:
                model = ShellSortModel(self.model.config, self.model.theme)
            case MenuItem.TREE:
                model = TreeSortModel(self.model.config, self.model.theme)
            case MenuItem.FAST:
                model = FastSortModel(self.model.config, self.model.theme)
            case MenuItem.HEAP:
                model = HeapSortModel(self.model.config, self.model.theme)
            case MenuItem.MERGE:
                model = MergeSortModel(self.model.config, self.model.theme)
            case MenuItem.EXCHANGE:
                model = ExchangeSortModel(self.model.config, self.model.theme)
            case _:
                raise ValueError(f"Unknown sort type: {sort_id}")

        controller = SortController(model, self.widgets_factory, self.view)

    def show_test(self):
        controller = TestController(
            TestModel(self.model.config, self.model.theme),
            self.widgets_factory,
            self.view
        )