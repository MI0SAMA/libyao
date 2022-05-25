#!/usr/bin/env python
#import sys
import math

check = input('Are your system is a cubic lattice?')
if  check == 'y' or check == 'Y':
    a = [input('Lattice length a: '), '0.0', '0.0']
    b = ['0.0', input('Lattice length b: '), '0.0']
    c = ['0.0', '0.0',input('Lattice length c: ') ]
else:
    a = input('Lattice constant a, like:1 2 3: ').rstrip().split(' ')
    b = input('Lattice constant b: ' ).rstrip().split(' ') 
    c = input('Lattice constant c: ').rstrip().split(' ') 

for i in (a,b,c):
    i=list(map(float, i))

Na=
