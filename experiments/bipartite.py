import networkx as nx
from sgvd.construct import from_positive_subgraph
from sgvd.embed import find_embedding

K = 5
DIMENSION = 6
TRIALS = 10

signed_graph = from_positive_subgraph(nx.algorithms.bipartite.generators.complete_bipartite_graph(K, K))

for _ in range(TRIALS):
    result = find_embedding(signed_graph, DIMENSION)
    print(result)
    if result == 0.0:
        break
