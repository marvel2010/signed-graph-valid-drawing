import networkx as nx


def _squared_euclidean_distance(v1, v2):
    assert len(v1) == len(v2)
    return sum((v1[i]-v2[i])**2 for i in range(len(v1)))


def is_complete_signed_graph(graph):
    """ Checks if a graph is a complete signed graph.

    Checks the following:
        (1) Must be a NetworkX Graph.
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


def is_embedded(graph, dimension):
    """ Checks if the graph is embedded in some dimension.

    Checks the following:
        (1) Must be a Complete Signed Graph.
        (2) Each node must have a tuple (embedding).
        (3) The length of each tuple must be the dimension.
    """
    if not is_complete_signed_graph(graph):
        return False
    for node in graph.nodes:
        if 'embedding' in graph.nodes[node] and len(graph.nodes[node]['embedding']) == dimension:
            continue
        else:
            return False
    return True


def is_valid_embedded(graph, dimension):
    """ Checks if the graph is valid embedded in some dimension.

    Checks the following:
        (1) Must be an Embedded Signed Graph.
        (2) Embedding must be Valid.

    An embedding is valid if, for every node, all its friends are closer
        than all its enemies.
    """
    if not is_embedded(graph, dimension):
        return False
    for node in graph.nodes:
        positive_distances = []
        negative_distances = []
        # record the distances
        for neighbor in graph.nodes:
            if node != neighbor:
                distance = _squared_euclidean_distance(graph.nodes[node]['embedding'], graph.nodes[neighbor]['embedding'])
                if graph[node][neighbor]['sign'] == 1:
                    positive_distances.append(distance)
                else:
                    negative_distances.append(distance)
        # check the conditions
        if len(positive_distances) == 0 or len(negative_distances) == 0:
            continue
        elif max(positive_distances) < min(negative_distances):
            continue
        else:
            return False
    return True

