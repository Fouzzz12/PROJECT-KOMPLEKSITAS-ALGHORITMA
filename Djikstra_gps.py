import heapq
import math
import networkx as nx
import matplotlib.pyplot as plt

def euclidean(a, b):
    (x1, y1), (x2, y2) = a, b
    return math.hypot(x2 - x1, y2 - y1)

class Graph:
    def __init__(self):
        self.adj = {}

    def add_node(self, node):
        if node not in self.adj:
            self.adj[node] = []

    def add_edge(self, u, v, w, bidirectional=True):
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append((v, w))
        if bidirectional:
            self.adj[v].append((u, w))

    def neighbors(self, node):
        return self.adj[node]


def djikstra(graph, start):
    dist = {node: math.inf for node in graph.adj}
    prev = {node: None for node in graph.adj}

    dist[start] = 0
    heap = [(0, start)]

    while heap:
        d, u = heapq.heappop(heap)

        for v, w in graph.neighbors(u):
            alt = d + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(heap, (alt, v))

    return dist, prev

def reconstruct_path(prev, start, target):
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path

def build_sample_graph():
    coords = {
        'SUKABUMI': (101, 9),
        'CIANJUR': (107, 1),
        'BOGOR': (103, 8),
        'BANDUNG': (110, 6),
        'JAKARTA': (105, 8)

    }

    g = Graph()
    speed_kmh = 60.0

    def add_road(u, v, speed_factor=1.0):
        dist_km = euclidean(coords[u], coords[v])
        travel_time_hours = dist_km / (speed_kmh * speed_factor)
        travel_time_min = travel_time_hours * 60
        g.add_edge(u, v, travel_time_min)

    add_road('SUKABUMI', 'CIANJUR')
    add_road('CIANJUR', 'BOGOR')
    add_road('BOGOR', 'JAKARTA')
    add_road('CIANJUR', 'BANDUNG')
    add_road('BANDUNG', 'JAKARTA')
    add_road('BOGOR', 'BANDUNG')
    add_road('SUKABUMI', 'BOGOR')

    return g, coords

def draw_graph(coords, graph, path):
    NX = nx.Graph()

    for node in coords:
        NX.add_node(node, pos=coords[node])

    for u in graph.adj:
        for v, w in graph.adj[u]:
            if not NX.has_edge(u, v):
                NX.add_edge(u, v)

    pos = nx.get_node_attributes(NX, 'pos')

    plt.figure(figsize=(8, 6))
    nx.draw(NX, pos, with_labels=True, node_size=800)


    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(
            NX, pos,
            edgelist=path_edges,
            width=3,
            edge_color='green'
        )

    plt.title("Rute Tercepat dengan Algoritma Djikstra")
    plt.show()
    plt.figure(figsize=(8, 6))
    nx.draw(NX, pos, with_labels=True, node_size=800)

    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(NX, pos, edgelist=path_edges, width=3, edge_color='red')

    edge_labels = nx.get_edge_attributes(NX, 'weight')
    nx.draw_networkx_edge_labels(NX, pos, edge_labels=edge_labels)

    plt.title("Rute Tercepat dengan Algoritma Djikstra")
    plt.show()

def main():
    g, coords = build_sample_graph()

    start = input("Masukkan titik awal: ").upper()
    target = input("Masukkan titik tujuan: ").upper()

    dist, prev = djikstra(g, start)
    path = reconstruct_path(prev, start, target)

    print("\nRute tercepat:")
    print(" -> ".join(path))
    print(f"Perkiraan waktu: {dist[target]:.2f} Menit")

    draw_graph(coords, g, path)


if __name__ == "__main__":
    main()