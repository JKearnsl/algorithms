import os
from pathlib import Path
from typing import Iterable

from textual.containers import Container, Horizontal
from textual.screen import Screen
from textual.validation import Function
from textual.widgets import Input, Button, DirectoryTree, Footer, Header


class FilteredDirectoryTree(DirectoryTree):

    def __init__(self, path: Path, endswith: str = ".bmp"):
        super().__init__(path)
        self.endswith = endswith

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [
            path
            for path in paths
            if path.is_dir() and not path.name.startswith('.') or path.name.endswith(self.endswith)
        ]


def validate_path(path: str) -> bool:
    if os.path.isfile(path.strip()):
        return True
    return False


class BMPLoadWidget(Container):

    def __init__(self):
        self.filepath = Input(
            placeholder="Введите путь к файлу",
            validators=[
                Function(validate_path, "Неверный путь к файлу")
            ],
        )
        self.filepath.styles.width = "60%"

        button_fc = Button(
            label="Выбрать файл",
            variant="primary",
            id="chooserClicked"
        )
        button_fc.styles.width = "10%"
        button_fc.press = self.file_choose_clicked

        button_continue = Button(
            label="Продолжить",
            variant="success",
            id="continueClicked"
        )
        button_continue.styles.width = "20%"
        button_continue.styles.margin = 0, 1, 0, 1
        button_continue.press = self.continue_clicked

        self.horizontal = Horizontal(
            self.filepath, button_fc, button_continue
        )

        super().__init__(
            self.horizontal
        )
        self.styles.align_vertical = "middle"
        self.styles.align_horizontal = "center"
        self.styles.padding = 10

    def file_choose_clicked(self):
        self.app.switch_mode("file_chose")

    def continue_clicked(self):
        filepath = self.filepath.value

        if os.path.isfile(filepath):
            self.app.switch_mode("main_menu")
        else:
            self.filepath.validation_error = "Неверный путь к файлу"


class FileChoseScreen(Screen):
    directory: FilteredDirectoryTree

    BINDINGS = [
        ("c", "cancel", "Отменить"),
        ("s", "confirm", "Выбрать"),
    ]

    def compose(self):
        self.directory = FilteredDirectoryTree(Path.home())
        yield self.directory
        yield Footer()

    def action_cancel(self):
        self.app.switch_mode("select_file")

    def action_confirm(self):
        filepath = self.app.MODES["select_file"].bmp_load.filepath
        filepath.clear()
        filepath.insert_text_at_cursor(str(self.directory.cursor_node.data.path))
        self.app.switch_mode("select_file")


class BMPLoadScreen(Screen):
    bmp_load = BMPLoadWidget()

    BINDINGS = [
        ("q", "exit", "Выход"),
    ]

    def compose(self):
        yield Header()
        yield self.bmp_load
        yield Footer()

        self.title = "Выбор BMP файла"

    def action_exit(self):
        self.app.exit()
