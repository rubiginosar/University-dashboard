from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)
        self.matching = set()

    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def find_maximal_matching(self):
        visited = set()

        for u in range(self.V):
            if u not in visited:
                for v in self.graph[u]:
                    if v not in visited:
                        self.matching.add((u, v))
                        visited.add(u)
                        visited.add(v)
                        break

        return self.matching

    def printVertexCover(self):
        matching = self.find_maximal_matching()
        vertex_cover = set()

        for edge in matching:
            vertex_cover.add(edge[0])
            vertex_cover.add(edge[1])

        print("Vertex Cover (V0):", vertex_cover)

def createGraphFromInput():
    vertices = int(input("Enter the number of vertices: "))
    g = Graph(vertices)
    while True:
        edge_input = input("Enter an edge as 'u v' (or 'done' to finish): ").strip()
        if edge_input.lower() == 'done':
            break
        try:
            u, v = map(int, edge_input.split())
            if u < 0 or u >= vertices or v < 0 or v >= vertices:
                print("Invalid edge! Vertices must be between 0 and", vertices - 1)
                continue
            g.addEdge(u, v)
        except ValueError:
            print("Invalid input format! Please enter two integers separated by a space.")
    return g

# Driver code
graph = createGraphFromInput()
graph.printVertexCover()
