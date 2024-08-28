from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QWidget
from apscheduler.schedulers.qt import QtScheduler

from src.models.sort import MenuItem
from src.utils.observer import DObserver
from src.utils.ts_meta import TSMeta
from src.views.main.static_ui import UiMainWindow
from src.models.main import MainModel
from src.views.widgets import WidgetsFactory


class MainView(QWidget, DObserver, metaclass=TSMeta):

    def __init__(self, controller, model: MainModel, widgets_factory: WidgetsFactory, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.model = model
        self.widgets_factory = widgets_factory

        self.ui = UiMainWindow()
        self.ui.setup_ui(
            self,
            theme_class=model.theme[0],
            widgets_factory=widgets_factory,
            version=self.model.config.VAR.VERSION,
            app_name=self.model.config.VAR.BASE.APP_NAME,
            debug=self.model.config.VAR.BASE.DEBUG
        )

        self.scheduler = QtScheduler()
        self.scheduler.add_job(self.memory_usage_tick, 'interval', seconds=2)
        self.scheduler.start()

        # Регистрация представлений
        self.model.add_observer(self)

        # События
        self.ui.menu_select_model.currentChanged.connect(self.menu_select_changed)
        self.ui.menu_settings_button.clicked.connect(self.menu_settings_button_clicked)
        self.ui.settings_item.triggered.connect(self.controller.show_settings)
        self.ui.about_item.triggered.connect(self.about_dialog)

    def model_changed(self):
        pass

    def memory_usage_tick(self):
        self.ui.memory_usage_label.setText(f"ОЗУ: {self.model.get_ram_usage()} МБ")

    def model_loaded(self):
        self.ui.menu_list_widget.setCurrentIndex(self.ui.menu_list_widget.model().index(0, 0))

    def menu_select_changed(self, *args):
        index = self.ui.menu_list_widget.currentIndex().row()
        item = self.ui.menu_list_widget.model().item(index)

        if self.ui.content_layout.count() > 0:
            self.ui.content_layout.setCurrentIndex(0)
            current_widget = self.ui.content_layout.currentWidget()
            if current_widget.id == item.id:
                return

            # Кэш
            for i in range(self.ui.content_layout.count()):
                widget = self.ui.content_layout.widget(i)
                if widget.id == item.id:
                    self.ui.content_layout.setCurrentWidget(widget)
                    return

        if item.id == MenuItem.TEST:
            self.controller.show_test()
        else:
            self.controller.show_sort(item.id)

    def about_dialog(self):
        modal = self.widgets_factory.modal(self)
        modal.setWindowTitle("О программе")
        modal.setFixedSize(300, 200)

        modal.setObjectName("modal")

        modal_layout = modal.layout()
        modal_layout.setContentsMargins(0, 0, 0, 0)
        modal_layout.setSpacing(0)

        customize_sheet = QtWidgets.QWidget(modal)
        customize_sheet.setObjectName("customize_sheet")
        modal_layout.addWidget(customize_sheet)

        central_layout = QtWidgets.QHBoxLayout(customize_sheet)
        central_layout.setContentsMargins(20, 20, 20, 20)
        central_layout.setSpacing(20)
        central_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignTop)

        # Logo
        logo_layout = QtWidgets.QVBoxLayout()
        logo_layout.setContentsMargins(0, 5, 0, 0)
        logo_layout.setSpacing(10)

        logo = QtWidgets.QLabel()
        logo.setObjectName("logo")
        logo.setPixmap(self.windowIcon().pixmap(QtCore.QSize(64, 64)))
        logo.setScaledContents(True)
        logo.setFixedSize(QtCore.QSize(32, 32))
        logo_layout.addWidget(logo)

        logo_layout.addStretch(1)
        central_layout.addLayout(logo_layout)

        # Text
        text_widget = self.widgets_factory.label(parent=modal)
        text_widget.setObjectName("text_widget")
        text_widget.setTextFormat(QtCore.Qt.TextFormat.MarkdownText)
        text_widget.setOpenExternalLinks(True)
        text_widget.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        text_widget.setWordWrap(True)
        text_widget.setText(
            f"### {self.model.config.VAR.BASE.APP_NAME} | {self.model.config.VAR.VERSION}\n\n"
            "Программа разработана в рамках лабораторной работы\n\n\n"
            "Разработчик: "
            f"<a href='{self.model.config.VAR.BASE.CONTACT.URL}'>{self.model.config.VAR.BASE.CONTACT.NAME}</a> 2023"
        )
        central_layout.addWidget(text_widget)
        modal.exec()

    def menu_settings_button_clicked(self):
        point = self.ui.menu_settings_button.rect().topLeft()
        point.setY(point.y() - (self.ui.context_menu.height() + self.ui.menu_settings_button.height()))
        self.ui.context_menu.exec(self.ui.menu_settings_button.mapToGlobal(point))
