#!/usr/bin/python

import MI_sensorPlacement as MI
import numpy as np
import matplotlib.pyplot as plt
import random

#files=['mote_locs.txt']
#parser=MI.Parsing(files)
#parsedText=parser.textParsing()
#locations=parsedText[2] #get the possible locations of the sensors
#S=set(locations.keys())
S=set()
locations=dict()
averagedData=open('averagedGuestrinDataFile.txt','r').readlines()
dataMatrix=np.array([])

for line in averagedData:
	dat=[]
	line=line.split()
	moteNum=int(line[0])
	for datstring in line[5:]:
		dat.append(float(datstring.replace(',',' ').replace('[',' ').replace(']',' ').strip()))
	currentDataVec=np.atleast_2d(dat)
	if 4<moteNum<7:   #[4, 14, 49, 19, 17, 7]
		moteNum-=1
		S.add(moteNum-1)
	elif 7<moteNum<14:
		moteNum-=2
		S.add(moteNum-2)
	elif 14<moteNum<17:
		moteNum-=3
		S.add(moteNum-3)
	elif 17<moteNum<19:
		moteNum-=4
		S.add(moteNum-4)
	elif 19<moteNum<49:
		moteNum-=5
		S.add(moteNum-5)
	elif 49<moteNum:
		moteNum-=6
		S.add(moteNum-6)
	locations[moteNum]=np.array([float(line[2]),float(line[3])])
	if dataMatrix.size==0:
		dataMatrix=currentDataVec
	else:
		dataMatrix=np.vstack((dataMatrix,currentDataVec)) #NOT DONENENENENENENENE
U=set()
k=10

#create the covariance matrices for each kernel function
#KernelsList=['squared exponential', 'matern', 'rational quadratic']
KernelsList=['squared exponential']
SigmaList=[1, 2, 3]
cov_V_V=dict()
for kernel in KernelsList:
	kernelObj=MI.Kernel(kernel,1,1,1)
	if not kernel=='sample covariance':
		locationsVec=locations.keys() #from up above
		data=MI.distanceMatrix(locations)
	else:
		data=dataMatrix
	kernelObj.store_kernel_matrix(data)
	cov_V_V[kernel]=kernelObj.get_kernel_matrix()

#if 'sample covariance' in cov_V_V.keys():
#	size=cov_V_V['sample covariance'].shape
MI_placement=dict()
MI_placement_locs=dict()
MI_placement_x_locs=dict()
MI_placement_y_locs=dict()
greedy_placement=dict()
greedy_placement_locs=dict()
greedy_placement_x_locs=dict()
greedy_placement_y_locs=dict()
labels=dict()
#im = plt.imread('guestrin_lab.png')
#mplot = plt.imshow(im)
#ax=fig.add_subplot(111)
shapes=['8',',','^']
colors=['r','b','g']
shapes2=['d','h','s']
colors2=['c','m','k']
i=0

#for each kernel, solve the sensor placement problem using MI, and plot the results.
for kernel in cov_V_V.keys():
	labels[kernel]="%s covariance" % (kernel)
	MI_placement[i]=MI.maxMutualInformation(k,cov_V_V[kernel],S,U)
	MI_placement_locs[i]=np.array([])
	MI_placement_x_locs=np.array([])
	MI_placement_y_locs=np.array([])
	for sensor in MI_placement[i]:
		#MI_placement_x_locs=np.append(MI_placement_x_locs,np.array((60.5-locations[sensor][0])*10))
		#MI_placement_y_locs=np.append(MI_placement_y_locs,np.array((locations[sensor][1])*10))
		MI_placement_x_locs=np.append(MI_placement_x_locs,np.array(locations[sensor][0]))
		MI_placement_y_locs=np.append(MI_placement_y_locs,np.array(locations[sensor][1]))

	plt.scatter(MI_placement_x_locs, MI_placement_y_locs, c=colors[i], marker=shapes[i], label=labels[kernel])

	greedy_placement[i]=MI.greedyVariance(k,cov_V_V[kernel],S,U)
	greedy_placement_locs[i]=np.array([])
	greedy_placement_x_locs=np.array([])
	greedy_placement_y_locs=np.array([])
	for sensor in greedy_placement[i]:
		#greedy_placement_x_locs=np.append(greedy_placement_x_locs,np.array((60.5-locations[sensor][0])*10))
		#greedy_placement_y_locs=np.append(greedy_placement_y_locs,np.array((locations[sensor][1])*10))
		greedy_placement_x_locs=np.append(greedy_placement_x_locs,np.array(locations[sensor][0]))
		greedy_placement_y_locs=np.append(greedy_placement_y_locs,np.array(locations[sensor][1]))

	plt.scatter(greedy_placement_x_locs, greedy_placement_y_locs, c=colors2[i], marker=shapes2[i], label=labels[kernel])
	i+=1
	# Put a legend below current axis
	#ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True)
	#box = ax.get_position()
	#ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
	#plt.xlim(0,41)
	#plt.ylim(-1,31)
plt.show()
