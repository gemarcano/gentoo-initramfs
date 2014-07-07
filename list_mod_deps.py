#!/usr/bin/env python
from subprocess import check_output
from subprocess import CalledProcessError

def list_mod_deps(module):
  """Returns a list of dependencies for the given kernel module."""
  result = set()
  args = ["modinfo", "-F", "depends", "-0", module]
  
  try:
    dependencies = check_output(args, universal_newlines=True, shell=False).split('\x00')
  except CalledProcessError:
    return result
  
  tmp = []
  for dep in dependencies:
    tmp += dep.split(',')
  dependencies = tmp
  dependencies = list(filter(None, dependencies))
  
  if not dependencies or next(iter(dependencies)) == '\x00':
    return set([module])
  
  for dep in dependencies:
    result.update(list_mod_deps(dep))
    result.add(module)
  
  return result

def list_mod_location(module, kernel=None):
  """Returns the location of the kernel module."""
  args = ["modinfo", "-n", "-0"]
  if kernel:
    args.append("-k")
    args.append(kernel)
  args.append(module)
  result = next(iter((check_output(args, universal_newlines=True, shell=False).split('\x00'))))
  return result
  
import argparse

if __name__ == "__main__":
  
  parser = argparse.ArgumentParser(description="List module dependency tree for given module.")
  parser.add_argument("modules", nargs='+', type=str, help="Module to use as root of tree.")
  parser.add_argument("-0", "--null", action="store_const", const='\0', dest="delim", default='\n', help="Use null as the delimiter between modules.")
  parser.add_argument("-k", "--kernel", action="store", dest="kernel", help="Kernel version to use when searching for modules. Default is active kernel.")

  args = parser.parse_args()
  delim = args.delim
  
  deps = set()
  for module in args.modules:
    deps.update(list_mod_deps(module))
    
  for dep in deps:
    print(list_mod_location(dep, args.kernel), end=delim)
