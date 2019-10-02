"""Showing that the graph K_{4, 3} can be embedded in R^4."""
import numpy as np
import networkx as nx
from sgvd.construct import from_positive_subgraph
from sgvd.validate import is_valid_embedded

graph = from_positive_subgraph(nx.algorithms.bipartite.generators.complete_bipartite_graph(4, 3))

graph.nodes[0]['embedding'] = (1, 1, 0, 0)
graph.nodes[1]['embedding'] = (-1, 1, 0, 0)
graph.nodes[2]['embedding'] = (1, -1, 0, 0)
graph.nodes[3]['embedding'] = (-1, -1, 0, 0)

graph.nodes[4]['embedding'] = (0, 0, np.sqrt(2)-1/8, -1/4)
graph.nodes[5]['embedding'] = (0, 0, -np.sqrt(2)+1/8, -1/4)
graph.nodes[6]['embedding'] = (0, 0, 0, np.sqrt(2)-1/8)

# expected result: True
print(is_valid_embedded(graph, 4))

another_embedding = [
    (2.8507385, 6.1482606, -2.3753448, 2.518072),
    (-2.9618878, -1.0120164, -7.4049244, -2.3642173),
    (0.18204233, -0.49255607, 7.442692, 4.149554),
    (-2.2062209, -8.0445595, 1.9426373, -2.561302),
    (-2.6976945, 2.734865, 2.9277918, -4.66719),
    (-5.018606, -1.5530125, -2.568531, 5.059862),
    (5.4571576, -1.6337873, -1.3643979, 0.5478879)
]

for i in range(7):
    graph.nodes[i]['embedding'] = another_embedding[i]

# expected result: True
print(is_valid_embedded(graph, 4))
