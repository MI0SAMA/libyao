#!/usr/bin/env python
import sys
import numpy
import matplotlib.pyplot as plt

file_inp = sys.argv[1]
f = open(file_inp, 'r')
lines = f.readlines()
f.close()

count=len(lines)
result, angle=[], []
angle_dic = {}
for i in range(count):
    single_line=lines[i].strip().split()
    result.append(float(single_line[1]))
    angle.append(numpy.rad2deg(float(single_line[1])))
var=numpy.var(result)
f_out = open('angle', 'w')
f_out.write("Variance="+str(var)+'\n')
f_out.write("angle"+'\n')
#f_out.write('\n'.join(angle))
for i in range(95,110,1):
    num=0
    for j in range(len(angle)):
        if float(angle[j]) > (i-0.5) and float(angle[j]) < (i+0.5):
            num += 1
        #list.append(num)
    angle_dic[i] = num
    f_out.write(str(i)+':'+str(num)+'\n')
f_out.close()

a, b=[], []
for i in angle_dic.keys():
    #print(i)
    a.append(i)
    b.append(angle_dic[i])
plt.figure()
plt.plot(a, b, marker='o', color='r')
plt.xlabel('Angle')
plt.ylabel('Possibility')
plt.savefig('angle.png')
#plt.show()