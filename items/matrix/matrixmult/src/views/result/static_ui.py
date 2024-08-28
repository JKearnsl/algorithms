from PyQt6 import QtCore, QtWidgets

from src.views.widgets import WidgetsFactory


class UiResult:
    def setup_ui(self, result: QtWidgets.QWidget, theme_class, widgets_factory: WidgetsFactory):
        result.setObjectName("result")
        result_layout = QtWidgets.QVBoxLayout(result)
        result_layout.setContentsMargins(0, 0, 0, 0)
        result_layout.setSpacing(0)

        customize_sheet = QtWidgets.QWidget(result)
        customize_sheet.setObjectName("customize_sheet")
        customize_sheet.setStyleSheet("""
            QWidget#customize_sheet {
                background-color: $BG3;
            }
            QWidget#customize_sheet:disabled {
                background-color: $HOVER;
            }
        """.replace(
            "$BG3", theme_class.third_background
        ).replace(
            "$HOVER", theme_class.hover
        )
        )
        result_layout.addWidget(customize_sheet)

        central_layout = QtWidgets.QVBoxLayout(customize_sheet)
        central_layout.setContentsMargins(20, 20, 20, 20)
        central_layout.setSpacing(10)
        central_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)

        result_layout = QtWidgets.QVBoxLayout()
        result_layout.setContentsMargins(0, 0, 0, 0)
        result_layout.setSpacing(10)

        # Header
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(10)
        central_layout.addLayout(header_layout)

        result_header = widgets_factory.heading2(parent=result)
        result_header.setObjectName("result_header")
        header_layout.addWidget(result_header)
        self.result_header = result_header

        header_layout.addStretch(1)

        result_complexity = widgets_factory.heading4(parent=result)
        result_complexity.setObjectName("result_complexity")
        header_layout.addWidget(result_complexity)
        self.result_complexity = result_complexity

        # Info

        info_header = widgets_factory.heading3(parent=result)
        info_header.setObjectName("info_header")
        result_layout.addWidget(info_header)
        self.info_header = info_header

        info_layout = QtWidgets.QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(10)
        result_layout.addLayout(info_layout)

        # ---> Input Matrix info
        imo_layout = QtWidgets.QHBoxLayout()
        imo_layout.setContentsMargins(0, 0, 0, 0)
        imo_layout.setSpacing(10)
        info_layout.addLayout(imo_layout)

        imo_count_label = widgets_factory.label()
        imo_layout.addWidget(imo_count_label)
        self.imo_count_label = imo_count_label

        imo_count_value = widgets_factory.label()
        imo_layout.addWidget(imo_count_value)
        self.imo_count_value = imo_count_value

        imo_layout.addStretch(1)

        # ---> Count Of Scalar Mult
        csm_layout = QtWidgets.QHBoxLayout()
        csm_layout.setContentsMargins(0, 0, 0, 0)
        csm_layout.setSpacing(10)
        info_layout.addLayout(csm_layout)

        csm_count_label = widgets_factory.label()
        csm_layout.addWidget(csm_count_label)
        self.csm_count_label = csm_count_label

        csm_count_value = widgets_factory.label()
        csm_layout.addWidget(csm_count_value)
        self.csm_count_value = csm_count_value

        csm_layout.addStretch(1)

        # ---> Show Steps
        show_steps_button = widgets_factory.button(parent=result)
        show_steps_button.setObjectName("show_steps_button")
        show_steps_button.setMaximumWidth(150)
        info_layout.addWidget(show_steps_button)
        self.show_steps_button = show_steps_button

        # Output
        output_header_layout = QtWidgets.QHBoxLayout()
        result_layout.addLayout(output_header_layout)

        output_header = widgets_factory.heading3(parent=result)
        output_header.setObjectName("output_header")
        output_header_layout.addWidget(output_header)
        self.output_header = output_header

        output_header_layout.addStretch(1)

        calculate_button = widgets_factory.button(parent=result)
        calculate_button.setObjectName("calculate_button")
        output_header_layout.addWidget(calculate_button)
        self.calculate_button = calculate_button

        matrix = widgets_factory.matrix()
        matrix.setObjectName("matrix")
        result_layout.addWidget(matrix)
        self.matrix = matrix

        central_layout.addLayout(result_layout)
        self.translate_ui(result)
        QtCore.QMetaObject.connectSlotsByName(result)

    def translate_ui(self, result: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate

        self.imo_count_label.setText(
            _translate("imo_count_label", "Кол-во матриц")
        )
        self.csm_count_label.setText(
            _translate("csm_count_label", "Скалярных умножений")
        )

        self.result_header.setText(
            _translate("result_header", "Результат умножения")
        )
        self.info_header.setText(
            _translate("info_header", "Информация")
        )
        self.output_header.setText(
            _translate("output_header", "Выходная матрица")
        )
        self.calculate_button.setText(
            _translate("calculate_button", "Рассчитать")
        )
        self.show_steps_button.setText(
            _translate("show_steps_button", "Показать шаги")
        )
