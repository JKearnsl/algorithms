"""

"""
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QToolButton


class ToolButton(QToolButton):
    def __init__(self, hover_color, text_primary_color, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QToolButton {
                border-radius: 3px;
                background-color: transparent;
                color: $TEXT;
            }
            QToolButton:hover {
                background-color: $HOVER;
            }
            QToolButton:pressed {
                background-color: transparent;
            }

            QToolButton:disabled {
                background-color: $HOVER;
            }
        """.replace(
            "$HOVER", hover_color,
        ).replace(
            "$TEXT", text_primary_color,
        ))

        self.setIconSize(QtCore.QSize(16, 16))
        self.setFixedSize(16, 16)

        self.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=10,
            color=QtGui.QColor(0, 0, 0, 50),
            offset=QtCore.QPointF(0, 0)
        ))
