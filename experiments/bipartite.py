import networkx as nx
from sgvd.construct import from_positive_subgraph
from sgvd.embed import find_embedding

DIMENSION_BY_K = {
    4: 5,
    5: 7,
    6: 8,
    7: 10,
    8: 11,
    9: 13,
    10: 14,
    11: 16,
    12: 17,
    13: 20,
    14: 21,
    15: 23,
}
K_TO_TEST = [13, 14, 15]

for k in K_TO_TEST:
    signed_graph = from_positive_subgraph(
        nx.algorithms.bipartite.generators.complete_bipartite_graph(k, k)
    )

    # attempt to improve the dimension
    dimension = DIMENSION_BY_K[k] - 1

    # more trials for larger k?
    for _ in range(100):
        # more steps for larger k
        result = find_embedding(
            signed_graph,
            dimension,
            max_steps=k*100
        )
        print("K_%s,%s in Dimension %s: Objective %s" % (k, k, dimension, result))
        if result == 0.0:
            break
