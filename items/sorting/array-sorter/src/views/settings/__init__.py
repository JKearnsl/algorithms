from typing import TypeVar

from PyQt6.QtWidgets import QWidget

from src.models.settings import SettingsModel
from src.utils.observer import DObserver
from src.utils.ts_meta import TSMeta
from src.views.settings.static_ui import UiSettings
from src.views.widgets import Dialog

ViewWidget = TypeVar('ViewWidget', bound=QWidget)


class SettingsView(Dialog, DObserver, metaclass=TSMeta):

    def __init__(self, controller, model: SettingsModel, widgets_factory, parent: ViewWidget):
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

        self.ui = UiSettings()
        self.ui.setup_ui(self, self.model.theme[0], widgets_factory)

        # Регистрация представлений
        self.model.add_observer(self)

        # События
        self.ui.ch_color_theme_widget.currentIndexChanged.connect(self.change_theme)

    def model_changed(self):
        # Themes
        self.ui.ch_color_theme_widget.blockSignals(True)
        self.ui.ch_color_theme_widget.clear()
        current_theme_index = 0
        for theme_name, theme in self.model.get_themes().items():
            self.ui.ch_color_theme_widget.addItem(theme_name, theme)
            if theme_name == self.model.theme[0].__title__:
                current_theme_index = self.ui.ch_color_theme_widget.count() - 1
        self.ui.ch_color_theme_widget.setCurrentIndex(current_theme_index)
        self.ui.ch_color_theme_widget.blockSignals(False)

    def model_loaded(self):
        self.model_changed()

    def change_theme(self, index):
        old_theme = self.model.theme[0]
        new_theme = self.ui.ch_color_theme_widget.itemData(index)
        result = self.ui.ch_color_theme_dialog.exec()
        if result == 0:
            self.ui.ch_color_theme_widget.blockSignals(True)
            self.ui.ch_color_theme_widget.setCurrentText(old_theme.__title__)
            self.ui.ch_color_theme_widget.blockSignals(False)
            return

        self.controller.change_theme(new_theme[0].__title__)
        self.controller.reboot()
