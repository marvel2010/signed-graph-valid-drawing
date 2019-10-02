"""Embedding with Tensorflow1"""
# import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


def find_embedding(graph, dimension, max_steps=1000):
    """Tries to embed given graph in given dimension.

    Args:
        graph: the graph, in which every edge is assumed to have a 'sign'
            which is either +1 or -1.
        dimension: the dimension in which to try embedding the graph.
        max_steps: the maximum number of gradient steps to perform.

    Returns:
        obj: The value of the objective function, which will be 0.0 if
            the embedding succeeds and strictly positive, otherwise.
    """

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

    # 3n variables
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
    for step in range(max_steps):
        if sess.run(obj) == 0.0:
            break
        sess.run(opt)

    # assign values
    for node in graph.nodes:
        graph.nodes[node]['embedding'] = tuple(sess.run(graph.nodes[node]['embedding_variable']))

    return sess.run(obj)
