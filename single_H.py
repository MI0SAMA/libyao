#!/usr/bin/env python
import sys
import numpy
import numpy as np
import libyao
file_inp=sys.argv[1]
lines, ele_name, ele_num, dic_ele, dic_ele2 = libyao.read_poscar(file_inp)
pos_dic={}
if lines[7].strip() == "Selective Dynamics" or lines[7].strip() == "S":
    start_line = 8
else:
    start_line= 7
for i in ele_name:
    pos_list=[]
    for j in dic_ele2.get(i)[0]: #get lines one type of atom belongs to
        coord_list = lines[j+start_line].strip().split()[0:3]
        pos_list.append(coord_list) #the position agained
        pos_dic[i]= pos_list
#Calculate the distance between O and H
a = lines[2].strip().split()
b = lines[3].strip().split()
c = lines[4].strip().split()
axis = np.matrix((a,b,c),dtype=float).T #3*3array
O_dic,H_dic={},{}
H_list=[] #all H atoms in 0.3~0.7
num=0
for i in pos_dic['H']:
    i = [float(k) for k in i]
    if 0.3<float(i[0])<0.7 and 0.3<float(i[1])<0.7:
        H_list.append(i)
for i in pos_dic['O']:
    i = [float(k) for k in i]
    if 0.3<i[0]<0.7 and 0.3<i[1]<0.7:
        num +=1
        O_dic[num]=i
        H_dic[num]=[]
        for j in H_list:
            j = [float(k) for k in j]
            dis=np.subtract(i,j,dtype=float)
            dis1=np.inner(dis,axis) #Attention!!!
            if np.linalg.norm(dis1) < 1.1:
                H_dic[num].append(j)
H_around_list=[] # H atoms within 1.1 from O atom
for i in range(len(H_dic)):
    for k in H_dic[i+1]:
        H_around_list.append(k)
#goal=112-len(H_around_list)
H_no_list=[x for x in H_list if x not in H_around_list]
H_alone_list=[]
for i in H_no_list:
    if 0.3333333<i[0]<0.66666666 and 0.33333333<i[1]<0.66666666:
        H_alone_list.append(i)
file_out = file_inp+'_single'
f_out = open(file_out, 'w')
f_out.truncate()
if len(H_alone_list)!=0:
    f_out.write(str(len(H_alone_list))+'\n')
    for i in H_alone_list:
        for j in i:
            f_out.write(str(format(j,'7f'))+'    ')
        f_out.write('\n')
else:
    f_out.write('No single H')
f_out.close() 
"""
flag = True
for distance in np.arange(1.1,5.1,0.1):
    for i in range(1,57):
        for j in H_no_list:
            dis=np.subtract(O_dic[i],j,dtype=float)
            dis1=np.inner(dis,axis)
            #print (np.linalg.norm(dis1))
            if np.linalg.norm(dis1) < distance:
                #H_no_list.remove(j)
                H_alone_list.append(j)
                if len(H_alone_list)==goal:
                    flag = False
                    break
        if not flag:
            break
    if not flag:
        break
"""