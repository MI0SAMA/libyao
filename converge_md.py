#!/usr/bin/env python
import libyao 
import sys 
sta_num=float(sys.argv[1])
end_num=float(sys.argv[2])
z_list=[]
for h in range(80):
    num = 0
    for i in range(50):
        number = str(h*50+i)
        number=number.zfill(4)
        file_inp='POSCAR_'+number
        lines, ele_name, ele_num, dic_ele, dic_ele2 = libyao.read_poscar(file_inp)
        start_line= 7
        for j in dic_ele2.get('O')[0]:
            z_coord=lines[j+start_line].strip().split()[2]
            if sta_num<float(z_coord)<end_num:
                num += 1
    z_list.append(num)
print (z_list)