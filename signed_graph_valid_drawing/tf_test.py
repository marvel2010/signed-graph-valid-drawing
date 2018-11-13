import tensorflow as tf

DIMENSION = 1

# n variables
x1 = tf.get_variable("x1", [DIMENSION])
x2 = tf.get_variable("x2", [DIMENSION])
x3 = tf.get_variable("x3", [DIMENSION])

# m variables
d12 = tf.norm(x1 - x2)
d13 = tf.norm(x1 - x3)
d23 = tf.norm(x2 - x3)

# assume edge (1, 2) is positive
#  d12 < d13
#  d12 < d23

# n variables
v1 = tf.maximum(d12 - d13 + 0.1, 0)
v2 = tf.maximum(d12 - d23 + 0.1, 0)
v3 = tf.maximum(0.0, 0.0)

# objective
obj = (v1 + v2 + v3)

# optimizer
opt = tf.train.GradientDescentOptimizer(0.1).minimize(obj)

# session
sess = tf.Session()

# initialize
init = tf.global_variables_initializer()
sess.run(init)

for step in range(10):
    sess.run(opt)
    print(step, sess.run(x1), sess.run(x2), sess.run(x3))
    print(step, sess.run(obj))