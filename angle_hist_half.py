#!/usr/bin/env python
import sys
import math
import numpy as np
import matplotlib.cm as cm
import matplotlib
import matplotlib.pyplot as plt
try:
    sta_num=int(sys.argv[1])
    end_num=int(sys.argv[2])
except:
    print ("""Input Wrong""")
z_dic={}
z_dic[1],z_dic[2]=[],[]
for i in range (sta_num,end_num+1):
    num=str(i).zfill(4)
    file_inp='POSCAR_'+num+'_ex_ang'
    f = open(file_inp, 'r')
    lines = f.readlines()
    f.close()
    for j in range(len(lines)):
        line = lines[j].strip().split()
        if len(line)==10:
            if 0.25<float(line[9])<0.5:
                z_dic[1].append(float(line[1]))
                z_dic[2].append(float(line[3]))
x = np.array(z_dic[1])
y = np.array(z_dic[2])
fig = plt.figure()
ax = fig.add_subplot(111)

#H = ax.hist2d(x,y, bins=110, norm=matplotlib.colors.LogNorm(), cmap=cm.jet)
H = ax.hist2d(x,y, bins=100, cmap=cm.jet)
fig.colorbar(H[3],ax=ax)
plt.show()
