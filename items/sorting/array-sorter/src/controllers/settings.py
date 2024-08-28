import os
import sys

from src.views.settings import SettingsView


class SettingsController:

    def __init__(self, model: 'SettingsModel', widgets_factory, parent):
        self.model = model
        self.view = SettingsView(self, self.model, widgets_factory, parent)

        self.view.show()
        self.view.model_loaded()

    def change_theme(self, theme_name):
        self.model.change_theme(theme_name)

    def reboot(self):
        os.execl(sys.executable, sys.executable, *sys.argv)
