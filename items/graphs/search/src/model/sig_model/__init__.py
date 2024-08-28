from collections import OrderedDict

from src.model.enum.graph import GraphType, ShowAs
from src.model.enum.problem import ProblemType
from src.model.sig_model.dfs import dfs


class SIGModel:

    def __init__(self):
        self._graph_links = []
        self._graph_type: GraphType = GraphType.DIRECTED
        self._problem_type: ProblemType = ProblemType.DFS
        self._show_as: ShowAs = ShowAs.FULL_GRAPH
        self._search_time = None
        self._visited_path = []
        self._search_value = None
        self._start_vertex = None
        self._is_found = False

        # список наблюдателей
        self._mObservers = []

    @property
    def graph_links(self):
        return self._graph_links

    @property
    def visited_path(self):
        return self._visited_path

    @property
    def start_vertex(self):
        return self._start_vertex

    @property
    def show_as(self):
        return self._show_as

    @property
    def graph_type(self) -> GraphType:
        return self._graph_type

    @property
    def search_time(self):
        return self._search_time

    @property
    def problem_type(self) -> ProblemType:
        return self._problem_type

    @property
    def search_value(self):
        return self._search_value

    @property
    def is_found(self):
        return self._is_found

    def add_link(self, from_node: str, to_node: str):
        self.graph_links.append((from_node, to_node))
        self.solve()
        self.notify_observers()

    def remove_link(self, index: int = -1):
        if self.graph_links:
            self.graph_links.pop(index)
            self.solve()
            self.notify_observers()

    def solve(self):
        self._is_found, self._search_time, self._visited_path = dfs(
            self.graph_links, self.start_vertex, self._search_value, self.graph_type
        )

    def graph_table(self):
        if self._graph_links is None:
            return None, None

        vertices = list(OrderedDict.fromkeys([vertex for link in self._graph_links for vertex in link]))
        table: list[list[str]] = [["-"] * len(vertices) for _ in range(len(vertices))]

        for i in range(len(vertices)):
            for j in range(len(vertices)):
                if (vertices[i], vertices[j]) in self.graph_links:
                    table[i][j] = "+"
                    if self._graph_type == GraphType.UNDIRECTED:
                        table[j][i] = "+"
        return table, vertices

    @graph_type.setter
    def graph_type(self, value: GraphType):
        self._graph_type = value
        self.solve()
        self.notify_observers()

    @problem_type.setter
    def problem_type(self, value: ProblemType):
        self._problem_type = value
        self.solve()
        self.notify_observers()

    @search_value.setter
    def search_value(self, value: int):
        self._search_value = value
        self.solve()
        self.notify_observers()

    @show_as.setter
    def show_as(self, value):
        self._show_as = value
        self.notify_observers()

    @start_vertex.setter
    def start_vertex(self, value):
        self._start_vertex = value
        self.solve()
        self.notify_observers()

    @graph_links.setter
    def graph_links(self, value):
        self._graph_links = value
        self.solve()
        self.notify_observers()

    def add_observer(self, observer):
        self._mObservers.append(observer)

    def remove_observer(self, observer):
        self._mObservers.remove(observer)

    def notify_observers(self):
        for observer in self._mObservers:
            observer.model_changed()
