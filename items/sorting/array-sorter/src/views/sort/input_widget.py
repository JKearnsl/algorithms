from PyQt6 import QtCore
from PyQt6.QtGui import QValidator, QKeyEvent

from src.views.widgets import LineEdit


class ArrayValidator(QValidator):
    def __init__(self, parent):
        super().__init__(parent)

    def validate(self, string: str | None, pos: int) -> tuple['QValidator.State', str, int]:
        _ = string.replace(" ", "").split(",")
        response_str = ", ".join(_)
        position = pos if pos != len(string) else len(response_str)

        for substr in _:
            if substr.startswith("-"):
                substr = substr[1:]

            if (not substr.isdigit() or ",," in string.replace(" ", "")) and substr != "":
                return QValidator.State.Invalid, response_str, position

        return QValidator.State.Acceptable, response_str, position


class InputArray(LineEdit):

    def __init__(self, selection_color, primary_text_color, hover_color, third_background_color):
        super().__init__(selection_color, primary_text_color, hover_color, third_background_color)
        self.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhDate)
        self.setValidator(ArrayValidator(self))

    def array(self) -> list[int]:
        return [int(x) for x in self.text().replace(" ", "").split(",") if x != "" and x != "-"]

    def set_array(self, array: list[int]):
        self.setText(', '.join([str(x) for x in array]))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key.Key_Backspace and self.text().endswith(", "):
            self.setText(self.text()[:-2])
        else:
            super().keyPressEvent(event)
