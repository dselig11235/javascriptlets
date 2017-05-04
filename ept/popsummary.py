#!/usr/bin/python


from TraceNmapParser import NmapParser
from sys import argv
from json import dumps
import os


with open(argv[1]) as f:
    echoes = [x.strip() for x in f]
path = os.path.dirname(os.path.realpath(__file__))
parser = NmapParser()
parser.open(argv[2:])
dataStr = dumps(parser.data)
uniqueIps = set(x[0] for x in parser.data)
with open(os.path.join(path, 'addPorts.js'), 'r') as f:
    funcStr = f.read()
print '{} addPorts({})'.format(funcStr, dataStr)

dataStr = dumps([x for x in uniqueIps])
echoesStr = dumps(echoes)
with open(os.path.join(path, 'addICMP.js'), 'r') as f:
    funcStr = f.read()
print '{} addICMP({}, {})'.format(funcStr, dataStr, echoesStr)
