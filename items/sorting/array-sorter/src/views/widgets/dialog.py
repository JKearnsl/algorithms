from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLayout, QHBoxLayout, QWidget, QGraphicsDropShadowEffect


class Dialog(QDialog):

    def __init__(
            self,
            third_background,
            second_background,
            hover,
            text_header,
            parent=None
    ):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Dialog")
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFixedSize(400, 300)

        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.setSpacing(0)

        sheet = QWidget(self)
        sheet.setObjectName("sheet")
        sheet.setStyleSheet("""
            QWidget#sheet {
                background-color: $BG3;
                border-radius: 10px;
            }
        """.replace(
            "$BG3", third_background
        ))
        dialog_layout.addWidget(sheet)

        general_layout = QVBoxLayout(sheet)
        general_layout.setContentsMargins(0, 0, 0, 0)
        general_layout.setSpacing(0)

        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        general_layout.addLayout(header_layout)

        exit_button = QPushButton(self)
        exit_button.setFixedSize(30, 30)
        exit_button.setText("×")
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: $BG2;
                border-bottom-left-radius: 10px;
                border-top-right-radius: 10px;
                color: $TEXT_HEADER;
                font-size: 26px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: $HOVER;
            }
            QPushButton:pressed {
                background-color: $BG2;
            }
        """.replace(
            "$BG2", second_background
        ).replace(
            "$HOVER", hover
        ).replace(
            "$TEXT_HEADER", text_header
        ))

        exit_button.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=10,
            color=QtGui.QColor(0, 0, 0, 50),
            offset=QtCore.QPointF(0, 0)
        ))

        exit_button.clicked.connect(self.close)
        header_layout.addWidget(exit_button)

        self.__layout = QVBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)
        general_layout.addLayout(self.__layout)

    def layout(self) -> QLayout | None:
        return self.__layout
