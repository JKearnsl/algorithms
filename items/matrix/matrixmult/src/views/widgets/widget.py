from PyQt6.QtWidgets import QWidget


class Widget(QWidget):
    def __init__(self, hover_color, parent=None):
        super().__init__(parent)
        self.styles = """
            QWidget:disabled {
                background-color: $HOVER
            }
        """.replace(
            "$HOVER", hover_color,
        )
        self.setStyleSheet = self.__decorator_set_style_sheet(self.setStyleSheet)

    def __decorator_set_style_sheet(self, func: callable):
        def override(style: str):
            self.styles += style
            func(self.styles)

        return override

