#!/user/bin/env python
from matplotlib import colors 
from matplotlib.ticker import PercentFormatter 
import numpy as np 
import matplotlib.pyplot as plt 
  
   
N_points = 100000
x = np.random.randn(N_points) 
y = 4 * x + np.random.randn(100000) + 50
   
plt.hist2d(x, y, 
           bins = 100,  
           norm = colors.LogNorm(),  
           cmap ="gray") 
  
plt.title('matplotlib.pyplot.hist2d() function Example\n\n', fontweight ="bold") 
  
plt.show()