from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem, QGraphicsScene, QGraphicsProxyWidget

from src.model.enum.graph import ShowGraphAs
from src.model.enum.problem import AlgorithmType
from src.utils.observer import TransportSolutionDObserver
from src.utils.ts_meta import TSMeta
from src.view.MainWindow import Ui_MainWindow
from src.widgets.relationGraphItem import RGI
from utils.graph import Graph


class FSPView(QMainWindow, TransportSolutionDObserver, metaclass=TSMeta):
    """
    Визуальное представление FSPModel.

    """

    def __init__(self, controller, model, parent=None):

        super(QMainWindow, self).__init__(parent)
        self.controller = controller
        self.model = model

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        for el in AlgorithmType:
            self.ui.algType.addItem(el.value, el)

        for el in ShowGraphAs:
            self.ui.viewGraphAs.addItem(el.value, el)

        self.ui.inputGraph.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.ui.inputGraph.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Регистрация представлений
        self.model.add_observer(self)

        # События
        self.ui.algType.currentIndexChanged.connect(self.controller.input_alg_type)
        self.ui.viewGraphAs.currentIndexChanged.connect(self.controller.input_view_graph_as)
        self.ui.searchValue.textChanged.connect(self.controller.input_search_vertex)
        self.ui.startValue.textChanged.connect(self.controller.input_start_vertex)
        self.ui.addVertexButton.clicked.connect(self.controller.add_link)
        self.ui.rmVertexButton.clicked.connect(self.controller.remove_link)
        self.ui.updateGraph.clicked.connect(self.controller.update_graph_canvas)

    def model_changed(self):
        """
        Метод вызывается при изменении модели.
        Запрашивает и отображает решение
        """
        self.ui.inputGraph.clear()

        for i, el in enumerate(self.model.graph):
            item = QListWidgetItem(self.ui.inputGraph)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            rgi_widget = RGI(i, el["from_node"], el["to_node"], el["weight"])
            rgi_widget.valueChanged.connect(self.controller.graph_data_changed)
            self.ui.inputGraph.addItem(item)
            item.setSizeHint(rgi_widget.sizeHint())
            self.ui.inputGraph.setItemWidget(item, rgi_widget)

        # Перерисовка графа
        graph = Graph(node_size=1000)

        graph_data = self.model.graph if self.model.show_graph_as == ShowGraphAs.FULL_GRAPH else self.model.visited_path

        for branch in graph_data:
            graph.add_edge(
                f'{branch["from_node"]}[{self.model.distance[branch["from_node"]]}]',
                f'{branch["to_node"]}[{self.model.distance[branch["to_node"]]}]',
                branch["weight"]
            )

        if graph_data:
            if self.model.vertex_in_graph(self.model.start_vertex):
                graph.style_node(
                    f'{self.model.start_vertex}[{self.model.distance[self.model.start_vertex]}]',
                    node_color='aquamarine',
                    node_size=1000
                )

            if self.model.vertex_in_graph(self.model.search_vertex) and self.model.is_found:
                graph.style_node(
                    f'{self.model.search_vertex}[{self.model.distance[self.model.search_vertex]}]',
                    node_color='red',
                    node_size=1000
                )

        graph.canvas().figure.clf()
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
            self.ui.searchTime.setText(f"{round(self.model.search_time, 6)} мс.")

        # Результат
        if self.model.is_found:
            self.ui.minValue.setText(str(self.model.short_value))

        # Путь
        if self.model.is_found:
            self.ui.shortPath.setText(" -> ".join(
                [str(el["from_node"]) for el in self.model.visited_path] + [str(self.model.search_vertex)])
            )
