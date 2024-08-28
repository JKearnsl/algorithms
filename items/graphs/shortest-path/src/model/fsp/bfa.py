import time


def bellman_ford_algorithm(graph: dict[str: dict[str: int]], source: str, search_node: str = None):
    distance = {}
    predecessor = {}

    start_time = time.time()
    for node in graph:
        distance[node] = float('inf')
        predecessor[node] = None
    distance[source] = 0

    for node in graph:
        for neighbour in graph[node]:
            new_distance = distance[node] + graph[node][neighbour]
            if new_distance < distance[neighbour]:
                distance[neighbour] = new_distance
                predecessor[neighbour] = node

    end_time = time.time()
    delta_time = (end_time - start_time) * 1000

    for node in graph:
        for neighbour in graph[node]:
            if distance[node] + graph[node][neighbour] < distance[neighbour]:
                return delta_time, None, [], distance

    if search_node is not None:
        path = []
        node = search_node
        while node is not None:
            path.insert(0, node)
            node = predecessor[node]
        if distance[search_node] != float('inf'):
            return delta_time, distance[search_node], path, distance

    return delta_time, None, [], distance
