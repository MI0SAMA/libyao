#!/usr/bin/env python
import sys
import libyao
import numpy
import numpy as np
#sequence    O_H_angle*2    mid_angle    H_O_H_angle    O_H_dis*2    O_coordinate
file_inp = sys.argv[1]
f = open(file_inp, 'r')
lines = f.readlines()
f.close()
#---change the O atoms number of model---#
O_num=56
a = lines[2].strip().split()
b = lines[3].strip().split()
c = lines[4].strip().split()
axis = np.matrix((a,b,c),dtype=float).T #3*3array
O_dic,H_dic = libyao.read_water_angle_poscar(file_inp)
ang_dic1, ang_dic2, ang_dic3, ang_dic4 = {}, {}, {}, {}
dis_dic1, dis_dic2={},{}
mark=0
def O_H1_angle(O_dic,H_dic,axis,i):
    vec_oh1 = [float(H_dic[i][0][k]) - float(O_dic[i][k]) for k in range(3)]
    vec_oh1=np.inner(vec_oh1,axis)
    a1=np.inner(np.array(vec_oh1),np.array([0,0,-1]))
    b1=np.linalg.norm(np.array(vec_oh1))*np.linalg.norm(np.array([0,0,-1]))
    angle1=np.degrees(np.arccos(a1/b1))
    return angle1[0]
def O_H2_angle(O_dic,H_dic,axis,i):
    vec_oh2 = [float(H_dic[i][1][k]) - float(O_dic[i][k]) for k in range(3)]
    vec_oh2=np.inner(vec_oh2,axis)
    a2=np.inner(np.array(vec_oh2),np.array([0,0,-1]))
    b2=np.linalg.norm(np.array(vec_oh2))*np.linalg.norm(np.array([0,0,-1]))
    angle2=np.degrees(np.arccos(a2/b2))
    return angle2[0]
def mid_angle(O_dic,H_dic,axis,i):
    vec_mid = [(float(H_dic[i][0][k]) + float(H_dic[i][1][k]))/2 for k in range(3)]
    for x in range(3):
        vec_mid[x] = vec_mid[x] - float(O_dic[i][x])
    vec_mid=np.inner(vec_mid,axis)
    a3=np.inner(np.array(vec_mid),np.array([0,0,-1]))
    b3=np.linalg.norm(np.array(vec_mid))*np.linalg.norm(np.array([0,0,-1]))
    angle3=np.degrees(np.arccos(a3/b3))
    return angle3[0]
def H_O_H_angle(O_dic,H_dic,axis,i):
    vec_oh1 = [float(H_dic[i][0][k]) - float(O_dic[i][k]) for k in range(3)]
    vec_oh1=np.inner(vec_oh1,axis)
    vec_oh2 = [float(H_dic[i][1][k]) - float(O_dic[i][k]) for k in range(3)]
    vec_oh2=np.inner(vec_oh2,axis)    
    a=np.inner(np.array(vec_oh1),np.array(vec_oh2))
    b=np.linalg.norm(np.array(vec_oh1))*np.linalg.norm(np.array(vec_oh2))
    angle4=np.degrees(np.arccos(a/b))
    return angle4[0][0]
def O_H1_dis(O_dic,H_dic,axis,i):
    dis=np.subtract(H_dic[i][0],O_dic[i],dtype=float)
    dis=np.inner(dis,axis)
    dis1=np.linalg.norm(dis)
    return dis1
def O_H2_dis(O_dic,H_dic,axis,i):
    dis=np.subtract(H_dic[i][1],O_dic[i],dtype=float)
    dis=np.inner(dis,axis)
    dis2=np.linalg.norm(dis)
    return dis2
if len(O_dic) == O_num:
    for j in range(len(O_dic)):
        i=j+1
        if len(H_dic[i]) == 2:
            ang_dic1[i]=O_H1_angle(O_dic,H_dic,axis,i)
            ang_dic2[i]=O_H2_angle(O_dic,H_dic,axis,i)
            ang_dic3[i]=mid_angle(O_dic,H_dic,axis,i)
            ang_dic4[i]=H_O_H_angle(O_dic,H_dic,axis,i)
            dis_dic1[i]=O_H1_dis(O_dic,H_dic,axis,i)
            dis_dic2[i]=O_H2_dis(O_dic,H_dic,axis,i)
        elif len(H_dic[i]) == 1:
            ang_dic1[i]='Only one H atom around,The angle is:'
            ang_dic2[i]=O_H1_angle(O_dic,H_dic,axis,i)
            ang_dic3[i]='The distance is:'
            ang_dic4[i]=O_H1_dis(O_dic,H_dic,axis,i)
            dis_dic1[i]='The z_pos of O atom is:'
            dis_dic2[i]=O_dic[i][2]*float(c[2])
        elif len(H_dic[i]) == 0:
            ang_dic1[i]=ang_dic2[i]=ang_dic3[i]=ang_dic4[i]=dis_dic1[i]=dis_dic2[i]=' '
            ang_dic1[i]='No H atom around'
            dis_dic1[i]='Here is the O atom position:'
            dis_dic2[i]=O_dic[i]
        elif len(H_dic[i]) == 3:
            ang_dic1[i]=ang_dic2[i]=ang_dic3[i]=ang_dic4[i]=dis_dic1[i]=dis_dic2[i]=' '
            ang_dic1[i]='Three H atom around'
            dis_dic1[i]='Here is the O atom position:'
            dis_dic2[i]=O_dic[i]
        else:
            ang_dic1[i]=ang_dic2[i]=ang_dic3[i]=ang_dic4[i]=dis_dic1[i]=dis_dic2[i]=' '           
            ang_dic1[i]='More than three H atoms! OH my god!'
else:
    mark=1
file_out = file_inp+'_ang'
f_out = open(file_out, 'w')
f_out.truncate()
if mark==1:
    f_out.write('###########################################'+'\n')
    f_out.write('       Something unexcepted happened       '+'\n')
    f_out.write('###########################################'+'\n')
else:
    for i in range(1,O_num+1):
        f_out.write(str("{:0>2d}".format(i))+'    ')
        for j in ang_dic1[i],ang_dic2[i],ang_dic3[i],ang_dic4[i],dis_dic1[i],dis_dic2[i]:
            if isinstance(j,float):
                f_out.write(str(format(j,'7f'))+'    ')
            elif isinstance(j,str):
                f_out.write(str(j))
        for j in O_dic[i]:
            f_out.write(str(format(float(j),'7f'))+'    ')
        f_out.write('\n')
f_out.close() 