#!/usr/bin/python

import MI_sensorPlacement as MI

files=['data.txt']
parser=MI.Parsing(files)
start=20
end=63020
binSize=100
#parser.averagedData(start,binSize,end)
dataYes=open('averagedGuestrinDataFile.txt')
data=dataYes.readlines() #need to get those \n's out!
#also need to work on putting locs into text file, for quick usage of sensor placement.
print data
