#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import ase.io.vasp

file_read = sys.argv[1]
a=input('Supercell size like "3 3 3" >>').rstrip().split()
x,y,z = [int(i) for i in a]
#x,y,z     = [int(i) for i in sys.argv[2:5]]
try:
    cell = ase.io.vasp.read_vasp(file_read)
    ase.io.vasp.write_vasp(file_read+'_ex',cell*(x, y, z), direct=True,sort=True)
except:
    print('Something maybe wrong')
