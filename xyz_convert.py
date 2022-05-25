#!/usr/bin/env python
import sys, numpy, libyao
import numpy as np
import ase.io.vasp

print ('Please ensure the lattice information and the supercell size are set correctly')
file_inp = sys.argv[1]
file_out = sys.argv[2]
libyao.convert_xyz(file_inp,file_out)
