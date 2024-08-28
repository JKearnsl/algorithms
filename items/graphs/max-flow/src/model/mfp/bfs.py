from queue import Queue


def bfs_path(
        flow_matrix: dict[int, dict[int, int]],
        graph: dict[int, dict[int, int]],
        start_node: int,
        end_node: int
) -> list[tuple[int, int]] | None:

    queue = Queue()
    queue.put(start_node)
    paths = {start_node: []}

    if start_node == end_node:
        return paths[start_node]

    while not queue.empty():
        source_node = queue.get()
        for neighbour in graph[source_node]:
            if neighbour not in paths and graph[source_node][neighbour] - flow_matrix[source_node][neighbour] > 0:
                paths[neighbour] = paths[source_node] + [(source_node, neighbour)]
                if neighbour == end_node:
                    return paths[neighbour]
                queue.put(neighbour)
    return None
