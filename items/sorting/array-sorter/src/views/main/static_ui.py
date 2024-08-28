from PyQt6 import QtCore, QtGui, QtWidgets

from src.models.sort import MenuItem
from src.views.widgets import WidgetsFactory, Label
from src.views.widgets.list import ListItemWidget


class UiMainWindow:
    def setup_ui(
            self, main_window: QtWidgets.QWidget,
            widgets_factory: WidgetsFactory,
            theme_class,
            version: str,
            app_name: str,
            debug: bool
    ):
        main_window.setObjectName("main_window")
        main_window.setWindowTitle(app_name)
        main_window.resize(830, 600)
        main_window.setStyleSheet("""
            QWidget#main_window {
                background-color: $BG1;
            }
            QToolTip {
                background: #D9DBDD;
                border: 1px solid #000000;
                border-radius: 3px;
                color: #000000;
            }
        """.replace("$BG1", theme_class.first_background))
        central_layout = QtWidgets.QHBoxLayout(main_window)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        # Menu widget
        menu_widget = QtWidgets.QWidget(main_window)
        menu_widget.setObjectName("menu_widget")
        menu_widget.setStyleSheet("""
            QWidget#menu_widget {
                background-color: $BG2;
                border-right: 1px solid $HOVER;
            }
        """.replace(
            "$BG2", theme_class.second_background
        ).replace(
            "$HOVER", theme_class.hover
        ))
        menu_widget.setFixedWidth(300)
        menu_layout = QtWidgets.QVBoxLayout(menu_widget)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.addWidget(menu_widget)

        # Menu header
        menu_header_widget = QtWidgets.QWidget()
        menu_header_widget.setObjectName("menu_header_widget")
        menu_header_widget.setToolTip(f"{app_name} {version}")

        menu_header_layout = QtWidgets.QHBoxLayout(menu_header_widget)
        menu_header_layout.setContentsMargins(0, 15, 0, 10)
        menu_header_layout.addItem(
            QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        )

        # Menu header logo widget
        menu_header_logo_widget = QtWidgets.QWidget()
        menu_header_logo_widget.setObjectName("menu_header_logo_widget")
        menu_header_logo_widget.setFixedHeight(50)

        menu_header_logo_layout = QtWidgets.QHBoxLayout(menu_header_logo_widget)
        menu_header_logo_layout.setContentsMargins(0, 0, 0, 0)
        menu_header_logo_layout.setSpacing(5)

        logo = QtWidgets.QLabel()
        logo.setObjectName("logo")
        logo.setPixmap(main_window.windowIcon().pixmap(QtCore.QSize(64, 64)))
        logo.setScaledContents(True)
        logo.setFixedSize(QtCore.QSize(32, 32))
        menu_header_logo_layout.addWidget(logo)

        program_title_layout = QtWidgets.QVBoxLayout()
        program_title_layout.setContentsMargins(4, 3, 0, 3)
        program_title_layout.setSpacing(0)

        program_name_widget = QtWidgets.QLabel()
        program_name_widget.setObjectName("program_name_widget")
        program_name_widget.setText(app_name)
        program_name_widget.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        program_name_widget.setStyleSheet("""
            QLabel#program_name_widget {
                font-size: 14px;
                font-weight: 800;
                color: $TEXT_HEADER;
            }
        """.replace(
            "$TEXT_HEADER", theme_class.text_header
        ))
        program_title_layout.addWidget(program_name_widget)

        program_version_widget = QtWidgets.QLabel()
        program_version_widget.setObjectName("program_version_widget")
        program_version_widget.setText(version)
        program_version_widget.setStyleSheet("""
            QLabel#program_version_widget {
                font-size: 12px;
                font-weight: bold;
                color: $TEXT_SECONDARY;
            }
        """.replace(
            "$TEXT_SECONDARY", theme_class.text_secondary
        ))
        program_title_layout.addWidget(program_version_widget)

        menu_header_logo_layout.addLayout(program_title_layout)

        menu_header_layout.addWidget(menu_header_logo_widget)

        menu_layout.addWidget(menu_header_widget)

        # Menu list
        menu_list_widget = widgets_factory.list()
        menu_list_widget.setObjectName("menu_list_widget")

        menu_list_model = menu_list_widget.model()

        self.menu_select_model = menu_list_widget.selectionModel()

        self.menu_item_insertion_sort = ListItemWidget("Menu item 1", MenuItem.INSERTION)
        self.menu_item_selection_sort = ListItemWidget("Menu item 2", MenuItem.SELECT)
        self.menu_item_exchange_sort = ListItemWidget("Menu item 3", MenuItem.EXCHANGE)
        self.menu_item_fast_sort = ListItemWidget("Menu item 4", MenuItem.FAST)
        self.menu_item_tree_sort = ListItemWidget("Menu item 5", MenuItem.TREE)
        self.menu_item_heap_sort = ListItemWidget("Menu item 6", MenuItem.HEAP)
        self.menu_item_shell_sort = ListItemWidget("Menu item 7", MenuItem.SHELL)
        self.menu_item_merge_sort = ListItemWidget("Menu item 8", MenuItem.MERGE)
        self.menu_item_test = ListItemWidget("Menu item 9", MenuItem.TEST)


        menu_list_model.appendRow(self.menu_item_insertion_sort)
        menu_list_model.appendRow(self.menu_item_selection_sort)
        menu_list_model.appendRow(self.menu_item_exchange_sort)
        menu_list_model.appendRow(self.menu_item_fast_sort)
        menu_list_model.appendRow(self.menu_item_tree_sort)
        menu_list_model.appendRow(self.menu_item_heap_sort)
        menu_list_model.appendRow(self.menu_item_shell_sort)
        menu_list_model.appendRow(self.menu_item_merge_sort)
        menu_list_model.appendRow(self.menu_item_test)

        menu_layout.addWidget(menu_list_widget)
        self.menu_list_widget = menu_list_widget

        # Tool section
        menu_tool_layout = QtWidgets.QHBoxLayout()
        menu_settings_button = QtWidgets.QToolButton()
        menu_settings_button.setObjectName("menu_settings_button")
        menu_settings_button.setIcon(QtGui.QIcon("icons:settings-64.png"))
        menu_settings_button.setIconSize(QtCore.QSize(16, 16))
        menu_settings_button.setStyleSheet("""
            QToolButton#menu_settings_button {
                border-radius: 3px;
                background-color: transparent;
            }
            QToolButton#menu_settings_button:hover {
                background-color: $HOVER;
            }
            QToolButton#menu_settings_button:pressed {
                background-color: transparent;
            }
        """.replace(
            "$HOVER", theme_class.hover
        ))
        self.menu_settings_button = menu_settings_button

        memory_usage_label = Label(theme_class.text_secondary)
        memory_usage_label.setObjectName("memory_usage_label")
        memory_usage_label.add_style("""
            QLabel#memory_usage_label {
                font-size: 12px;
                font-weight: bold;
                }
        """)
        self.memory_usage_label = memory_usage_label

        # Context menu
        context_menu = QtWidgets.QMenu(main_window)
        context_menu.setObjectName("context_menu")
        context_menu.setStyleSheet("""
            QMenuBar {
                background-color: transparent;
            }

            QMenuBar::item {
                color : $PRIMARY_COLOR;
                margin-top:4px;
                spacing: 3px;
                padding: 1px 10px;
                background: transparent;
                border-radius: 4px;
            }


            QMenuBar::item:selected {
                background: $BG2;
            }

            QMenuBar::item:pressed {
                background: $SELECTED_COLOR;
                color: #FFFFFF;
            }

            QMenu {
                background-color: $BG3;
                border: 1px solid $HOVER_COLOR;
                border-top-right-radius: 5px;
                border-top-left-radius: 5px;
                border-bottom-right-radius: 5px;
            }
            QMenu::item {
                color: $PRIMARY_COLOR;
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: $HOVER_COLOR;
            } 
                """.replace(
            "$PRIMARY_COLOR", theme_class.text_primary
        ).replace(
            "$BG2", theme_class.second_background
        ).replace(
            "$SELECTED_COLOR", theme_class.selection
        ).replace(
            "$BG3", theme_class.third_background
        ).replace(
            "$HOVER_COLOR", theme_class.hover
        ))
        self.settings_item = context_menu.addAction("Настойки")
        self.about_item = context_menu.addAction("О программе")
        self.context_menu = context_menu

        menu_tool_layout.addItem(
            QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        )
        menu_tool_layout.addWidget(menu_settings_button)
        menu_tool_layout.addItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        )
        menu_tool_layout.addWidget(memory_usage_label)
        menu_tool_layout.addItem(
            QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        )
        menu_layout.addLayout(menu_tool_layout)
        menu_layout.addItem(
            QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        )

        # Content layout
        content_layout = QtWidgets.QStackedLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setObjectName("content_widget")
        central_layout.addLayout(content_layout)
        self.content_layout = content_layout

        self.translate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def translate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        self.menu_item_insertion_sort.setText(_translate("menu_item_insertion_sort", "Вставками"))
        self.menu_item_selection_sort.setText(_translate("menu_item_selection_sort", "Выбором"))
        self.menu_item_exchange_sort.setText(_translate("menu_item_exchange_sort", "Обменом"))
        self.menu_item_fast_sort.setText(_translate("menu_item_fast_sort", "Быстрая"))
        self.menu_item_tree_sort.setText(_translate("menu_item_tree_sort", "Деревом"))
        self.menu_item_heap_sort.setText(_translate("menu_item_heap_sort", "Пирамидальная"))
        self.menu_item_shell_sort.setText(_translate("menu_item_shell_sort", "Шелла"))
        self.menu_item_merge_sort.setText(_translate("menu_item_merge_sort", "Слиянием"))
        self.menu_item_test.setText(_translate("menu_item_test", "Тест"))
