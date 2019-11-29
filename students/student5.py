import numpy as np
from scipy.spatial.distance import pdist, squareform

a = np.arange(15).reshape(3, 5)
x = np.array([[0, 1], [1, 0], [2, 0]])
d = squareform(pdist(x, 'euclidean'))
print(a.ndim)
print(42)

def add():
  pass

def curry(a):
  def add(b):
    return b+a
  return add

print(curry(1)(2))