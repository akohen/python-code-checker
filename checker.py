from RestrictedPython import compile_restricted_exec
from RestrictedPython.Guards import safe_builtins
from RestrictedPython.Guards import guarded_iter_unpack_sequence
from RestrictedPython.Guards import full_write_guard
from RestrictedPython.Eval import default_guarded_getiter
from RestrictedPython.PrintCollector import PrintCollector

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

def get_globals():
  glb = dict(__builtins__=safe_builtins)
  glb['_getiter_'] = default_guarded_getiter
  glb['_iter_unpack_sequence_'] = guarded_iter_unpack_sequence
  glb['_inplacevar_'] = custom_inplacevar
  glb['_getitem_'] = getattr
  glb['_write_'] = write
  glb['__metaclass__'] = type
  glb['__name__'] = __name__
  glb['_print_'] = PrintCollector
  glb['__import__'] = write
  glb['__builtins__']['__import__'] = __import__
  return glb

class check:
  def __init__(self, correction, file):
    self.score = 0
    self.printed = ''
    compiled = compile_restricted_exec(file, '<string>')
    if not compiled.errors:
      code = {}
      exec(compiled.code, get_globals(), code)
      self.errors = [i for i in (self.test(correction, m, code) for m in dir(correction) if not m.startswith('_')) if i]
      if '_print' in code:
        self.printed = code['_print']()[:-1]
    else:
      self.errors = [compiled.errors]
    

  def test(self, correction, func, code):
    try:
      self.score += getattr(correction, func)(self, code)
    except:
      return func


  def __str__(self):
    return '{} pts with {} errors : {}'.format(self.score, len(self.errors), self.errors)
