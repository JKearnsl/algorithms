import time


def kruskal_algorithm(graph):
    UT = []
    ftr = {}
    rnk = {}

    def find(i):
        if i != ftr[i]:
            ftr[i] = find(ftr[i])
        return ftr[i]

    def union(r, s):
        if rnk[r] >= rnk[s]:
            ftr[s] = r
            if rnk[r] == rnk[s]:
                rnk[r] += 1
        else:
            ftr[r] = s

    start_time = time.time()

    for edge in graph:
        from_node = edge["from_node"]
        to_node = edge["to_node"]
        ftr[from_node] = from_node
        ftr[to_node] = to_node
        rnk[from_node] = 0
        rnk[to_node] = 0

    graph = sorted(graph, key=lambda x: x["weight"])  # Сортировка ребер по весам

    for edge in graph:
        from_node = edge["from_node"]
        to_node = edge["to_node"]
        if find(from_node) != find(to_node):
            UT.append(dict(from_node=from_node, to_node=to_node, weight=edge["weight"]))
            union(find(from_node), find(to_node))

    end_time = time.time()
    delta_time = (end_time - start_time) * 1000

    return delta_time, UT
