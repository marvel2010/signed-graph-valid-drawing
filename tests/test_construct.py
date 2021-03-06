import networkx as nx
from sgvd.construct import from_positive_subgraph


def test_construct_simple():
    positive_subgraph = nx.generators.classic.path_graph(3)
    assert len(positive_subgraph.nodes) == 3
    assert len(positive_subgraph.edges) == 2
    signed_graph = from_positive_subgraph(positive_subgraph)
    assert len(signed_graph.nodes) == 3
    assert len(signed_graph.edges) == 3
