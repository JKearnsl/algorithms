from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Footer, Button, Header, Log

from src.core import bmp


class OutLog(Log):
    def __init__(self):
        super().__init__()
        self.styles.background = "black"


class ColorPartsMenu(Container):

    def __init__(self):
        manual_btn = Button("1. Ручной способ", "primary")
        manual_btn.press = lambda: self.manual_clicked()
        automatically_btn = Button("2. Автоматический (Pillow)", "primary")
        automatically_btn.press = lambda: self.automatically_clicked()

        exit_btn = Button("3. Назад", "primary")
        exit_btn.press = lambda: self.app.switch_mode("main_menu")

        super().__init__(
            manual_btn,
            automatically_btn,
            exit_btn,
        )

    def manual_clicked(self):
        self.out_log.clear()
        result = bmp.color_components_manually(self.filepath)
        self.out_log.write_line("Результат:")
        for path in result:
            self.out_log.write_line(path)

    def automatically_clicked(self):
        self.out_log.clear()
        result = bmp.color_components(self.filepath)
        self.out_log.write_line("Результат:")
        for path in result:
            self.out_log.write_line(path)

    @property
    def filepath(self) -> str:
        return self.parent.filepath

    @property
    def out_log(self) -> OutLog:
        return self.parent.out_log


class ColorMenuScreen(Screen):

    def compose(self):
        yield Header()
        yield ColorPartsMenu()
        self.out_log = OutLog()
        yield self.out_log
        yield Footer()

        self.title = "Выберите способ"

        self.styles.align_vertical = "middle"
        self.styles.align_horizontal = "center"

    @property
    def filepath(self) -> str:
        return self.app.MODES["select_file"].bmp_load.filepath.value
