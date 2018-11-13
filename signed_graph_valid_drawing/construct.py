import networkx as nx


def from_positive_subgraph(positive_graph):
    negative_graph = nx.algorithms.operators.unary.complement(positive_graph)
    graph = nx.Graph()
    graph.add_nodes_from(positive_graph.nodes)
    graph.add_edges_from(positive_graph.edges, sign=1)
    graph.add_edges_from(negative_graph.edges, sign=-1)
    return graph
