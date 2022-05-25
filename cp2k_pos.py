#!/usr/bin/env python
import sys
import numpy 

file_inp = sys.argv[1]

f = open(file_inp, 'r')
line = f.readlines()
f.close()
atom_num = int(line[0])
step_num = len(line)/(atom_num+2)
h_pos = []
o_pos = []
for i in range(len(line)):
    if line[i].strip().split()[0] == 'H':
        h_pos.append(line[i].strip().split()) #a list caontain all position began by mark H
    elif line[i].strip().split()[0] == 'O':
        o_pos.append(line[i].strip().split()) #a list caontain all position of O began by mark O
h_num, o_num = 2, 1 #depend on the real situation
ang_list, dis_list1, dis_list2 = [], [], []
for j in range(step_num):
    dist1_x = float(h_pos[2*j][1]) - float(o_pos[j][1])
    dist1_y = float(h_pos[2*j][2]) - float(o_pos[j][2])
    dist1_z = float(h_pos[2*j][3]) - float(o_pos[j][3])
    dist1 = numpy.sqrt(numpy.square(dist1_x)+numpy.square(dist1_y)+numpy.square(dist1_z))
    dis_list1.append(dist1)
    dist2_x = float(h_pos[2*j+1][1]) - float(o_pos[j][1])
    dist2_y = float(h_pos[2*j+1][2]) - float(o_pos[j][2])
    dist2_z = float(h_pos[2*j+1][3]) - float(o_pos[j][3])
    dist2 = numpy.sqrt(numpy.square(dist2_x)+numpy.square(dist2_y)+numpy.square(dist2_z))
    dis_list2.append(dist2)
    dist3_x = float(h_pos[2*j+1][1]) - float(h_pos[2*j][1])
    dist3_y = float(h_pos[2*j+1][2]) - float(h_pos[2*j][2])
    dist3_z = float(h_pos[2*j+1][3]) - float(h_pos[2*j][3])
    dist3 = numpy.sqrt(numpy.square(dist3_x)+numpy.square(dist3_y)+numpy.square(dist3_z))
    angle = numpy.arccos((numpy.square(dist1) + numpy.square(dist2) - numpy.square(dist3))/2*dist1*dist2)
    ang_list.append(numpy.degrees(angle))
print (ang_list)
