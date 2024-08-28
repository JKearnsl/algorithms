from src.models import BaseModel
from src.views.test import TestView


class TestController:

    def __init__(self, model: BaseModel, widgets_factory: 'WidgetsFactory', parent):
        self.model = model
        self.widgets_factory = widgets_factory
        self.view = TestView(self, self.model, widgets_factory, parent)

        self.view.show()
        self.view.model_loaded()

