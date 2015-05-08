__author__ = 'mirusso'
from subprocess import call
import sys

for arg in sys.argv:
    print arg

args = '-h'
call(["dev_appserver.py", args])

