class BellmanFordAlgorithm:
    INFINITY = float("Inf")

    class Edge:
        vertex_u: int
        vertex_v: int
        weight: int

    @staticmethod
    def execute(
            vertex_count: int,
            edges: list[Edge],
            start_edge_index,
            is_allow_negative_cycles: bool = True,
    ) -> (list[int], list[int|None]):
        distances = [BellmanFordAlgorithm.INFINITY] * vertex_count
        predecessors = [None] * vertex_count
        distances[start_edge_index] = 0

        for i in range(vertex_count - 1):

            is_updated = False

            for edge in edges:
                u, v, w = edge.vertex_u, edge.vertex_v, edge.weight
                if distances[u] != BellmanFordAlgorithm.INFINITY and distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
                    predecessors[v] = u
                    is_updated = True

            if not is_updated:
                break

        if BellmanFordAlgorithm.__edges_has_negative_weight_cycle(edges, distances):
            if not is_allow_negative_cycles:
                raise Exception("Negative cycle detected")

            print("Graph contains negative weight cycle!")

        return distances, predecessors

    @staticmethod
    def show_path(
            source_index: int,
            target_index: int,
            distances: list[int],
            predecessors: list[int|None]
    ) -> None:
        if distances[target_index] == BellmanFordAlgorithm.INFINITY:
            print(f"path from vertex {source_index} to vertex {target_index} is not exists!")

        path = []
        current = target_index
        visited_count = 0
        vertex_count = len(predecessors)

        while current is not None:
            path.append(current)
            current = predecessors[current]
            visited_count += 1

            if visited_count > vertex_count:
                print("Detected a loop in path reconstruction, possibly due to a negative cycle!")
                break

        path.reverse()

        print(path)

    @staticmethod
    def __edges_has_negative_weight_cycle(edges: list[Edge], distances: list[int]) -> bool:
        for edge in edges:
            u, v, w = edge.vertex_u, edge.vertex_v, edge.weight
            if distances[u] != BellmanFordAlgorithm.INFINITY and distances[u] + w < distances[v]:
                return True
        return False

    @staticmethod
    def convert_matrix_to_edges(matrix: list[list[int]]) -> list[Edge]:
        edges = []
        vertex_count = len(matrix)

        for u in range(vertex_count):
            for v in range(vertex_count):
                weight = matrix[u][v]
                if weight != BellmanFordAlgorithm.INFINITY:
                    edge = BellmanFordAlgorithm.Edge()
                    edge.vertex_u = u
                    edge.vertex_v = v
                    edge.weight = weight
                    edges.append(edge)

        return edges

INF = BellmanFordAlgorithm.INFINITY

# adjacency_matrix = [
#     [0, 6, INF, INF, 7],
#     [INF, 0, 5, -4, 8],
#     [INF, -2, 0, INF, INF],
#     [2, INF, 7, 0, INF],
#     [INF, INF, -3, 9, 0]
# ]

adjacency_matrix = [
    [0, 1, INF],
    [INF, 0, -1],
    [-1, INF, 0]
]


edges = BellmanFordAlgorithm.convert_matrix_to_edges(adjacency_matrix)

vertex_count = len(adjacency_matrix)

distances, predecessors = BellmanFordAlgorithm.execute(vertex_count, edges, start_edge_index=0)

print("Расстояния:", distances)
print("Предшественники:", predecessors)

BellmanFordAlgorithm.show_path(0, 2, distances, predecessors)
