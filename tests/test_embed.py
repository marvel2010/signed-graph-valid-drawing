import pytest
import networkx as nx
from sgvd.construct import from_positive_subgraph
from sgvd.embed import find_embedding
from sgvd.validate import is_valid_embedded

test_graphs = [
    (nx.generators.classic.path_graph(3), 1, 1),
    (nx.generators.classic.path_graph(4), 1, 1),
    (nx.generators.classic.cycle_graph(4), 1, 0),
    (nx.generators.classic.cycle_graph(4), 2, 1),
    (nx.algorithms.bipartite.generators.complete_bipartite_graph(3, 2), 2, 0),
    (nx.algorithms.bipartite.generators.complete_bipartite_graph(3, 3), 3, 0),
    (nx.algorithms.bipartite.generators.complete_bipartite_graph(3, 3), 4, 1),
]


@pytest.mark.parametrize("positive_subgraph,dimension,expected_result", test_graphs)
def test_embed(positive_subgraph, dimension, expected_result):
    signed_graph = from_positive_subgraph(positive_subgraph)
    objective = find_embedding(signed_graph, dimension)
    if expected_result:
        assert objective == 0.0
        assert is_valid_embedded(signed_graph, dimension)
    else:
        assert objective > 0.0
        assert not is_valid_embedded(signed_graph, dimension)
