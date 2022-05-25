#!/usr/bin/env python

import sys
import numpy
import libyao

file_inp = sys.argv[1]

fix = input("How your atoms fied (eg: F,F,T): ")
atom = input("The atoms to be fixed (eg: 1-12,24-36): ")
libyao.fix_poscar(fix,atom,file_inp)
