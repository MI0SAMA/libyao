#!/usr/bin/env python
import sys, numpy, libyao
import numpy as np
import ase.io.vasp

file_inp = sys.argv[1]
file_out = sys.argv[2]
#change the lattice information and extend size
xyz_file, out_file = file_inp, file_out
def get_box(xyz_file):
    with open(xyz_file) as in_xyz:
        line1 = in_xyz.readlines()[1] 
        if 'Lattice="' in line1:  # Lattice="40.0 0.0 0.0 0.0 40.0 0.0 0.0 0.0 40.0"
            box =  line1.rstrip().split('"')[1].split()
            a = box[0:3]
            b = box[3:6]
            c = box[6:]
        else:
            print ("Are your system is a cubic lattice?")
            check = input('Please type y to input lattice length or other keys to input lattice constant: ')
            if  check == 'y' or check == 'Y':
                a = [input('please enter a direction: '), '0.0', '0.0']
                b = ['0.0', input('please enter b direction: '), '0.0']
                c = ['0.0', '0.0',input('please enter c direction: ') ]
            else:
                a = input('Lattice constant a, like:1 2 3: ').rstrip().split( )
                b = input('Lattice constant b: ' ).rstrip().split( ) 
                c = input('Lattice constant c: ').rstrip().split( ) 
                for i in (a,b,c):
                    i=list(map(float, i))
    return a, b, c
#Cell size
a = ['13.55300000', '0.0', '0.0'] 
b = [' 6.77999952', '11.73500057', '0.0'] 
c = ['4.21399883', '2.43199956', '17.70789335']  
def get_total_ele(xyz_file):
    ele_list = []
    with open(xyz_file) as in_xyz:
        in_file = in_xyz.readlines()[2:]
        for line in in_file:
            ele_list.append(line.rstrip().split()[0])
    return list(set(ele_list))
def get_coordinations(ele):# get the coordination for one specifix element 
    line_list = []
    with open(xyz_file) as in_xyz:
        in_file = in_xyz.readlines()[2:]
        for line in in_file:
            line_s = line.rstrip().split()[0:4]
            if ele in line_s:
                line_list.append(line_s)
    return line_list
def get_num_ele(ele):#Get the number of each element 
    return len(get_coordinations(ele))
poscar = open(out_file, 'w')
poscar.write('Converted_POSCAR\n1.0\n')
#--a,b,c input by hand or set in script--#
#for i in get_box(xyz_file):
for i in a,b,c:
    poscar.write('%s %s %s\n' %(i[0], i[1], i[2]))
for i in get_total_ele(xyz_file):
    poscar.write(i+' ')
poscar.write('\n')
for i in get_total_ele(xyz_file):
    poscar.write(str(get_num_ele(i))+' ') 
poscar.write('\nCartesian\n')
for i in get_total_ele(xyz_file):
    for j in get_coordinations(i): 
        poscar.write('%s %s %s\n' %(j[1], j[2], j[3]))
poscar.close() #!!!
#--crystal size input by hand or set in script--#
#a=input('Supercell size like "3 3 3" >>').rstrip().split()
a=[3,3,1]
x,y,z = [int(i) for i in a]
try:
    cell = ase.io.vasp.read_vasp(out_file)
    ase.io.vasp.write_vasp(out_file+'_ex',cell*(x, y, z), direct=True,sort=True)
except:
    print('Something maybe wrong when using ase')