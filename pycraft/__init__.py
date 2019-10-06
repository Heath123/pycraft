import __main__
import inspect
import sys
import pycraft.parse

def __error(data):
  print("pycraft: Error while parsing\n", file=sys.stderr)
  print('  File "' + __main__.__file__ + '", line ' + str(data[1]), file=sys.stderr)
  print('    ' + data[2].strip(), file=sys.stderr)
  print('  ' + (data[3] - 1) * ' ' + '^', file=sys.stderr)
  print(data[4], file=sys.stderr)

#__code = """import test

#if 1 == 2:
#  print("abc")
# abc
#"""

__code = inspect.getsource(__main__)

__result = parse.parse(__code)

if str(type(__result)) == "<class 'list'>":
  if __result[0] == "error":
    error(__result)
else:
  print(__result.strip())

sys.exit()