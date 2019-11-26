from checker import check
import os

class exo1:
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
    return 1

  def negative_values(self, code):
    assert code['add'](2,-3) == -1
    return 1

  def substraction(self, code):
    assert code['substract'](2,3) == -1
    return 1

class exo2:
  def return_value(self, code):
    assert code['myClass'](12).foo() == 12
    return 10
  
for student_submission in os.listdir('students'):
  source_code = open("students/" + student_submission,"r").read()
  correction = check(exo1, source_code)
  correction2 = check(exo2, source_code)
  print('{} - Exercise 1 - {}'.format(student_submission[:-3], correction))
  print('{} - Exercise 2 - {}'.format(student_submission[:-3], correction2))