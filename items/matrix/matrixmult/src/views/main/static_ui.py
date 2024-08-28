from PyQt6 import QtCore, QtGui, QtWidgets

from src.views.widgets import WidgetsFactory
from src.views.widgets.list import ListItemWidget


class UiMainWindow:
    def setup_ui(
            self,
            main_window: QtWidgets.QWidget,
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
        
            QWidget#main_window:disabled {
                background-color: $HOVER;
            }
        
            QToolTip {
                background: #D9DBDD;
                border: 1px solid #000000;
                border-radius: 3px;
                color: #000000;
            }
        """.replace(
            "$BG1", theme_class.first_background
        ).replace(
            "$HOVER", theme_class.hover
        ))
        central_layout = QtWidgets.QHBoxLayout(main_window)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        # Menu widget
        menu_widget = widgets_factory.widget(main_window)
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
        menu_layout.setContentsMargins(0, 0, 1, 0)
        menu_layout.setSpacing(10)
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
        matrix_list_widget = widgets_factory.list()
        matrix_list_widget.setObjectName("matrix_list_widget")
        menu_layout.addWidget(matrix_list_widget)
        self.matrix_list_widget = matrix_list_widget

        # Tool section
        menu_tool_layout = QtWidgets.QHBoxLayout()
        menu_tool_layout.setContentsMargins(10, 0, 10, 0)
        menu_layout.addLayout(menu_tool_layout)
        menu_layout.addItem(
            QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        )

        menu_settings_button = widgets_factory.tool_button(QtGui.QIcon("icons:settings-64.png"))
        self.menu_settings_button = menu_settings_button
        menu_tool_layout.addWidget(menu_settings_button)
        menu_tool_layout.addItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        )

        remove_matrix_button = widgets_factory.tool_button(QtGui.QIcon("icons:remove-gray-64.png"))
        self.remove_matrix_button = remove_matrix_button
        menu_tool_layout.addWidget(remove_matrix_button)

        add_matrix_button = widgets_factory.tool_button(QtGui.QIcon("icons:add-64.png"))
        self.add_matrix_button = add_matrix_button
        menu_tool_layout.addWidget(add_matrix_button)

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

        # Content layout
        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setObjectName("content_widget")
        central_layout.addLayout(content_layout)
        self.content_layout = content_layout

        self.translate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def translate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
