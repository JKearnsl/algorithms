from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QPushButton, QGraphicsDropShadowEffect


class Button(QPushButton):
    def __init__(self, hover_color, text_primary_color, third_background_color, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: $BG3;
                border: 1px solid $HOVER;
                border-radius: 4px;
                padding: 2px 4px;
                color: $TEXT;
            }
            QPushButton:hover {
                background-color: $HOVER;
            }
            QPushButton:pressed {
                background-color: $BG3;
            }
            
            QPushButton:disabled {
                background-color: $HOVER;
                color: $TEXT;
            }
        """.replace(
            "$HOVER", hover_color,
        ).replace(
            "$TEXT", text_primary_color,
        ).replace(
            "$BG3", third_background_color,
        ))

        self.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=10,
            color=QtGui.QColor(0, 0, 0, 50),
            offset=QtCore.QPointF(0, 0)
        ))
