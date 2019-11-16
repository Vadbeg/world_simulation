import random
import numpy as np

field = [[int(random.randint(0, 5)) for i in range(5)]
         for j in range(5)]

print(field)
field = np.asarray([[0, 5, 4, 3, 1],
                    [4, 3, 1, 5, 0],
                    [3, 0, 5, 2, 1],
                    [0, 0, 2, 0, 0],
                    [5, 4, 0, 2, 1]])

print(field[0:1, 0:1])
