from src.models.result import ResultModel
from src.views.result import ResultView


class ResultController:

    def __init__(self, model: ResultModel, widgets_factory: 'WidgetsFactory', parent):
        self.model = model
        self.widgets_factory = widgets_factory
        self.view = ResultView(self, self.model, widgets_factory, parent)

        self.view.show()
        self.view.model_loaded()

    def calculate(self):
        self.model.calculate()
