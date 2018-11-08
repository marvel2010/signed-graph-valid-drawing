import networkx as nx


def is_complete_signed_graph(graph):
    """ Checks if a graph is a complete signed graph.

    Checks the following:
        (1) Must be a networkx Graph.
        (2) Must be a complete graph.
        (3) Must have a 'sign' for every edge in [-1, 1]
    """
    if not isinstance(graph, nx.Graph):
        return False
    if len(graph.edges) == len(graph.nodes) * (len(graph.nodes) - 1) / 2:
        for edge in graph.edges:
            if 'sign' not in graph[edge[0]][edge[1]]:
                return False
            if graph[edge[0]][edge[1]]['sign'] in [-1, 1]:
                continue
            else:
                return False
        return True
    else:
        return False