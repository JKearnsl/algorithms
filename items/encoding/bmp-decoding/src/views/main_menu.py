from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Footer, Button, Header


class MainMenu(Container):

    def __init__(self):
        view_headers_btn = Button("1. Отобразить заголовки", "primary")
        view_headers_btn.press = lambda: self.app.switch_mode("view_headers")
        color_parts_btn = Button("2. Цветовые составляющие", "primary")
        color_parts_btn.press = lambda: self.app.switch_mode("color_parts")
        bit_slices = Button("3. Битовые срезы", "primary")
        bit_slices.press = lambda: self.app.switch_mode("bit_slices")
        color_parts_btn.press = lambda: self.app.switch_mode("color_parts")
        select_file_btn = Button("4. Выбрать файл", "primary")
        select_file_btn.press = lambda: self.app.switch_mode("select_file")
        exit_btn = Button("5. Выход", "primary")
        exit_btn.press = lambda: self.app.exit()

        super().__init__(
            view_headers_btn,
            color_parts_btn,
            bit_slices,
            select_file_btn,
            exit_btn,
        )


class MainMenuScreen(Screen):
    CSS_PATH = "css/main_menu.tcss"

    def compose(self):
        yield Header()
        yield MainMenu()
        yield Footer()

        self.title = "Главное меню"

        self.styles.align_vertical = "middle"
        self.styles.align_horizontal = "center"

    @property
    def filepath(self) -> str:
        return self.app.MODES["select_file"].bmp_load.filepath.value
