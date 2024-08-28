from textual.app import App

from src.views.bitplane_menu import BitPlanesMenuScreen
from src.views.bmpload import BMPLoadScreen, FileChoseScreen
from src.views.color_menu import ColorMenuScreen
from src.views.file_headers import FileHeadersScreen
from src.views.main_menu import MainMenuScreen


class BMPDecoding(App):
    BINDINGS = [("d", "toggle_dark", "Переключить тему")]

    MODES = {
        "select_file": BMPLoadScreen,
        "file_chose": FileChoseScreen,
        "main_menu": MainMenuScreen,
        "view_headers": FileHeadersScreen,
        "color_parts": ColorMenuScreen,
        "bit_slices": BitPlanesMenuScreen,
    }

    def on_mount(self) -> None:
        self.switch_mode("select_file")


if __name__ == "__main__":
    app = BMPDecoding()
    app.run()
