from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt


class RGI(QtWidgets.QWidget):
    """
    Виджет представляет собой элемент входных
    данных графа: связь между вершинами.
    """

    valueChanged = QtCore.pyqtSignal(tuple)

    def __init__(self, index, _from=0, _to=0, _weight=0, *args, **kwargs):
        super().__init__()

        self._index = index

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(20, 5, 20, 5)

        layout.addWidget(QtWidgets.QLabel(f"[{index + 1}]"))

        layout.addItem(QtWidgets.QSpacerItem(
            15, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        ))

        layout.addWidget(QtWidgets.QLabel("Из: "))
        self._from_widget = QtWidgets.QLineEdit()
        self._from_widget.setMaximumWidth(50)
        self._from_widget.setValidator(QtGui.QIntValidator())
        self._from_widget.setText(str(_from))
        self._from_widget.textChanged.connect(self.signal_change)
        layout.addWidget(self._from_widget)

        layout.addWidget(QtWidgets.QLabel("В: "))
        self._to_widget = QtWidgets.QLineEdit()
        self._to_widget.setMaximumWidth(50)
        self._to_widget.setValidator(QtGui.QIntValidator())
        self._to_widget.setText(str(_to))
        self._to_widget.textChanged.connect(self.signal_change)
        layout.addWidget(self._to_widget)

        layout.addWidget(QtWidgets.QLabel("Вес: "))
        self._weight_widget = QtWidgets.QLineEdit()
        self._weight_widget.setMaximumWidth(50)
        self._weight_widget.setValidator(QtGui.QIntValidator())
        self._weight_widget.setText(str(_weight))
        self._weight_widget.textChanged.connect(self.signal_change)
        layout.addWidget(self._weight_widget)

        self.setLayout(layout)

    @property
    def from_node(self):
        return self._from_widget.text()

    @property
    def to_node(self):
        return self._to_widget.text()

    @property
    def weight(self):
        return self._weight_widget.text()

    @from_node.setter
    def from_node(self, value):
        self._from_widget.setText(str(value))

    @to_node.setter
    def to_node(self, value):
        self._to_widget.setText(str(value))

    @weight.setter
    def weight(self, value):
        self._weight_widget.setText(str(value))

    def signal_change(self):
        """
        Вызывается при изменении любого из полей
        """
        from_value = self._from_widget.text()
        to_value = self._to_widget.text()
        weight_value = self._weight_widget.text()

        if not from_value or not to_value or not weight_value:
            return

        try:
            from_value = int(from_value)
            to_value = int(to_value)
            weight_value = int(weight_value)
        except ValueError:
            return

        self.valueChanged.emit((self._index, from_value, to_value, weight_value))
