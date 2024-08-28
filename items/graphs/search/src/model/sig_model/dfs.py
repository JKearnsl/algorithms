import time

from src.model.enum.graph import GraphType


def dfs(graph: list[tuple], start_vertex, search_value, graph_type: GraphType = GraphType.DIRECTED):
    """
    Поиск в глубину
    :param graph_type:
    :param graph:
    :param start_vertex:
    :param search_value:
    :return:
    """

    visited = []
    visited_path = []
    stack = [(None, start_vertex)]
    is_found = False

    start_time = time.time()
    while stack:
        pre_vertex, cur_vertex = stack.pop()
        if cur_vertex not in visited:
            visited.append(cur_vertex)

            if pre_vertex is not None:
                visited_path.append((pre_vertex, cur_vertex))

            if graph_type == GraphType.DIRECTED:
                directions = [x[1] for x in graph if x[0] == cur_vertex]
            else:
                directions = []
                for x in graph:
                    if x[0] == cur_vertex:
                        directions.append(x[1])
                    elif x[1] == cur_vertex and x[0] not in visited:
                        directions.append(x[0])

            stack.extend([(cur_vertex, x) for x in directions])

        if cur_vertex == search_value:
            is_found = True
            break
    end_time = time.time()

    return is_found, (end_time - start_time) * 1000, visited_path
