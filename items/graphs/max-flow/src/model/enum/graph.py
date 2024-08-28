from enum import Enum


class GraphType(Enum):
    DIRECTED = "ОРГ"
    UNDIRECTED = "НеОРГ"


class ShowAs(Enum):
    FULL_GRAPH = "Исходный граф"
    NETWORK = "Сеть"
