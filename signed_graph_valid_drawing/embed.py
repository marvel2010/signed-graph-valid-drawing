import tensorflow as tf


def find_embedding(graph, dimension):
    """ Tries to embed given graph in given dimension. """

    # make sure that no variables carry over between embeddings
    tf.reset_default_graph()

    # n variables
    # node 'embedding_variable'
    for node in graph.nodes:
        graph.nodes[node]['embedding_variable'] = tf.get_variable(str(node), [dimension])

    # m variables
    # edge 'distance_variable'
    for edge in graph.edges:
        graph.edges[edge]['distance_variable'] = tf.norm(
            graph.nodes[edge[0]]['embedding_variable'] - graph.nodes[edge[1]]['embedding_variable']
        )

    # 3*n variables
    #  n friend variables
    #  n enemies variables
    #  n objective variables
    for node in graph.nodes:
        friend_distance_variables = [graph.edges[edge]['distance_variable'] for edge in graph.edges(nbunch=node) if graph.edges[edge]['sign'] == 1]
        enemy_distance_variables = [graph.edges[edge]['distance_variable'] for edge in graph.edges(nbunch=node) if graph.edges[edge]['sign'] == -1]
        if len(friend_distance_variables) == 0 or len(enemy_distance_variables) == 0:
            # the node has only positive or only negative neighbors
            graph.nodes[node]['objective_penalty_variable'] = tf.constant(0.0)
        else:
            # the node has both positive and negative neighbors
            graph.nodes[node]['farthest_friend_distance_variable'] = tf.reduce_max(
                tf.stack(friend_distance_variables)
            )
            graph.nodes[node]['nearest_enemy_distance_variable'] = tf.reduce_min(
                tf.stack(enemy_distance_variables)
            )
            graph.nodes[node]['objective_penalty_variable'] = tf.maximum(
                graph.nodes[node]['farthest_friend_distance_variable'] - graph.nodes[node]['nearest_enemy_distance_variable'] + 0.1,
                0.0
            )

    # objective
    obj = sum(graph.nodes[node]['objective_penalty_variable'] for node in graph.nodes)

    # optimizer
    opt = tf.train.AdamOptimizer(1.0).minimize(obj)

    # session
    sess = tf.Session()

    # initialize
    init = tf.global_variables_initializer()
    sess.run(init)

    # optimize
    for step in range(1000):
        if sess.run(obj) == 0.0:
            break
        sess.run(opt)

    # assign values
    for node in graph.nodes:
        graph.nodes[node]['embedding'] = tuple(sess.run(graph.nodes[node]['embedding_variable']))

    return sess.run(obj)
