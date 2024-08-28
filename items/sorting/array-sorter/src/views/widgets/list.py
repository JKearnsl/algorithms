from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QListView


class List(QListView):
    def __init__(
            self,
            text_primary_color,
            hover_color,
            selection_color,
            parent=None
    ):
        super().__init__(parent)

        self.setStyleSheet("""
            QListView {
                background-color: transparent;
                selection-background-color: transparent;
                outline: none;
            }
            QListView::item {
                border: none;
                padding-left: 10px;
                font-size: 14px;
                font-weight: bold;
                color: $TEXT_PRIMARY;
            }
            QListView::item:hover {
                background-color: $HOVER;
            }
            QListView::item:selected {
                background: $SELECTION;
                color: #ffffff;
            }
                """.replace(
            "$TEXT_PRIMARY", text_primary_color
        ).replace(
            "$HOVER", hover_color
        ).replace(
            "$SELECTION", selection_color
        ))
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.setMovement(QtWidgets.QListView.Movement.Static)
        self.setFlow(QtWidgets.QListView.Flow.TopToBottom)
        self.setResizeMode(QtWidgets.QListView.ResizeMode.Fixed)
        self.setSpacing(0)
        self.setUniformItemSizes(True)
        self.setWordWrap(False)
        self.setWrapping(False)
        self.setMouseTracking(True)
        self.setTabKeyNavigation(False)
        self.setFrameStyle(0)

        self.setModel(QtGui.QStandardItemModel())

    def add_style(self, style: str):
        self.setStyleSheet(self.styleSheet() + style)


class ListItemWidget(QtGui.QStandardItem):
    id: any

    def __init__(self, title: str, _id: any = None, icon: QtGui.QIcon = None):
        super().__init__()
        self.setText(title)
        self.id = _id
        if icon:
            self.setIcon(icon)
        self.setSizeHint(QtCore.QSize(0, 40))

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} title={self.text()}>"
