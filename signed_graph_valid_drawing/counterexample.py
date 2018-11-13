import numpy as np
import networkx as nx
from signed_graph_valid_drawing.construct import from_positive_subgraph
from signed_graph_valid_drawing.validate import is_valid_embedded

graph = from_positive_subgraph(nx.algorithms.bipartite.generators.complete_bipartite_graph(4, 3))

graph.nodes[0]['embedding'] = (1, 1, 0, 0)
graph.nodes[1]['embedding'] = (-1, 1, 0, 0)
graph.nodes[2]['embedding'] = (1, -1, 0, 0)
graph.nodes[3]['embedding'] = (-1, -1, 0, 0)

graph.nodes[4]['embedding'] = (0, 0, np.sqrt(2)-1/8, -1/4)
graph.nodes[5]['embedding'] = (0, 0, -np.sqrt(2)+1/8, -1/4)
graph.nodes[6]['embedding'] = (0, 0, 0, np.sqrt(2)-1/8)

print(is_valid_embedded(graph, 4))
