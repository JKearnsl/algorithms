from PyQt6 import QtCore, QtWidgets, QtGui

from src.views.sort.input_widget import InputArray
from src.views.widgets import WidgetsFactory


class UiSort:
    def setup_ui(self, sort: QtWidgets.QWidget, theme_class, widgets_factory: WidgetsFactory):
        sort.setObjectName("sort")
        sort_layout = QtWidgets.QVBoxLayout(sort)
        sort_layout.setContentsMargins(0, 0, 0, 0)
        sort_layout.setSpacing(0)

        customize_sheet = QtWidgets.QWidget(sort)
        customize_sheet.setObjectName("customize_sheet")
        customize_sheet.setStyleSheet("""
            QWidget#customize_sheet {
                background-color: $BG3;
            }
        """.replace(
            "$BG3", theme_class.third_background)
        )
        sort_layout.addWidget(customize_sheet)

        central_layout = QtWidgets.QVBoxLayout(customize_sheet)
        central_layout.setContentsMargins(20, 20, 20, 20)
        central_layout.setSpacing(10)
        central_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)

        sort_layout = QtWidgets.QVBoxLayout()
        sort_layout.setContentsMargins(0, 0, 0, 0)
        sort_layout.setSpacing(10)

        # Header
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(10)
        central_layout.addLayout(header_layout)

        sort_header = widgets_factory.heading2(parent=sort)
        sort_header.setObjectName("sort_header")
        header_layout.addWidget(sort_header)
        self.sort_header = sort_header

        header_layout.addStretch(1)

        sort_complexity = widgets_factory.heading4(parent=sort)
        sort_complexity.setObjectName("sort_complexity")
        header_layout.addWidget(sort_complexity)
        self.sort_complexity = sort_complexity

        # Input

        input_header = widgets_factory.heading3(parent=sort)
        input_header.setObjectName("input_header")
        sort_layout.addWidget(input_header)
        self.input_header = input_header

        input_layout = QtWidgets.QVBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(10)
        sort_layout.addLayout(input_layout)

        input_widget = InputArray(
            selection_color=theme_class.selection,
            primary_text_color=theme_class.text_primary,
            hover_color=theme_class.hover,
            third_background_color=theme_class.third_background
        )
        input_widget.setObjectName("input_widget")
        input_widget.setMaximumHeight(100)
        input_layout.addWidget(input_widget)

        self.input_widget = input_widget

        # ---> Tools
        tools_layout = QtWidgets.QHBoxLayout()
        tools_layout.setContentsMargins(0, 0, 0, 0)
        tools_layout.setSpacing(10)
        tools_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        tools_layout.addStretch(1)
        input_layout.addLayout(tools_layout)

        input_type = widgets_factory.combo_box()
        input_type.setObjectName("input_type")
        input_type.setFixedWidth(100)
        input_type.setToolTip("Тип элементов массива")
        self.input_type = input_type

        tools_layout.addWidget(input_type)

        length_line_widget = widgets_factory.line_edit()
        length_line_widget.setObjectName("length_line_widget")
        length_line_widget.setMaximumWidth(80)
        length_line_widget.setToolTip("Длина списка")
        length_line_widget.setValidator(
            QtGui.QIntValidator(1, 999999, parent=length_line_widget)
        )
        length_line_widget.set_required(True)

        tools_layout.addWidget(length_line_widget)
        self.length_line_widget = length_line_widget

        generate_button = widgets_factory.button(parent=sort)
        generate_button.setObjectName("generate_button")
        tools_layout.addWidget(generate_button)
        self.generate_button = generate_button

        # Output

        output_header = widgets_factory.heading3(parent=sort)
        output_header.setObjectName("output_header")
        sort_layout.addWidget(output_header)
        self.output_header = output_header

        output_widget = widgets_factory.textarea()
        output_widget.setObjectName("output_widget")
        output_widget.setReadOnly(True)
        sort_layout.addWidget(output_widget)
        self.output_widget = output_widget

        central_layout.addLayout(sort_layout)
        self.translate_ui(sort)
        QtCore.QMetaObject.connectSlotsByName(sort)

    def translate_ui(self, sort: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
        self.sort_header.setText(
            _translate("sort_header", "Сортировка Обменом")
        )
        self.input_header.setText(
            _translate("input_header", "Ввод")
        )
        self.output_header.setText(
            _translate("output_header", "Вывод")
        )
        self.input_widget.setPlaceholderText(
            _translate("input_widget", "Введите список")
        )
        self.generate_button.setText(
            _translate("generate_button", "Сгенерировать")
        )
        self.length_line_widget.setPlaceholderText(
            _translate("length_line_widget", "Длина")
        )
        self.output_widget.setPlaceholderText(
            _translate("output_widget", "Отсортированный список")
        )
