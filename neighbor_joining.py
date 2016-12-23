from networkx import *
from matplotlib import pyplot
g = Graph()
g.add_nodes_from(["A", "B", "C", "D", "E"])
g.add_edge("A", "B", weight=10)
g.add_edge("A", "C", weight=12)
g.add_edge("A", "D", weight=8)
g.add_edge("A", "E", weight=7)
g.add_edge("B", "C", weight=4)
g.add_edge("B", "D", weight=4)
g.add_edge("B", "E", weight=14)
g.add_edge("C", "D", weight=6)
g.add_edge("C", "E", weight=16)
g.add_edge("D", "E", weight=12)
cluster = Graph()
while g.number_of_nodes() > 2:
    node_number = g.number_of_nodes()
    if node_number == 2:
        node_numer = 3
    avg_dist = {}
    for node in g.nodes_iter():
        avg = 0
        for neighbor in g.neighbors_iter(node):
            avg += g.get_edge_data(node, neighbor, default=-1000)['weight']
        avg_dist[node] = avg / (node_number - 2)
    min_dist = 1000
    for edge in g.edges_iter(data='weight'):
        x = edge[2] - avg_dist[edge[0]] - avg_dist[edge[1]]
        if x <= min_dist:
            if x == min_dist:
                if len(node1) + len(node2) < len(edge[0]) + len(edge[1]):
                    continue
            node1 = edge[0]
            node2 = edge[1]
            w = edge[2]
            min_dist = x
    new_node = node1 + node2
    new_edges = []
    for node in g.nodes_iter():
        if (node is not node1) & (node is not node2):
            d = g.get_edge_data(node, node1)['weight'] + g.get_edge_data(node, node2)['weight'] - w
            new_edges.append((node, new_node, d / 2))
    g.add_node(new_node)
    for edge in new_edges:
        g.add_edge(edge[0], edge[1], weight=edge[2])
    d1 = (w + avg_dist[node1] - avg_dist[node2]) / 2
    d2 = w - d1
    cluster.add_nodes_from([node1, node2, new_node])
    cluster.add_edge(new_node, node1, weight=round(d1, 3))
    cluster.add_edge(new_node, node2, weight=round(d2, 3))
    g.remove_node(node1)
    g.remove_node(node2)
edges = cluster.edges()
weights = [cluster[u][v]['weight'] * 2 for u, v in edges]
cluster.add_edges_from(g.edges(data=True))
labels = {i[0:2]: '${}'.format(i[2]['weight']) for i in cluster.edges(data=True)}
pos = spring_layout(cluster, weight='weight')
draw_networkx(cluster, pos, node_size=1000, font_size=20)
draw_networkx_edge_labels(cluster, pos, edge_labels=labels, width=weights)
draw(g, pos, node_size=100, width=5)
pyplot.show()
