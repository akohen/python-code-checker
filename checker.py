from RestrictedPython import compile_restricted_exec
from RestrictedPython.Guards import safe_builtins
from RestrictedPython.Guards import guarded_iter_unpack_sequence
from RestrictedPython.Guards import full_write_guard
from RestrictedPython.Eval import default_guarded_getiter
from RestrictedPython.PrintCollector import PrintCollector

class SecurityException(Exception):
  pass

def custom_inplacevar(op, x, y):
  globs = {'x': x, 'y': y}
  exec('x{}y'.format(op),globs)
  return globs['x']

def custom_import(correction):
  def guarded_import(mname, globals=None, locals=None, fromlist=None, level=None):
    if fromlist is None:
        fromlist = ()
    if globals is None:
        globals = {}
    if locals is None:
        locals = {}

    mnameparts = mname.split('.')
    if not hasattr(correction, '_allowed_imports') or mnameparts[0] not in correction._allowed_imports:
      raise SecurityException("Not allowed to import module : %s" % mnameparts[0])
    return __import__(mname, globals, locals, fromlist)
  return guarded_import
      

def get_globals(correction):
  glb = dict(__builtins__=safe_builtins)
  glb['_getiter_'] = default_guarded_getiter
  glb['_iter_unpack_sequence_'] = guarded_iter_unpack_sequence
  glb['_inplacevar_'] = custom_inplacevar
  glb['_getitem_'] = getattr
  glb['_write_'] = lambda x : x
  glb['__metaclass__'] = type
  glb['__name__'] = __name__
  glb['_print_'] = PrintCollector
  glb['__builtins__']['__import__'] = custom_import(correction)
  return glb

class check:
  def __init__(self, correction, file):
    self.score = 0
    self.printed = ''
    self.tests = []
    self.errors = []
    try:
      compiled = compile_restricted_exec(file, '<string>')
      if compiled.errors:
        self.errors.append(compiled.errors)
        return
      code = {}
      exec(compiled.code, get_globals(correction), code)
      for m in dir(correction):
        if not m.startswith('_'):
          self.test(correction, m, code)
      if '_print' in code:
        self.printed = code['_print']()[:-1]
    except Exception as e:
      self.errors.append(e)

  def test(self, correction, func, code):
    try:
      self.score += getattr(correction, func)(self, code)
      self.tests.append({'test': func, 'passed': True})
    except Exception as e:
      self.tests.append({'test': func, 'passed': False, 'error': e})

  def __str__(self):
    return '{} pts with {} errors : {}'.format(self.score, len(self.errors), self.errors)

  @property
  def passed(self):
    return [i for i in self.tests if i['passed']]

  @property
  def failed(self):
    return [i for i in self.tests if not i['passed']]
