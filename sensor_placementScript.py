#!/usr/bin/python

import MI_sensorPlacement as MI
import numpy as np
import matplotlib.pyplot as plt
import random

def sensorPlacement(datafile='data.txt', locationfile='mote_locs.txt'):
	
	parser=MI.Parsing(locationfile)
	parsedText=parser.textParsing()
	locations=parsedText[2] #get the possible locations of the sensors
	S=set(locations.keys())
	U=set()
	k=10

	#create the covariance matrices for each kernel function
	KernelsList=['squared exponential', 'matern', 'rational quadratic']
	SigmaList=[1, 2, 3]
	cov_V_V=dict()
	for kernel in KernelsList:
		kernelObj=MI.Kernel(kernel,21,1,1)
		kernelObj.store_kernel_matrix()
		cov_V_V[kernel]=kernelObj.get_kernel_matrix()
	i=0
	placement=dict()
	placement_locs=dict()
	placement_x_locs=dict()
	placement_y_locs=dict()
	labels=dict()
	fig=plt.figure()
	ax=fig.add_subplot(111)
	shapes=['8',',','^']
	colors=['r','b','g']

	#for each kernel, solve the sensor placement problem using MI, and plot the results.
	for kernel in cov_V_V.keys():
		labels[kernel]="%s covariance" % (kernel)
		placement[i]=MI.maxMutualInformation(k,cov_V_V[kernel],S,U)
		placement_locs[i]=np.array([])
		placement_x_locs=np.array([])
		placement_y_locs=np.array([])
		for sensor in placement[i]:
			placement_x_locs=np.append(placement_x_locs,np.array(locations[sensor][0]))
			placement_y_locs=np.append(placement_y_locs,np.array(locations[sensor][1]))
		ax.scatter(placement_x_locs, placement_y_locs, c=colors[i], marker=shapes[i], label=labels[kernel])
		i+=1
		# Put a legend below current axis
		ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True)
		box = ax.get_position()
		ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
	plt.show()
