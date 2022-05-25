#!/usr/bin/env python
import sys
import numpy

file_inp = sys.argv[1]
f = open(file_inp, 'r')
lines = f.readlines()
f.close()

ene_list=[]
for i in range(len(lines)):
    ene=lines[i].strip().split()
    ene_list.append(float(ene[3]))

f_out = open('energy', 'w')
for i in range(len(ene_list)):
    f_out.write(str(ene_list[i])+'\n')

f_out.close()