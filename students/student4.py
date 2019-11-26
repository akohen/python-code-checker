def add(*args):
  sum = 0
  for n in args:
    sum += n
  return sum

def substract(a, b):
  return a-b

class myClass:
  def __init__(self, value):
    self.value = value
  
  def foo(self):
    return self.value