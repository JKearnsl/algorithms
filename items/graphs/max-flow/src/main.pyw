import sys

from PyQt6.QtWidgets import QApplication

from src.model.mfp import MFPModel
from src.controller.mfp_main import MFPMainController


def main():
    app = QApplication(sys.argv)

    model = MFPModel()
    controller = MFPMainController(model)

    app.exec()


if __name__ == '__main__':
    sys.exit(main())
