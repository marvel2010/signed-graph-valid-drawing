import networkx as nx
import pytest
from sgvd.validate import is_complete_signed_graph
from sgvd.validate import is_embedded
from sgvd.validate import is_valid_embedded


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


@pytest.fixture
def graph_embedded(graph_signed):
    graph_signed.nodes[1]['embedding'] = (1.0, 0.0, 0.0)
    graph_signed.nodes[2]['embedding'] = (0.0, 1.0, 0.0)
    graph_signed.nodes[3]['embedding'] = (0.0, 0.0, 1.0)
    return graph_signed


@pytest.fixture
def graph_embedded_contracted(graph_embedded):
    graph_embedded.nodes[2]['embedding'] = (0.5, 0.1, 0.5)
    return graph_embedded


@pytest.fixture
def graph_embedded_expanded(graph_embedded):
    graph_embedded.nodes[2]['embedding'] = (2.0, 0.1, 0.1)
    return graph_embedded


def test_too_few_edges(graph_with_too_few_edges):
    assert not is_complete_signed_graph(graph_with_too_few_edges)


def test_missing_signs(graph_missing_signs):
    assert not is_complete_signed_graph(graph_missing_signs)


def test_graph_signed(graph_signed):
    assert is_complete_signed_graph(graph_signed)


def test_signed_graph_not_embedded(graph_signed):
    assert not is_embedded(graph_signed, 3)


def test_embedded_graph_wrong_dimension(graph_embedded):
    assert not is_embedded(graph_embedded, 2)
    assert not is_embedded(graph_embedded, 4)


def test_embedded_graph_correct_dimension(graph_embedded):
    assert is_embedded(graph_embedded, 3)


def test_embedding_fails_at_equality(graph_embedded):
    assert not is_valid_embedded(graph_embedded, 3)


def test_embedding_fails_at_invalid(graph_embedded_expanded):
    assert not is_valid_embedded(graph_embedded_expanded, 3)


def test_embedding_passes_at_valid(graph_embedded_contracted):
    assert is_valid_embedded(graph_embedded_contracted, 3)