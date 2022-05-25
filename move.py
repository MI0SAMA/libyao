#!/usr/bin/env python
import sys, numpy, libyao
file_inp = sys.argv[1]

atom_inp = input("The atoms to be moved (eg: 1-12,24-36): ")
dis_inp = input("The moved distance in xyz (eg: 0.1,0.1,0.1): ")

libyao.move_poscar(file_inp, atom_inp, dis_inp)
