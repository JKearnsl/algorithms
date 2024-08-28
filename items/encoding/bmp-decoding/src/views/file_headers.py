from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Footer, Header, Tabs, Tab, Markdown, DataTable

from src.core import bmp


class FileHeaders(Container):

    def __init__(self):
        tabs = Tabs(
            Tab("Ручной перебор", id="manual"),
            Tab("Автоматизированный (KaitaiBMP)", id="pillow"),
        )
        self.table = DataTable()
        self.table.add_columns("Наименование", "Значение")

        super().__init__(
            tabs,
            self.table,
        )
        self.styles.align_vertical = "top"
        self.styles.align_horizontal = "center"

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        """Handle TabActivated message sent by Tabs."""
        self.table.clear()
        if event.tab.id == "manual":
            data = bmp.get_bmp_headers_manually(self.filepath)
        elif event.tab.id == "pillow":
            data = bmp.get_bmp_headers(self.filepath)
        else:
            raise ValueError(f"Unknown tab id: {event.tab.id}")

        self.table.add_rows(data.items())

    @property
    def filepath(self) -> str:
        return self.parent.filepath


class FileHeadersScreen(Screen):
    BINDINGS = [
        ("b", "back", "Назад"),
    ]

    def compose(self):
        yield Header()
        yield FileHeaders()
        yield Footer()

        self.title = "Заголовки файла"

        self.styles.align_vertical = "top"
        self.styles.align_horizontal = "center"

    def action_back(self):
        self.app.switch_mode("main_menu")

    @property
    def filepath(self) -> str:
        return self.app.MODES["select_file"].bmp_load.filepath.value
