from PyQt6 import QtCore, QtWidgets, QtGui

from src.views.widgets import WidgetsFactory


class UiMatrix:
    def setup_ui(self, matrix_modal: QtWidgets.QWidget, theme_class, widgets_factory: WidgetsFactory):
        matrix_modal.setObjectName("matrix_modal")

        matrix_modal.setFixedSize(600, 500)
        matrix_modal_layout = matrix_modal.layout()
        matrix_modal_layout.setContentsMargins(0, 0, 0, 0)
        matrix_modal_layout.setSpacing(0)

        customize_sheet = QtWidgets.QWidget(matrix_modal)
        customize_sheet.setObjectName("customize_sheet")
        matrix_modal_layout.addWidget(customize_sheet)

        central_layout = QtWidgets.QVBoxLayout(customize_sheet)
        central_layout.setContentsMargins(20, 20, 20, 20)
        central_layout.setSpacing(10)
        central_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)

        # Matrix Dimension
        dimension_header = widgets_factory.heading3()
        central_layout.addWidget(dimension_header)
        self.dimension_header = dimension_header

        # Form
        form_area = QtWidgets.QHBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        form_area.addLayout(form_layout)
        form_area.addStretch(1)
        central_layout.addLayout(form_area)

        # Rows
        rows_count_label = widgets_factory.label()
        self.rows_count_label = rows_count_label

        rows_count_value = widgets_factory.spin_box()
        rows_count_value.setFixedWidth(70)
        self.rows_count_value = rows_count_value
        form_layout.addRow(rows_count_label, rows_count_value)

        # Columns
        columns_count_label = widgets_factory.label()
        self.columns_count_label = columns_count_label

        columns_count_value = widgets_factory.spin_box()
        columns_count_value.setFixedWidth(70)
        self.columns_count_value = columns_count_value
        form_layout.addRow(columns_count_label, columns_count_value)

        # Random Button
        randomize_button = widgets_factory.button()
        randomize_button.setFixedWidth(140)
        self.randomize_button = randomize_button
        form_layout.addRow(randomize_button)

        # Matrix
        matrix_header = widgets_factory.heading3()
        central_layout.addWidget(matrix_header)
        self.matrix_header = matrix_header

        matrix = widgets_factory.matrix()
        self.matrix = matrix
        central_layout.addWidget(matrix)

        self.translate_ui(matrix_modal)
        QtCore.QMetaObject.connectSlotsByName(matrix_modal)

    def translate_ui(self, matrix_modal: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
        matrix_modal.setWindowTitle(
            _translate("matrix_modal_window_title", "Матрица")
        )
        self.dimension_header.setText(
            _translate("matrix_modal_setups", "Установки")
        )
        self.rows_count_label.setText(
            _translate("matrix_modal_rows_count_label", "Строк")
        )
        self.columns_count_label.setText(
            _translate("matrix_modal_columns_count_label", "Колонок")
        )
        self.randomize_button.setText(
            _translate("matrix_modal_randomize_button", "Автозаполнение")
        )
        self.matrix_header.setText(
            _translate("matrix_modal_matrix_label", "Матрица")
        )
