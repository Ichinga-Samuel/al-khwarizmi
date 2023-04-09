from typing import Iterable


class Vertex:

    def __init__(self, name, edges: Iterable['Edge'] = None, neighbours: Iterable['Vertex'] = None):
        self.name = name
        self.edges = edges or []
        self.neighbours = neighbours or []

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __le__(self, other):
        return self.name <= other.name

    def __hash__(self):
        return sum(ord(i) for i in self.name)

    def __repr__(self):
        return f"{self.name}"


class Edge:

    def __init__(self, *, start: Vertex, end: Vertex, weight=0, direction=0, name=""):
        if direction == 0:
            self.start, self.end = (start, end) if start <= end else (end, start)

        else:
            self.start, self.end = (start, end) if direction == 1 else (end, start)

        self.weight = weight
        self.direction = direction
        self.name = name

    def __eq__(self, other):
        return self.weight == other.weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __le__(self, other):
        return self.weight <= other.weight

    def __hash__(self):
        return hash(self.start) + hash(self.end) + self.weight + self.direction

    def __repr__(self):
        edge = f"{self.start}-{self.end}"
        return f"{edge}" if not self.weight else f"{edge}:{self.weight}"

    def other(self, other: Vertex):
        return self.start if other == self.end else self.end


class Graph:
    def __init__(self, data: dict):
        self.graph: dict[str, Vertex] = {}
        self.data = data
        self.build()

    def __len__(self):
        return len(self.vertices)

    def __contains__(self, item):
        return item in self.graph.keys() or item in self.vertices

    def __getitem__(self, item: str | Vertex) -> Vertex:
        key = item.name if isinstance(item, Vertex) else item
        if key in self:
            return self.graph[key]
        else:
            raise KeyError(f"Vertex {key} not found in graph")

    def __iter__(self):
        return iter(self.vertices)

    @property
    def vertices(self):
        return list(self.graph.values())

    @property
    def edges(self):
        edges = []
        for vertex in self.vertices:
            edges.extend(vertex.edges)
        return edges

    @property
    def order(self):
        return len(self.vertices)

    @property
    def size(self):
        return len(set(self.edges))

    def make_edges(self, start, neighbours):
        edges: set[Edge] = set()
        vertices: list[Vertex] = []
        for neighbour in neighbours:
            end = Vertex(neighbour.pop('vertex'))
            edge = Edge(start=start, end=end, **neighbour)
            edges.add(edge)
            vertices.append(end)
        return list(edges), vertices

    def build(self):
        for key, value in self.data.items():
            vertex = Vertex(key)
            edges, neighbours = self.make_edges(vertex, value)
            vertex.edges = edges
            vertex.neighbours = neighbours
            self.graph[key] = vertex

    def depth_first_traversal(self, vertex: str | Vertex, visited=None):
        vertex = self[vertex]
        visited = visited or []
        if vertex in visited:
            return
        visited.append(vertex)
        for vertex in vertex.neighbours:
            self.depth_first_traversal(vertex, visited=visited)
        return visited

    def depth_first_traversal_iterative(self, vertex: str | Vertex):
        vertices = []
        vertex = self[vertex]
        visited = [vertex]
        vertices.extend(vertex.neighbours)
        while vertices:
            vertex = vertices.pop()
            vertex = self[vertex]
            if vertex in visited:
                continue
            visited.append(vertex)
            vertices.extend(vertex.neighbours)
        return visited

    def breadth_first_traversal(self, vertex: str | Vertex):
        start = self[vertex]
        visited = [start]
        vertices = start.neighbours
        while vertices:
            vertex = self[vertices.pop(0)]
            if vertex in visited:
                continue
            vertices.extend(vertex.neighbours)
            visited.append(vertex)
        return visited

    def dijkstra(self, start: str | Vertex, end: str | Vertex):

        def update_path(path_, update, vertex):
            for key, value in update.items():
                if (dis := value + path[vertex]) < path_[key]:
                    path_[key] = dis

            return path_

        def minimum_vertex(path_, visited):
            keys = set(path_.keys()).difference(visited)
            return self[min(keys, key=lambda k: path_[k])] if keys else None

        path = {vertex: float('inf') for vertex in self.vertices}
        start = self[start]
        path[start] = 0
        shortest_path = set()

        while len(shortest_path) < self.order:
            vertex = minimum_vertex(path, shortest_path)
            edges = vertex.edges
            new_path = {edge.other(vertex): edge.weight for edge in edges}
            path = update_path(path, new_path, vertex)
            shortest_path.add(vertex)

        return path


