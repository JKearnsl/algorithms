import sys

from PyQt6.QtWidgets import QApplication

from src.model.sig_model import SIGModel
from src.controller.sig_controller import SIGController


def main():
    app = QApplication(sys.argv)

    model = SIGModel()
    controller = SIGController(model)

    app.exec()


if __name__ == '__main__':
    sys.exit(main())
