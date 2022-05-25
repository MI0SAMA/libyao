import sys
import math
import numpy as np
import libyao 
try:
    sta_num=int(sys.argv[1])
    end_num=int(sys.argv[2])
    dis=float(sys.argv[3])
except:
    print ("""Please input the sequence number of POSCAR and distance
For exampe: python density.py 24 3124 0.2""")
z_list=[]
for i in range (sta_num,end_num+1):
    num=str(i).zfill(4)
    file_inp='POSCAR_'+num
    lines, ele_name, ele_num, dic_ele, dic_ele2 = libyao.read_poscar(file_inp)
    if lines[7].strip() == "Selective Dynamics" or lines[7].strip() == "S":
        start_line = 8
    else:
        start_line= 7
    for j in dic_ele2.get('O')[0]:
        z_list.append(float(lines[j+start_line].strip().split()[2]))    
a = lines[2].strip().split()
b = lines[3].strip().split()
z_max,z_min=math.ceil(max(z_list)),int(min(z_list))
num_dic={}
for j in np.arange(z_min,z_max,dis):
    num=0
    for i in range(len(z_list)-1,-1,-1):
        if z_list[i] >= j and z_list[i] <= j+dis:
            num+=1
            del z_list[i]
    num_dic[j]=num*18/0.6022/dis/float(a[0])/float(b[1])/(end_num-sta_num+1)
for i in num_dic:
    print (str(format(i,'.1f')),':',str(format(num_dic[i],'.7f')))   