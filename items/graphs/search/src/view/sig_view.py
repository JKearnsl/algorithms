import networkx
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem, QGraphicsScene, QGraphicsProxyWidget, QListView

from src.model.enum.graph import GraphType, ShowAs
from src.model.enum.problem import ProblemType
from src.utils.graph import Graph
from src.utils.observer import TransportSolutionDObserver
from src.utils.ts_meta import TSMeta
from src.view.MainWindow import Ui_MainWindow
from src.widgets.relationGraphItem import RGI


class SIGView(QMainWindow, TransportSolutionDObserver, metaclass=TSMeta):
    """
    Визуальное представление SIGModel.

    """

    def __init__(self, controller, model, parent=None):

        super(QMainWindow, self).__init__(parent)
        self.controller = controller
        self.model = model

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        for el in ProblemType:
            self.ui.problemType.addItem(el.value, el)

        for el in GraphType:
            self.ui.graphType.addItem(el.value, el)

        for el in ShowAs:
            self.ui.showAs.addItem(el.value, el)

        self.ui.inputGraph.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.ui.inputGraph.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.ui.outputTable.setModel(QStandardItemModel(1, 1))
        self.ui.outputTable.model().setHorizontalHeaderLabels([" "])
        self.ui.outputTable.model().setVerticalHeaderLabels([" "])
        self.ui.outputTable.setColumnWidth(0, 50)

        # Регистрация представлений
        self.model.add_observer(self)

        # События
        self.ui.problemType.currentIndexChanged.connect(self.controller.input_problem_type)
        self.ui.graphType.currentIndexChanged.connect(self.controller.input_graph_type)
        self.ui.showAs.currentIndexChanged.connect(self.controller.input_show_as)
        self.ui.searchValue.textChanged.connect(self.controller.input_search_value)
        self.ui.startVertex.textChanged.connect(self.controller.input_start_vertex)
        self.ui.addVertexButton.clicked.connect(self.controller.add_link)
        self.ui.rmVertexButton.clicked.connect(self.controller.remove_link)
        self.ui.updateGraph.clicked.connect(self.controller.update_graph_canvas)

    def model_changed(self):
        """
        Метод вызывается при изменении модели.
        Запрашивает и отображает решение
        """
        self.ui.inputGraph.clear()

        for i, el in enumerate(self.model.graph_links):
            _from, _to = el
            item = QListWidgetItem(self.ui.inputGraph)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            rgi_widget = RGI(i, _from, _to)
            rgi_widget.valueChanged.connect(self.controller.graph_data_changed)
            self.ui.inputGraph.addItem(item)
            item.setSizeHint(rgi_widget.sizeHint())
            self.ui.inputGraph.setItemWidget(item, rgi_widget)

        # Перерисовка графа
        graph = Graph(arrows=self.model.graph_type == GraphType.DIRECTED)
        if self.model.show_as == ShowAs.FULL_GRAPH:
            graph_data = self.model.graph_links
        elif self.model.show_as == ShowAs.VISITED_PATH:
            graph_data = self.model.visited_path
        else:
            graph_data = []

        try:
            graph.canvas().figure.clf()
            graph.clear()
        except networkx.exception.NetworkXError:
            #
            # Если очень быстро удаляется граф, то возникает ошибка
            #
            pass

        for link in graph_data:
            graph.add_edge(*link)

        if graph_data:
            if self.model.start_vertex:
                vertices = [el[0] for el in graph_data] + [el[1] for el in graph_data]
                if self.model.start_vertex in vertices:
                    graph.style_node(self.model.start_vertex, node_color='aquamarine', node_size=500)

            if self.model.search_value and self.model.is_found:
                graph.style_node(self.model.search_value, node_color='red', node_size=500)

        scene = self.ui.outputGraph.scene()
        if scene is not None:
            for item in scene.items():
                scene.removeItem(item)

        scene = QGraphicsScene()
        self.ui.outputGraph.setScene(scene)
        proxy_widget = QGraphicsProxyWidget()
        proxy_widget.setWidget(graph.canvas(
            width=self.ui.outputGraph.width() / self.ui.outputGraph.physicalDpiX() * 1.5,
            height=self.ui.outputGraph.height() / self.ui.outputGraph.physicalDpiY() * 1.5,
        ))
        scene.addItem(proxy_widget)

        # Время поиска
        if self.model.search_time:
            self.ui.searchTime.setText(f"Время: {round(self.model.search_time, 6)} мс.")

        # Перерисовка таблицы
        table, vertexes = self.model.graph_table()

        if not table:
            self.ui.outputTable.setColumnWidth(0, 50)
            return

        self.ui.outputTable.model().setRowCount(len(table))
        self.ui.outputTable.model().setColumnCount(len(table[0]))
        self.ui.outputTable.model().setHorizontalHeaderLabels(vertexes)
        self.ui.outputTable.model().setVerticalHeaderLabels(vertexes)

        for i, row in enumerate(table):
            for j, el in enumerate(row):
                item = QStandardItem(str(el))
                item.setEditable(False)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ui.outputTable.setColumnWidth(j, 50)
                if el == "+":
                    item.setBackground(QColor(0, 255, 0, 100))
                self.ui.outputTable.model().setItem(i, j, item)
