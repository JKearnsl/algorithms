import sys

from PyQt6.QtWidgets import QApplication

from src.model.fsp import FSPModel
from src.controller.fsp import FSPController


def main():
    app = QApplication(sys.argv)

    model = FSPModel()
    controller = FSPController(model)

    app.exec()


if __name__ == '__main__':
    sys.exit(main())
