class GraphBox:

    def __init__(self, graph_links: list[dict[int: int]], source: int = None, target: int = None):
        self.graph_links = graph_links
        self.source = source
        self.target = target
