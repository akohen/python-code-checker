from checker import check
import os

class exo1:
  _allowed_imports = ['numpy']

  def compiles(self, code):
    return 1

  def basic_addition(self, code):
    assert code['add'](2,3) == 5
    return 1

  def add_zero(self, code):
    assert code['add'](2,0) == 2
    return 1

  def multiple_additions(self, code):
    assert code['add'](1,2,3) == 6
    return 5

  def negative_values(self, code):
    assert code['add'](2,-3) == -1
    return 1

  def substraction(self, code):
    assert code['substract'](2,3) == -1
    return 1

  def return_value(self, code):
    assert code['myClass'](12).foo() == 12
    return 10
  
for student_submission in os.listdir('students'):
  source_code = open("students/" + student_submission,"r").read()
  correction = check(exo1, source_code)
  if correction.errors:
    print('{} 0 pts - Errors: {}\n'.format(student_submission[:-3], correction.errors))
  else:
    print('{} {} pts'.format(student_submission[:-3], correction.score))
    print('Passed {}'.format( [i['test'] for i in correction.passed] ))
    print('Failed {}\n'.format( [(i['test'], type(i['error']).__name__) for i in correction.failed] ))