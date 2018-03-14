#!/usr/bin/env python3

from lib.compiler import dodosc
from sys import argv

for arg in dodosc(argv[1])(*map(int, argv[2:])): print(arg)
