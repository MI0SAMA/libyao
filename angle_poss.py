#!/usr/bin/env python
import sys

file_inp=sys.argv[1]
f = open(file_inp, 'r')
lines = f.readlines()
f.close()
names=locals()
for i in range(4):
    names['ang_list'+str(i+1)]=[]
for i in range(len(lines)):
    line=lines[i].strip().split()
    if len(line)==7:
        for j in range(4):
            eval('ang_list'+str(j+1)).append(line[j+1])
def cal_poss(ang_list):
    pos_list = []
    for i in range(5,180,10):
        num = 0
        for j in range(len(ang_list)):
            if float(ang_list[j]) > float(i-5) and float(ang_list[j]) < float(i+5):
                num += 1
        num = float(num)/len(ang_list)
        pos_list.append(num)
    return pos_list
pos_dic={}
for i in range(4):
    pos_dic[i] = cal_poss(eval('ang_list'+str(i+1)))
#print (pos_dic[1])
file_out = file_inp + '_poss'
f_out = open(file_out, 'w')
f_out.truncate()
f_out.write('Range     O-H1_poss    O-H2_poss    mid_poss    H-O-H_poss\n')
for j in range(5,180,10):
    f_out.write(str("{:0>2d}".format(j-5))+'~'+str("{:0>2d}".format(j+5)))
    for k in range(4):
        f_out.write('     '+str(format(pos_dic[k][int((j-5)/10)], '4f')))
    f_out.write('\n')
f_out.close()