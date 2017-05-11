#!/usr/bin/python


from TraceNmapParser import NmapParser
from sys import argv
from json import dumps
import os,csv


if(argv[1] == "-t"):
    type=argv[2]
    files = argv[3:]
else:
    type="gnmap"
    files = argv[1:]

path = os.path.dirname(os.path.realpath(__file__))
parser = NmapParser()
parser.open(files, type)
dataStr = dumps(parser.data)
with open(os.path.join(path, 'addPorts.js'), 'r') as f:
    funcStr = f.read()
print '{} addPorts({})'.format(funcStr, dataStr)

with open(os.path.join(path, 'addICMP.js'), 'r') as f:
    funcStr = f.read()
print '{} addICMP()'.format(funcStr)
