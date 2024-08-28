from src.models.sort import BaseSortModel
from src.views.sort import SortView


class SortController:

    def __init__(self, model: BaseSortModel, widgets_factory: 'WidgetsFactory', parent):
        self.model = model
        self.widgets_factory = widgets_factory
        self.view = SortView(self, self.model, widgets_factory, parent)

        self.view.show()
        self.view.model_loaded()

