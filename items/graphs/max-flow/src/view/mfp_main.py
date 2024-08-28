from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem, QGraphicsScene, QGraphicsProxyWidget

from src.utils.graph import Graph
from src.utils.observer import DObserver
from src.utils.ts_meta import TSMeta
from src.view.MainWindow import Ui_MainWindow
from src.model.enum.graph import GraphType, ShowAs
from src.model.enum.algorithm import AlgType
from src.widgets.relationGraphItem import RGI
from src.model.mfp import MFPModel


class MFPMainView(QMainWindow, DObserver, metaclass=TSMeta):

    def __init__(self, controller, model: MFPModel, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.controller = controller
        self.model = model

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Инициализация виджетов
        for el in AlgType:
            self.ui.algInput.addItem(el.value, el)

        for el in GraphType:
            self.ui.graphType.addItem(el.value, el)

        for el in ShowAs:
            self.ui.showAsBox.addItem(el.value, el)

        self.ui.inputGraph.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.ui.inputGraph.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ui.sourceInput.setValidator(QtGui.QIntValidator())
        self.ui.targetInput.setValidator(QtGui.QIntValidator())

        # Регистрация представлений
        self.model.add_observer(self)

        # События
        self.ui.algInput.currentIndexChanged.connect(self.controller.alg_changed)
        self.ui.sourceInput.textChanged.connect(self.controller.source_changed)
        self.ui.targetInput.textChanged.connect(self.controller.target_changed)
        self.ui.graphType.currentIndexChanged.connect(self.controller.graph_type_changed)
        self.ui.showAsBox.currentIndexChanged.connect(self.controller.show_as_changed)
        self.ui.updateGraph.clicked.connect(self.controller.update_graph_clicked)

        self.ui.rmVertexButton.clicked.connect(self.controller.remove_link_clicked)
        self.ui.addVertexButton.clicked.connect(self.controller.add_link_clicked)

        self.ui.open_file.triggered.connect(self.controller.open_file)
        self.ui.save_file.triggered.connect(self.controller.save_file)
        self.ui.about.triggered.connect(self.controller.about)

    def model_changed(self):

        # Список входных ребер
        while len(self.model.graph_links) != self.ui.inputGraph.count():
            if len(self.model.graph_links) < self.ui.inputGraph.count():
                item = self.ui.inputGraph.takeItem(self.ui.inputGraph.count() - 1)
                self.ui.inputGraph.removeItemWidget(item)
                del item
            elif len(self.model.graph_links) > self.ui.inputGraph.count():
                item = QListWidgetItem(self.ui.inputGraph)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                widget = RGI(len(self.model.graph_links) - 1)
                widget.valueChanged.connect(self.controller.update_graph_link)
                item.setSizeHint(widget.sizeHint())
                self.ui.inputGraph.addItem(item)
                self.ui.inputGraph.setItemWidget(item, widget)

        for i in range(len(self.model.graph_links)):
            widget = self.ui.inputGraph.itemWidget(self.ui.inputGraph.item(i))
            link = self.model.graph_links[i]
            link_from = link["from_node"]
            link_to = link["to_node"]
            link_weight = link["weight"]
            if widget.from_node != link_from or widget.to_node != link_to or widget.weight != link_weight:
                widget.from_node = link_from
                widget.to_node = link_to
                widget.weight = link_weight
                widget.update()

        # Перерисовка графа
        graph = Graph(node_size=1000, arrows=True if self.model.graph_type == GraphType.DIRECTED else False)

        gdata = self.model.graph_links if self.model.show_graph_as == ShowAs.FULL_GRAPH else self.model.flow_network

        for branch in gdata:
            graph.add_edge(str(branch["from_node"]), str(branch["to_node"]), str(branch["weight"]))

        graph.canvas().figure.clf()
        scene = self.ui.graphView.scene()
        if scene is not None:
            for item in scene.items():
                scene.removeItem(item)

        scene = QGraphicsScene()
        self.ui.graphView.setScene(scene)
        proxy_widget = QGraphicsProxyWidget()
        proxy_widget.setWidget(graph.canvas(
            width=self.ui.graphView.width() / self.ui.graphView.physicalDpiX() * 1.5,
            height=self.ui.graphView.height() / self.ui.graphView.physicalDpiY() * 1.5,
        ))
        scene.addItem(proxy_widget)

        # Установка значений которые могут быть изменены
        if self.model.source is not None:
            self.ui.sourceInput.setText(str(self.model.source))
            self.ui.outputSource.setText(str(self.model.source))
        else:
            self.ui.outputSource.setText("")

        if self.model.target is not None:
            self.ui.targetInput.setText(str(self.model.target))
            self.ui.outputTarget.setText(str(self.model.target))
        else:
            self.ui.outputTarget.setText("")

        if self.model.max_flow is not None:
            self.ui.outputMaxFlow.setText(str(self.model.max_flow))

    def about(self):
        messagebox = QtWidgets.QMessageBox(self)
        messagebox.setTextFormat(Qt.TextFormat.MarkdownText)
        messagebox.setIcon(QtWidgets.QMessageBox.Icon.Information)
        messagebox.setWindowTitle("О программе")
        messagebox.setText(
            "Разработчик: JKearnsl "
            "[GitHub](https://github.com/JKearnsl/maximum_flow_problem)"
        )
        messagebox.exec()

    def show_error(self, message: str, title: str = "Ошибка"):
        messagebox = QtWidgets.QMessageBox(self)
        messagebox.setTextFormat(Qt.TextFormat.MarkdownText)
        messagebox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        messagebox.setWindowTitle(title)
        messagebox.setText(message)
        messagebox.exec()

    def show_info(self, message: str, title: str = "Информация"):
        messagebox = QtWidgets.QMessageBox(self)
        messagebox.setTextFormat(Qt.TextFormat.MarkdownText)
        messagebox.setIcon(QtWidgets.QMessageBox.Icon.Information)
        messagebox.setWindowTitle(title)
        messagebox.setText(message)
        messagebox.exec()