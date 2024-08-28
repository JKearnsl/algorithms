import sys

from PyQt6.QtWidgets import QApplication

from src.model.fsp import MSTModel
from src.controller.fsp import MSTController


def main():
    app = QApplication(sys.argv)

    model = MSTModel()
    controller = MSTController(model)

    app.exec()


if __name__ == '__main__':
    sys.exit(main())
