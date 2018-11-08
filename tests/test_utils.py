import networkx as nx
import pytest

@pytest.fixture
def graph_with_too_few_edges():
    graph = nx.Graph()
    graph.add_nodes_from([1, 2, 3])
    graph.add_edges_from([(1, 2, {'sign': 1}),
                          (1, 3, {'sign': -1})])
    return graph

@pytest.fixture
def graph_missing_signs(graph_with_too_few_edges):
    graph_with_too_few_edges.add_edge(2, 3)
    return graph_with_too_few_edges

@pytest.fixture
def graph_signed(graph_missing_signs):
    graph_missing_signs[2][3]['sign'] = 1
    return graph_missing_signs


def test_too_few_edges(graph_with_too_few_edges):
    from signed_graph_valid_drawing.utils import is_complete_signed_graph
    assert not is_complete_signed_graph(graph_with_too_few_edges)


def test_missing_signs(graph_missing_signs):
    from signed_graph_valid_drawing.utils import is_complete_signed_graph
    assert not is_complete_signed_graph(graph_missing_signs)


def test_graph_signed(graph_signed):
    from signed_graph_valid_drawing.utils import is_complete_signed_graph
    assert is_complete_signed_graph(graph_signed)