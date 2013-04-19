#!/usr/bin/python


#BEST_algorithms.py
import random as random
import numpy as np
import math
import scipy.linalg
import itertools
import matplotlib.pyplot as plt


class Parsing(object):

	def __init__(self, filenames):
		self.filenames=filenames

	def textParsing(self):
		data=dict()
		epochVec=dict()
		locations=dict()
		#parsedEpochFile=open('parsedEpochFile.txt', 'w')
		#parsedMoteFile=open('parsedMoteFile.txt','w')

		#specify filename strings ('motelocs.txt')

		for fyle in self.filenames:
			rawData=open(fyle) 
			for line in rawData:
				lineAsList=line.split() #make list of individual strings in line
				#print lineAsList
				if fyle=='data.txt':
					#date=lineAsList[0]
					#time=lineAsList[1]
					epoch=int(lineAsList[2]) #need int for indexing
					moteNum=int(lineAsList[3])-1 #need int for indexing
					moteReading=float(lineAsList[4])
					if not(moteNum==4 or moteNum==14 or moteNum==54 or moteNum==55 or moteNum==57 or moteNum==56 or moteNum==49 or moteNum==19 or moteNum==17 or moteNum==7):
						if moteNum not in data:
							data[moteNum]=[]
						if epoch not in epochVec:
							epochVec[epoch]=[]
						epochVec[epoch].append(moteReading) #data from all sensors per epoch
						data[moteNum].append((moteReading,epoch)) #data from each mote, indexed by moteid
				if fyle=='mote_locs.txt':
					moteNum=int(lineAsList[0].strip())-1
					moteX=float(lineAsList[1].strip())
					moteY=float(lineAsList[2].strip())
					moteXY=np.array([moteX,moteY])
					if moteNum not in locations:
						locations[moteNum]=[]
					locations[moteNum]=moteXY
			#print epochVec.keys()
			#for moteNum in data.keys():
			#	print (moteNum, max([a[0] for a in data[moteNum]))
		return (epochVec,data,locations)


#round up to the maximum time all datasets start (found this epoch to be #20) and round down to the minimum time all datasets end (approx. 63020)
	def averagedData(self, start, binSize, end): #bin size, start time, and end time are in epochs
		datafile=open('averagedGuestrinDataFile.txt', 'w')
		parsedText=self.textParsing()
		data=parsedText[1]
		#print data[15]
		epochVec=parsedText[0]
		numBins=(end-start)/binSize
		binStart=start
		averagedData=dict()
		finalData=dict()
		badIndicesList=[]

		for moteNum in data.keys(): #loop over all motes
			#print moteNum
			for i in range(numBins): #get average for every bin
				binStart=start+i*binSize
				binEnd=start+(i+1)*binSize #epoch the bin ends on
				binContents=[]
				binContents=[a[0] for a in data[moteNum] if binStart<=a[1]<=binEnd] #find the data points that are in our bin
				if len(binContents)>0:
					average=sum(binContents)/float(len(binContents))
					if moteNum not in averagedData:
						averagedData[moteNum]=[]
					averagedData[moteNum].append((average,i)) #append each bin's averaged reading
				else:
					badIndicesList.append(i) #list of indices of bins for which at least one mote doesn't have any readings
				#print binStart
			#print averagedData[moteNum]
		for moteNum in averagedData.keys():
			for readings in averagedData[moteNum]:
				if not readings[1] in badIndicesList:
					if moteNum not in finalData:
						finalData[moteNum]=[]
					finalData[moteNum].append((readings[0],readings[1]))
			datafile.write(str(finalData[moteNum])+'\n')


		




#i'm going to stop working on getting the same data vector sizes for each mote to do "analysis" and 
#start working on finding the distance to create a cov. matrix.


'''
	for i in range(7000):#fix this WRITING!!!
		if len(epochVec[i])==20:
			epochVec[i]=str(epochVec[i])
			timePoints.append(i)
			finalEpochVec[i]=epochVec[i]
			parsedEpochFile.write(epochVec[i]+'\n')
	print timePoints

	for i in range(58):
		for j in timePoints:
			if i not in finalData:
				finalData[i]=[]
			print data[i][j]
			finalData[i].append(data[i][j])
		parsedMoteFile.write(finalData[i]+'\n')
'''
def distanceMatrix():
	fyles=['data.txt','mote_locs.txt']
	parser=Parsing(fyles)
	parsedText=parser.textParsing()
	locations=parsedText[2]
	for i in locations.keys():
		tempDistVec=[]
		for j in locations.keys():
			Norm=(np.linalg.norm(locations[i]-locations[j]))
			tempDistVec.append(Norm)
		tempDistArray=np.array([tempDistVec]) #create a row of distances
		if i==0: # initialize the distance matrix if there's nothing so far
			dists=tempDistArray
		else:
			dists=np.concatenate((dists,tempDistArray),axis=0) #concatenate the row we just created to the bottom of the distance matrix
	return dists





