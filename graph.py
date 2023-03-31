from functools import cached_property, cache


class Vertex:

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __le__(self, other):
        return self.name < other.name

    def __hash__(self):
        return sum(ord(i) for i in self.name)

    def __repr__(self):
        return f"{self.name}"


class Edge:

    def __init__(self, start: Vertex, end: Vertex, weight=0, direction=0):
        if direction == 0:
            self.start, self.end = (start, end) if start <= end else (end, start)

        else:
            self.start, self.end = (start, end) if direction == 1 else (end, start)

        self.weight = weight
        self.direction = direction

    def __eq__(self, other):
        return (self.start, self.end, self.weight,
                self.direction) == (other.start, other.end, other.weight,
                                    other.direction)

    def __hash__(self):
        return hash(self.start) + hash(self.end) + self.weight + self.direction

    def __repr__(self):
        edge = f"{self.start}-{self.end}"
        return f"{edge}" if not self.weight else f"{edge}:{self.weight}"


class Graph:

    def __init__(self, data: dict):
        self.graph = {}
        self.data = data
        self.build()

    def make_edges(self, vertex, neighbours):
        return [Edge(vertex, Vertex(neighbour), **props) for neighbour, props in neighbours.items()]

    def build(self):
        for key, value in self.data.items():
            vertex = Vertex(key)
            self.graph[vertex] = self.make_edges(vertex, value)

    @property
    def vertices(self):
        return list(self.graph.keys())

    @property
    def edges(self):
        edges = set()
        for edge in self.graph.values():
            edges.update(edge)
        return edges

    @cache
    def degree_sequence(self):
        ds = [len(value) for value in self.graph.values()]
        print('gh')
        return ds


g = {
    'v1': {'v2': {}, 'v5': {}, 'v6': {}, 'v7': {}},
    'v2': {'v1': {}, 'v3': {}, 'v5': {}, 'v8': {}},
    'v3': {'v2': {}, 'v4': {}, 'v5': {}},
    'v4': {'v3': {}, 'v5': {}, 'v7': {}, 'v8': {}},
    'v5': {'v1': {}, 'v2': {}, 'v3': {}, 'v4': {}, 'v6': {}, 'v7': {}, 'v8': {}},
    'v6': {'v1': {}, 'v5': {}, 'v7': {}, 'v8': {}},
    'v7': {'v1': {}, 'v4': {}, 'v5': {}, 'v6': {}, 'v8': {}},
    'v8': {'v2': {}, 'v4': {}, 'v5': {}, 'v6': {}, 'v7': {}}
}

graph = Graph(g)
print(len(graph.edges))
