from src.model.enum.graph import GraphType, ShowAs
from src.model.enum.algorithm import AlgType
from src.model.mfp.ekmf import edmonds_karp_max_flow
from src.model.mfp.graphbox import GraphBox
from src.utils.file import load_obj_from_file, save_obj_to_file


class MFPModel:

    def __init__(self):
        self._graph = []
        self._flow_network = {}
        self._source = None
        self._target = None
        self._max_flow = None
        self._alg = AlgType.EK
        self._graph_type = GraphType.DIRECTED
        self._show_graph_as = ShowAs.FULL_GRAPH

        # список наблюдателей
        self._mObservers = []

    def solve(self) -> None:
        vertices = self.graph.keys()

        if self._source is None or self._target is None:
            return None
        else:
            if self._source not in vertices or self._target not in vertices:
                return None

            if self._source == self._target:
                return None

        self._flow_network, self._max_flow = edmonds_karp_max_flow(self.graph, self._source, self._target)

    @property
    def graph(self) -> dict[int, dict[int, int]]:
        graph = {}
        for link in self._graph:
            _from = link['from_node']
            _to = link['to_node']
            graph[_from] = graph.get(_from, {})
            graph[_to] = graph.get(_to, {})
            graph[_from][_to] = link['weight']

        return dict(sorted(graph.items(), key=lambda item: item[0]))

    @property
    def graph_links(self) -> list[dict[str, int]]:
        return self._graph

    @property
    def flow_network(self) -> dict[int: dict[int: int]]:
        return self._flow_network

    @property
    def source(self) -> int | None:
        return self._source

    @property
    def target(self) -> int | None:
        return self._target

    @property
    def alg(self) -> AlgType:
        return self._alg

    @property
    def graph_type(self) -> GraphType:
        return self._graph_type

    @property
    def show_graph_as(self) -> ShowAs:
        return self._show_graph_as

    @property
    def max_flow(self) -> int | None:
        return self._max_flow

    @show_graph_as.setter
    def show_graph_as(self, value: ShowAs):
        self._show_graph_as = value
        self.notify_observers()

    @graph_type.setter
    def graph_type(self, value: GraphType):
        self._graph_type = value
        self.solve()
        self.notify_observers()

    @alg.setter
    def alg(self, value: AlgType):
        self._alg = value
        self.solve()
        self.notify_observers()

    @target.setter
    def target(self, value: int | None):
        if value:
            if self._target == value:
                return
            else:
                try:
                    value = int(value)
                except ValueError:
                    return

        self._target = value
        self.solve()
        self.notify_observers()

    @source.setter
    def source(self, value: int | None):
        if value:
            if self._source == value:
                return
            else:
                try:
                    value = int(value)
                except ValueError:
                    return

        self._source = value
        self.solve()
        self.notify_observers()

    def add_link(self, from_node: int, to_node: int, weight: int):
        self._graph.append(dict(from_node=from_node, to_node=to_node, weight=weight))
        self.solve()
        self.notify_observers()

    def edit_link(self, index: int, from_node: int, to_node: int, weight: int):
        self._graph[index] = dict(from_node=from_node, to_node=to_node, weight=weight)
        self.solve()
        self.notify_observers()

    def remove_link(self, index: int = -1):
        if self._graph:
            self._graph.pop(index)
            self.solve()
            self.notify_observers()

    def clear(self):
        self._graph.clear()
        self._flow_network.clear()
        self._source = None
        self._target = None
        self.notify_observers()

    def load_file(self, file_name: str) -> bool:
        graph_box: GraphBox = load_obj_from_file(file_name)
        if isinstance(graph_box, GraphBox) is False:
            return False

        self.clear()
        self._source = graph_box.source
        self._target = graph_box.target
        self._graph = graph_box.graph_links
        self.solve()
        self.notify_observers()
        return True

    def save_file(self, file_name: str) -> (bool, str):
        graph_box = GraphBox(self._graph, self._source, self._target)
        try:
            save_obj_to_file(graph_box, file_name)
        except FileExistsError:
            return False, 'Файл уже существует'
        except FileNotFoundError:
            return False, 'Неверный путь'
        except PermissionError:
            return False, 'Нет доступа к файлу'
        except OSError:
            return False, 'Ошибка ввода/вывода'
        return True, 'OK'

    def add_observer(self, observer):
        self._mObservers.append(observer)

    def remove_observer(self, observer):
        self._mObservers.remove(observer)

    def notify_observers(self):
        for observer in self._mObservers:
            observer.model_changed()
