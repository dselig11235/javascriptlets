#!/usr/bin/python


from TraceNmapParser import NmapParser
from sys import argv
from json import dumps
import os


path = os.path.dirname(os.path.realpath(__file__))
parser = NmapParser()
parser.open(argv[1:])
dataStr = dumps(parser.data)
with open(os.path.join(path, 'addPorts.js'), 'r') as f:
    funcStr = f.read()
print '{} addPorts({})'.format(funcStr, dataStr)

with open(os.path.join(path, 'addICMP.js'), 'r') as f:
    funcStr = f.read()
print '{} addICMP()'.format(funcStr)
