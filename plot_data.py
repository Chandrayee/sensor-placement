from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np



fig = plt.figure()
ax = fig.gca(projection='3d')
cov=[[1,0,1],[1,0,100],[1,0,1]]
mean=[0,0,0]
X,Y,Z=np.random.multivariate_normal(mean,cov,5000).T
#X = np.arange(-5, 5, 0.25)
#Y = np.arange(-5, 5, 0.25)
X,Y=np.meshgrid(X,Y)
Z=np.arange(-5, 5, 0.25)
#X,Y=np.meshgrid(X,Y)
#Z = np.sin(X+Y)
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
        linewidth=0, antialiased=False)

plt.show()