from PyQt6.QtWidgets import QLineEdit


class LineEdit(QLineEdit):
    def __init__(
            self,
            selection_color,
            primary_text_color,
            hover_color,
            third_background_color,
            parent=None
    ):
        super().__init__(parent)
        self.__is_required = False
        self.__is_error_state = False
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid $HOVER;
                border-radius: 5px;
                padding: 1px 10px 1px 3px;
                background: $BG3;
                color: $PRIMARY_TEXT_COLOR;
            }
            QLineEdit:focus {
                border: 2px solid $SELECTION;
            }
            QLineEdit::placeholder {
                color: $PRIMARY_TEXT_COLOR;
            }
        """.replace(
            "$SELECTION", selection_color
        ).replace(
            "$PRIMARY_TEXT_COLOR", primary_text_color
        ).replace(
            "$HOVER", hover_color
        ).replace(
            "$BG3", third_background_color
        ))
        self.__hover_color = hover_color
        self.__selection_color = selection_color

    def add_style(self, style: str):
        self.setStyleSheet(self.styleSheet() + style)

    def set_required(self, is_required: bool):

        if self.is_required() == is_required:
            return

        self.__is_required = is_required

        if is_required:
            if self.placeholderText() and not self.placeholderText().endswith("*"):
                self.setPlaceholderText(self.placeholderText() + " *")

            self.textChanged.connect(self.__check_required)
        else:
            if self.placeholderText() and self.placeholderText().endswith("*"):
                self.setPlaceholderText(self.placeholderText()[:-2])

            if self.textChanged is not None:
                self.textChanged.disconnect(self.__check_required)

    def is_required(self):
        return self.__is_required

    def set_error(self):
        if self.__is_error_state:
            """
                Бывают ситуации, когда вызывается set_error, когда ошибка
                еще не отработала, из-за чего после вызова `set_error` сразу
                же может вызваться `remove_error`, что приводит к неожиданному
                поведению.
            """
            self.textChanged.disconnect(self.remove_error)

        self.__is_error_state = True

        self.add_style("""
            QLineEdit {
                border: 2px solid #bf7373;
            }

            QLineEdit:focus {
                border: 2px solid #b33a3a;
            }

        """)
        self.setFocus()
        self.textChanged.connect(self.remove_error)

    def remove_error(self):
        self.__is_error_state = False
        self.add_style("""
            QLineEdit {
                border: 2px solid $HOVER;
            }

            QLineEdit:focus {
                border: 2px solid $SELECTION;
            }
        """.replace(
            "$HOVER", self.__hover_color
        ).replace(
            "$SELECTION", self.__selection_color
        ))
        self.textChanged.disconnect(self.remove_error)

    def is_error_state(self):
        return self.__is_error_state

    def __check_required(self):
        if len(self.text()) == 0:
            self.set_error()
