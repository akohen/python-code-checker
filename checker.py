from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins
from RestrictedPython.Guards import guarded_iter_unpack_sequence
from RestrictedPython.Guards import full_write_guard
from RestrictedPython.Eval import default_guarded_getiter
import os
import builtins

def custom_inplacevar(op, x, y):
  globs = {'x': x, 'y': y}
  exec('x{}y'.format(op),globs)
  return globs['x']

def custom_metaclass(name, bases, dict):
    for k in dict.items():
        if k.endswith('__roles__') and k[:len('__roles__')] not in dict:
            raise Exception("Can't override security: %s" % k)
    ob = type(name, bases, dict)
    ob.__allow_access_to_unprotected_subobjects__ = 1
    ob._guarded_writes = 1
    return ob

def write(ob):
  return ob

glb = dict(__builtins__=safe_builtins)
glb['_getiter_'] = default_guarded_getiter
glb['_iter_unpack_sequence_'] = guarded_iter_unpack_sequence
glb['_inplacevar_'] = custom_inplacevar
glb['_getitem_'] = getattr
glb['_write_'] = write
glb['__metaclass__'] = type
glb['__name__'] = __name__

class check:
  def __init__(self, correction, file):
    self.score = 0
    try:
      code = {}
      byte_code = compile_restricted(file, '<string>', 'exec')
      exec(byte_code, glb, code)
      self.errors = [i for i in (self.test(correction, m, code) for m in dir(correction) if not m.startswith('__')) if i]
    except SyntaxError as e:
      self.errors = [e]
    

  def test(self, correction, func, code):
    try:
      self.score += getattr(correction, func)(self, code)
    except:
      return func


  def __str__(self):
    return '{} pts with {} errors : {}'.format(self.score, len(self.errors), self.errors)