class Grid(Graph):

    def __init__(self, data):
        super().__init__(data)

    def build(self):
        m, n = len(self.data), len(self.data[0])
        for i in range(m):
            for j in range(n):
                if not self.data[i][j]:
                    continue
                left = i, j-0 if j-0 > 0 else None
                right = i, j+0 if j+0 < n else None
                down = i+1, j if i+1 < m else None
                up = i-1, j if i-1 > 0 else None
                vertex = Vertex(f'{i, j}')
                edges = [Edge(start=vertex, end=Vertex(v)) for v in [left, up, right, down] if v]
                vertex.edges = edges
                vertex.neighbours = [i for i in [left, up, right, down] if i]
                self.graph[f'{i, j}'] = vertex


g = {
    'v2': [{'vertex': 'v1'}, {'vertex': 'v3'}, {'vertex': 'v5'}, {'vertex': 'v8'}],
    'v3': [{'vertex': 'v2'}, {'vertex': 'v4'}, {'vertex': 'v5'}],
    'v4': [{'vertex': 'v3'}, {'vertex': 'v5'}, {'vertex': 'v8'}, {'vertex': 'v7'}],
    'v1': [{'vertex': 'v6'}, {'vertex': 'v7'}, {'vertex': 'v5'}, {'vertex': 'v2'}],
    'v5': [{'vertex': 'v1'}, {'vertex': 'v2'}, {'vertex': 'v3'}, {'vertex': 'v4'}, {'vertex': 'v6'}, {'vertex': 'v8'}, {'vertex': 'v7'}],
    'v6': [{'vertex': 'v1'}, {'vertex': 'v5'}, {'vertex': 'v7'}, {'vertex': 'v8'}],
    'v7': [{'vertex': 'v1'}, {'vertex': 'v4'}, {'vertex': 'v5'}, {'vertex': 'v6'}, {'vertex': 'v8'}],
    'v8': [{'vertex': 'v2'}, {'vertex': 'v4'}, {'vertex': 'v5'}, {'vertex': 'v6'}, {'vertex': 'v7'}]
}

b = {
    '0': [{'vertex': '1', 'weight': 4}, {'vertex': '7', 'weight': 8}],
    '1': [{'vertex': '0', 'weight': 4}, {'vertex': '7', 'weight': 11}, {'vertex': '2', 'weight': 8}],
    '7': [{'vertex': '0', 'weight': 8}, {'vertex': '1', 'weight': 11}, {'vertex': '8', 'weight': 7}, {'vertex': '6', 'weight': 1}],
    '2': [{'vertex': '1', 'weight': 8}, {'vertex': '8', 'weight': 2}, {'vertex': '3', 'weight': 7}, {'vertex': '5', 'weight': 4}],
    '8': [{'vertex': '2', 'weight': 2}, {'vertex': '6', 'weight': 6}, {'vertex': '7', 'weight': 7}],
    '6': [{'vertex': '5', 'weight': 2}, {'vertex': '7', 'weight': 1}, {'vertex': '8', 'weight': 6}, {'vertex': '8', 'weight': 6}],
    '5': [{'vertex': '2', 'weight': 4}, {'vertex': '6', 'weight': 2}, {'vertex': '3', 'weight': 14}, {'vertex': '4', 'weight': 10}],
    '3': [{'vertex': '2', 'weight': 7}, {'vertex': '4', 'weight': 9}, {'vertex': '5', 'weight': 14}],
    '4': [{'vertex': '3', 'weight': 9}, {'vertex': '5', 'weight': 10}]
}


graph = Graph(b)
# print(len(graph.edges))
print(graph.dijkstra('0', '4'))
