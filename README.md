# Python code checker

This package aims to simplify correcting Python code submissions (eg. in an academic setting) by providing a simple way to automatically check some Python against a predefined set of tests.

## Installation
TODO

## Usage
Start by creating a correction class:
```
class myCorrection:
```

Then define a function for each test you'd like to run. Each function should return an integer if it is successful and should throw an assertion error otherwise.
```
class myCorrection:
  def basic_addition(self, code):
    assert code['add'](2,3) == 5
    return 1
```
This example will call the function `add(2,3)` from the supplied code, and add 1 point if it returns 5.

To check some code against your correction class:
```
import os
from checker import check

class myCorrection:
  _allowed_imports = ['numpy']

  def basic_addition(self, code):
    assert code['add'](2,3) == 5
    return 1

source_code = open("file_to_check.py","r").read()
correction = check(myCorrection, source_code)
print(correction.score)
print(correction.printed)
print(correction.errors)
print(correction.tests)
```

- `correction.score` will return the sum of the value of the tests successfully passed
- `correction.printed` the results of all the calls to `print` in the code
- `correction.errors` a list of compilation errors
- `correction.tests` returns a list of all tests run, with their results and eventual reasons for failure
- `correction.passed` and `correction.failed` will only return the list of passed and failed tests
- The `_allowed_imports` attribute allows you to specify a list of modules that can be imported.

