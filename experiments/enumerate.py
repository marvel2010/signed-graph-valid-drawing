import networkx as nx
import numpy as np
from sgvd.construct import from_positive_subgraph
from sgvd.embed import find_embedding

NODE_COUNT = 7
EMBEDDING_DIMENSION = 4
GRAPH_COUNT = 1044
FILE = '../data/7.txt'

f = open(FILE)

disconnected_count = 0

for graph_number in range(GRAPH_COUNT):

    # construct the graph
    np_graph = []
    for row_count in range(NODE_COUNT):
        np_graph.append(np.array(f.readline().rstrip(']\n').lstrip('[').split(' '), dtype=np.int))
    np_graph = np.array(np_graph)
    positive_graph = nx.to_networkx_graph(np_graph)

    # skip the blank line
    f.readline()

    # check connected
    if not nx.is_connected(positive_graph):
        disconnected_count += 1
        continue

    # check complete
    if len(positive_graph.edges) == NODE_COUNT * (NODE_COUNT - 1) / 2:
        continue

    # # special skips
    # if graph_number not in repeat_list:
    #     continue

    # analyze the graph
    signed_graph = from_positive_subgraph(positive_graph)
    embedding_objective = find_embedding(signed_graph, EMBEDDING_DIMENSION)
    if embedding_objective == 0.0:
        print("Embedding Found for Graph ", graph_number)
    elif embedding_objective > 0.0:
        print("No Embedding Found for Graph", graph_number)
    else:
        print("Error")


print("Disconnected Count", disconnected_count)
