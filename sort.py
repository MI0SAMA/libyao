#!/usr/bin/env python
import sys, numpy, libyao

file_inp = sys.argv[1]
axis = input("which direction you want to sort by: ")
libyao.sort_poscar(axis,file_inp)
