#!/user/bin/env python
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
import matplotlib.cm as cm

file_inp = sys.argv[1]
f = open(file_inp, 'r')
lines = f.readlines()
f.close()
list1,list2=[],[]
for i in range(len(lines)):
    line=lines[i].strip().split()
    if len(line)==7:
        list1.append(float(line[1]))
        list2.append(float(line[3]))
x = np.array(list1)
y = np.array(list2)
"""
fig = plt.figure()
ax = fig.add_subplot(111)

for i in range(250):
    a = -45
    b = -15
    x.append(a + (b-a)*np.random.random())
    c = -5
    d = 10 
    y.append(c + (d-c)*np.random.random())

H=ax.hist2d(x, y, bins=95, norm=colors.LogNorm(), cmap=cm.jet)
H[3].set_clim(0,300)
#fig.colorbar(H[3],ax=ax)
plt.show()
"""
fig = plt.figure()
ax = fig.add_subplot(111)

H = ax.hist2d(x,y, bins=110, norm=matplotlib.colors.LogNorm(), cmap=cm.jet)
#H = ax.hist2d(x,y, bins=100, cmap=cm.jet)
fig.colorbar(H[3],ax=ax)
plt.show()
