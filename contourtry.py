##THIS PROGRAM GETS SENSOR READINGS FROM 9 SENSORS AT NASA AMES AND COMPUTES THE INTERPOLATION 
import run
import numpy as np
import scipy as sp
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import pylab as p
import numpy.ma as ma
from numpy.random import uniform, seed
seed(1234) # make up some randomly distributed data
npts = 9  #No. of sensors
x=sp.array([4,2.5,0,2.5,4,2.5,0,5,5]) #x coordinate of sensors
y=sp.array([4.75,4.75,4.75,2.5,0.2,0.2,0.2,5,0]) #y coordinate of sensors
z=run.plot() #gets the sensor readings for 9 sensors 
# define grid.
xi = np.linspace(-1,6,100)
yi = np.linspace(-1,6,100)
# grid the data.
fig=p.figure()
zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')
# contour the gridded data, plotting dots at the randomly spaced data points.
CS = plt.contour(xi,yi,zi,30,linewidths=0.5,colors='k')
CS = plt.contourf(xi,yi,zi,30,cmap=plt.cm.jet)
plt.colorbar() # draw colorbar
# plot data points.
plt.scatter(x,y,marker='o',c='b',s=10)
plt.xlim(0,5)
plt.ylim(0,5)
##j=(1,2,3,5,6,7,8,9)
##plt.text(x,y,'sensor %.0f' % j)
p.savefig('C:\Users\chandrayee\Desktop\NASA\python\colored_image.png')
plt.show()

