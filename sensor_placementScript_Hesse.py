#!/usr/bin/python

import MI_sensorPlacement as MI
import numpy as np
import matplotlib.pyplot as plt
import random
import DatabaseCloud as DC
import DatabaseLight as DL
import sqlite3

DC.updateCloudData()
DL.updateAllData()
connection=sqlite3.connect('data.db')
cursor=connection.cursor()
S=set()
dataDict=dict()
lightlist=['light1', 'light2', 'light3', 'light4']
for light in lightlist:
	moteNum=int(light[5])
	cursor.execute('select light from %s' %(light))
	temp=cursor.fetchall()
	dataDict[moteNum]=[float(x[0]) for x in temp]
dataMatrix=np.array([])
for moteNum in dataDict.keys():
	currentDataVec=dataDict[moteNum]
	S.add(moteNum)
	if dataMatrix.size==0:
		dataMatrix=np.atleast_2d(currentDataVec)
	else:
		dataMatrix=np.vstack((dataMatrix,currentDataVec)) #NOT DONENENENENENENENE
U=set()
k=10



#create the covariance matrices for each kernel function
#KernelsList=['squared exponential', 'matern', 'rational quadratic']
KernelsList=['squared exponential', 'sample covariance']
SigmaList=[1, 2, 3]
cov_V_V=dict()
for kernel in KernelsList:
	kernelObj=MI.Kernel(kernel,21,1,1)
	if not kernel=='sample covariance':
		data=MI.distanceMatrix('mote_locs.txt')
	else:
		data=dataMatrix
	kernelObj.store_kernel_matrix(data)
	cov_V_V[kernel]=kernelObj.get_kernel_matrix()

if 'sample covariance' in cov_V_V.keys():
	size=cov_V_V['sample covariance'].shape
	for i in [4, 14, 49, 19, 17, 7]: #may be a problem since i'm not using ALLL of the sensors (like all 58)
		zerosVert=np.zeros((size[0],1))
		zerosHoriz=np.zeros((1,size[1]))
		cov_V_V['sample covariance']=np.insert(cov_V_V['sample covariance'],i,zerosHoriz, axis=0)
		cov_V_V['sample covariance']=np.insert(cov_V_V['sample covariance'],i,zerosVert, axis=1)
placement=dict()
placement_locs=dict()
placement_x_locs=dict()
placement_y_locs=dict()
labels=dict()
#im = plt.imread('guestrin_lab.png')
#mplot = plt.imshow(im)
#ax=fig.add_subplot(111)
shapes=['8',',','^']
colors=['r','b','g']

#for each kernel, solve the sensor placement problem using MI, and plot the results.
for kernel in cov_V_V.keys():
	labels[kernel]="%s covariance" % (kernel)
	placement[i]=MI.maxMutualInformation(k,cov_V_V[kernel],S,U)
	print placement[i]
	placement_locs[i]=np.array([])
	placement_x_locs=np.array([])
	placement_y_locs=np.array([])
	for sensor in placement[i]:
		placement_x_locs=np.append(placement_x_locs,np.array((60.5-locations[sensor][0])*10))
		placement_y_locs=np.append(placement_y_locs,np.array((locations[sensor][1])*10))

	plt.scatter(placement_x_locs, placement_y_locs, c=colors[i], marker=shapes[i], label=labels[kernel])
	i+=1
	# Put a legend below current axis
	#ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True)
	#box = ax.get_position()
	#ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
	#plt.xlim(0,41)
	#plt.ylim(-1,31)
plt.show()
