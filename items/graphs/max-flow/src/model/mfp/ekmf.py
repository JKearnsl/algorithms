from src.model.mfp.bfs import bfs_path


def edmonds_karp_max_flow(graph: dict[int, dict[int, int]], source_node: int = None, sink_node: int = None):

    # Пустая матрица текущего потока
    flow_matrix = {}
    for node in graph.keys():
        flow_matrix[node] = {}

    for src_node in graph.keys():
        for dst_node in graph[src_node]:
            flow_matrix[src_node][dst_node] = 0

    # Вычисление минимальной пропускной способности на этом пути и обновление потока в сети
    while True:
        # Поиск пути в ширину для нахождения увеличивающих путей
        path = bfs_path(flow_matrix, graph, source_node, sink_node)

        if path is None:
            break

        flow = min(
            graph[start_node][neighbour] - flow_matrix[start_node][neighbour]
            for start_node, neighbour in path
        )
        for start_node, neighbour in path:
            flow_matrix[start_node][neighbour] += flow
            flow_matrix[neighbour][start_node] -= flow  # todo: реализовать для ОРГ графа

    # Вычисление значения максимального потока путем суммирования потока через все исходящие ребра от исходного узла.
    max_flow_value = sum(flow_matrix[source_node][node] for node in graph.keys())

    # Обработка отрицательных значений потока в flow_matrix, если такие есть.
    for _ in flow_matrix:
        for __ in flow_matrix[_]:
            if flow_matrix[_][__] < 0:
                flow_matrix[_][__] = 0

    return flow_matrix, max_flow_value
