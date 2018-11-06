import numpy as np
from scipy.spatial.distance import euclidean

v1=(1,1,0,0)
v2=(-1,1,0,0)
v3=(1,-1,0,0)
v4=(-1,-1,0,0)

w1=(0,0,np.sqrt(2)-1/8,-1/4)
w2=(0,0,-np.sqrt(2)+1/8,-1/4)
w3=(0,0,0,np.sqrt(2)-1/8)

for x in [v1, v2, v3, v4]:
    for friend in [w1, w2, w3]:
        for enemy in [v1, v2, v3, v4]:
            if enemy != x:
                assert euclidean(x, friend) < euclidean(x, enemy), '\n Node: %s \n Friend: %s (Distance: %s) \n Enemy: %s (Distance: %s)' % (x, friend, euclidean(x, friend), enemy, euclidean(x, enemy))

for x in [w1, w2, w3]:
    for friend in [v1, v2, v3, v4]:
        for enemy in [w1, w2, w3]:
            if enemy != x:
                assert euclidean(x, friend) < euclidean(x, enemy), '\n Node: %s \n Friend: %s (Distance: %s) \n Enemy: %s (Distance: %s)' % (x, friend, euclidean(x, friend), enemy, euclidean(x, enemy))

print("All assertions passed.")
