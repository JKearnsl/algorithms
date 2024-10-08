from src.model.enum.graph import ShowGraphAs
from src.model.enum.problem import AlgorithmType
from src.model.fsp.mst import kruskal_algorithm


class MSTModel:

    def __init__(self):
        self._graph = []

        self._algorithm_type: AlgorithmType = AlgorithmType.KMT
        self._show_graph_as: ShowGraphAs = ShowGraphAs.FULL_GRAPH
        self._start_vertex = None
        self._is_found = False

        self._search_time = None
        self._visited_path = []
        self._short_value = None
        self._distance = []

        # список наблюдателей
        self._mObservers = []

    @property
    def graph(self):
        return self._graph

    @property
    def is_found(self):
        return self._is_found

    @property
    def search_time(self):
        return self._search_time

    @property
    def algorithm_type(self) -> AlgorithmType:
        return self._algorithm_type

    @property
    def search_vertex(self):
        return self._search_vertex

    @property
    def show_graph_as(self):
        return self._show_graph_as

    @property
    def start_vertex(self):
        return self._start_vertex

    @property
    def visited_path(self):
        return self._visited_path

    @property
    def short_value(self):
        return self._short_value

    @property
    def distance(self):
        return self._distance

    def solve(self):
        if self._graph is None:
            return None

        if not self.vertex_in_graph(self._start_vertex):
            start_vertex = None
        else:
            start_vertex = self._start_vertex

        self._is_found = False
        self._search_time = None
        self._short_value = None
        self._visited_path = []

        if self._algorithm_type == AlgorithmType.KMT:
            self._search_time, self._visited_path = kruskal_algorithm(
                self.graph,
            )

    def add_link(self, from_node: str, to_node: str, weight: int):
        self._graph.append(dict(from_node=from_node, to_node=to_node, weight=weight))
        self.solve()
        self.notify_observers()

    def remove_link(self, index: int = -1):
        if self._graph:
            self._graph.pop(index)
            self.solve()
            self.notify_observers()

    @graph.setter
    def graph(self, value):
        self._graph = value
        self.solve()
        self.notify_observers()

    @algorithm_type.setter
    def algorithm_type(self, value: AlgorithmType):
        self._algorithm_type = value
        self.solve()
        self.notify_observers()

    @show_graph_as.setter
    def show_graph_as(self, value: AlgorithmType):
        self._show_graph_as = value
        self.notify_observers()

    @search_vertex.setter
    def search_vertex(self, value: str):
        self._search_vertex = value
        self.solve()
        self.notify_observers()

    @start_vertex.setter
    def start_vertex(self, value: str):
        self._start_vertex = value
        self.solve()
        self.notify_observers()

    def vertex_in_graph(self, vertex):
        for branch in self._graph:
            if branch['from_node'] == vertex or branch['to_node'] == vertex:
                return True
        return False

    def add_observer(self, observer):
        self._mObservers.append(observer)

    def remove_observer(self, observer):
        self._mObservers.remove(observer)

    def notify_observers(self):
        for observer in self._mObservers:
            observer.model_changed()
