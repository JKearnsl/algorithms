from enum import Enum


class GraphType(Enum):
    DIRECTED = "ОРГ"
    UNDIRECTED = "НеОРГ"


class ShowAs(Enum):
    FULL_GRAPH = "Исходный граф"
    VISITED_PATH = "Пройденный путь"