class Kernel(object):

    matrix= np.matrix(float)
    Lambda = 1

    def __init__(self,kernelChoice, Lambda = 1, Sigma=1, Alpha=1):
        self.Lambda = Lambda
        self.Sigma=Sigma
        self.Alpha=Alpha
       	self.kernelChoice=kernelChoice

    def compute_kernel_matrix(self):
        """Computes the kernel matrix between two given x vectors, using a specified kernel"""
        dists=distanceMatrix()
        if self.kernelChoice=='squared exponential':
        	sqExp=((self.Sigma)**2)*np.exp(-(1./2.)*np.square(dists)/(self.Lambda**2))
        	return sqExp
        elif self.kernelChoice=='matern':
        	matern=1+(np.sqrt(5)*dists/(self.Lambda))+((5.*np.square(dists))/(3*(self.Lambda**2)))*np.exp((-np.sqrt(5)*dists)/self.Lambda)
        	return matern
        elif self.kernelChoice=='rational quadratic':
        	rationalQuad=(1+((np.square(dists))/(2*self.Alpha*(self.Lambda**2))))
        	return rationalQuad



    def get_kernel_partitions(self,partition_number,partition_indices,remainder=False):
        """Returns a set of partitions of the kernel matrix.
           Given a partition of indices P*, this function returns 4 matrices:
           K(P*,P*),K(P*,P),K(P,P*),K(P,P)
           where P represents the remaining partitions
        """


        ##UNDERSTAND THIS

        #partion_indices = self.partion_indices  # copy the partions
        pi = list(partition_indices)
        target_inds = pi[partition_number]
        pi.pop(partition_number)
        # Now add the rest of the indices together
        remain_inds = list(itertools.chain(*pi))
        ix1 = np.ix_(target_inds,target_inds)
        ix2 = np.ix_(target_inds,remain_inds)
        ix3 = np.ix_(remain_inds,target_inds)
        ix4 = np.ix_(remain_inds,remain_inds)
        K = self.matrix
        return (K[ix1],K[ix2],K[ix3],K[ix4])

    def store_kernel_matrix(self):
        self.matrix = self.compute_kernel_matrix()
    
    def get_kernel_matrix(self):
        return self.matrix

    def set_Lambda(self,s):
        self.Lambda = s


# implementation assumes that V=S (there are no locations where it's impossible to place a sensor)
#S=set(locations.keys()), the sensor indices (not x,y position)

def maxMutualInformation(k, cov_V_V, S, U):
	A=set() #initialize set of optimally placed sensors A
	#a "sensor" here corresponds to the INDEX of the sensor
	V=S|U
	candidate_values=[]

	for i in range(k):
		A_indices=sorted(A)
		if not len(A)==0:
			cov_A_A=np.vstack([cov_V_V[i,[A_indices]] for i in A_indices]) #make sure this stacks right
			inv_cov_A_A=np.linalg.inv(cov_A_A)
		else:
			cov_A_A=0
			inv_cov_A_A=0
		for y in S-A:
			var_y=cov_V_V[y,y] #moteNums start from 0
			if not len(A)==0:
				cov_y_A=np.array([[cov_V_V[y,a] for a in A_indices]])
				cov_A_y=cov_y_A.T
			else:
				cov_y_A=0
				cov_A_y=0
			Abar=V-(A|{y}) #all sensors besides current candidate sensor and set of optimally placed sensors
			Abar_indices=sorted(Abar)
			cov_y_Abar=np.array([[cov_V_V[y,a] for a in Abar_indices]])
			cov_Abar_y=cov_y_Abar.T
			cov_Abar_Abar=np.vstack([cov_V_V[i,[Abar_indices]] for i in Abar_indices])
			inv_cov_Abar_Abar=np.linalg.inv(cov_Abar_Abar)
			condVar_y_A=var_y-np.dot(cov_y_A, np.dot(inv_cov_A_A,cov_A_y))
			condVar_y_Abar=var_y-np.dot(cov_y_Abar, np.dot(inv_cov_Abar_Abar,cov_Abar_y))
			value=(condVar_y_A)/(condVar_y_Abar)
			candidate_values.append(value)
			best_value=max(candidate_values)
			if best_value==value:
				y_star=y
		A.add(y_star)
		candidate_values=[]
	return A




