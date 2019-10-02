import networkx as nx
from sgvd.construct import from_positive_subgraph
from sgvd.embed import find_embedding

MAX_K = 10
DIMENSION_BY_K = {
    4: 5,
    5: 7,
    6: 8,
    7: 10,
    8: 11,
    9: 13,
    10: 14,
}

for k in [10]:
    signed_graph = from_positive_subgraph(
        nx.algorithms.bipartite.generators.complete_bipartite_graph(k, k)
    )

    # attempt to improve the dimension
    dimension = DIMENSION_BY_K[k] - 1

    # more trials for larger k
    for _ in range(3*k):
        # more steps for larger k
        result = find_embedding(
            signed_graph,
            dimension,
            max_steps=k*2000
        )
        print("K_%s,%s in Dimension %s: Objective %s" % (k, k, dimension, result))
        if result == 0.0:
            break
