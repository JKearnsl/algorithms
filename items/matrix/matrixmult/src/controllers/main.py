from src.controllers.matrix import MatrixController
from src.controllers.result import ResultController
from src.controllers.settings import SettingsController
from src.models.main import MainModel
from src.models.matrix import MatrixModel
from src.models.result import ResultModel
from src.models.settings import SettingsModel
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

    def new_matrix(self):
        self.model.new_matrix()

    def matrix_count(self) -> int:
        return self.model.matrix_count()

    def show_matrix_modal(self, matrix_id: int):
        controller = MatrixController(
            self.model.matrix[matrix_id], self.widgets_factory, self.view
        )
        self.model.notify_observers()

    def show_result_page(self):
        controller = ResultController(
            ResultModel(self.model.config, self.model.theme, self.model.matrix), self.widgets_factory, self.view
        )
        self.model.add_observer(controller.view)
