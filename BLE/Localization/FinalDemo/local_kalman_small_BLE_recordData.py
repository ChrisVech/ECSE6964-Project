## Localization using Four BLE Beacons
# Kalman Filtering
# Half Work Area

# ECSE 6964 - Internetworking of Things
# Final Project - Localization

# Mitchell Phillips - 661060944
# Chris V

# Last Edited: April 29, 2017


# import libraries
import numpy as np
from ble_scanner import BLScanner
from scipy.optimize import minimize


# BLE beacon parameters
def beacons():
    
    # beacon locations - reduced work space
    # b1 = [0.00, 0.00]
    # b2 = [0.00, 0.55]
    # b3 = [0.80, 0.55]
    # b4 = [0.80, 0.00]

	# beacon locations - full work space
    b1 = [0.0,0.0]
    b2 = [0.0, 0.820]
    b3 = [1.120, 0.820]
    b4 = [1.120, 0.0]
    
    return [b1, b2, b3, b4]


# convert RSSI value to distance values
def RSSIdistance(pckRSSI):
	
	# tune parameters
	A = 60 # reference recieved signal strength, [dBm]
	n = 1.40 # signal propagation constant

	pckRSSI = np.reshape(pckRSSI,(len(pckRSSI),1)) # reshape to col vector

	dist = np.exp(-A/(10*n) - (pckRSSI[:,0]/(10*n))) # [m]
	dist = np.reshape(dist,(1,len(dist))) # reshape to row vector

	return dist[0]


# 1D Kalman Filter - Based off scipy cookbook example
def kalmanFilterRSSI(beaconRSSI):
	
	i = len(beaconRSSI) # store the length of data to be filtered
	z = beaconRSSI # noisy date measurement

	# QR matricies can be tuned. Typically diagonal matrices.
	Q = 1e-5 # process covarience matrix
	R = 0.1 # measurement covarience  

	xhat = np.zeros(i)      # state estimate
	P = np.zeros(i)         # state covarience estimate
	xhat_last = np.zeros(i) # last state estimate
	P_last = np.zeros(i)    # last state covarience estimate
	K = np.zeros(i)         # kalman gain

	# intial guesses
	xhat[0] = 0.0
	P[0] = 1.0

	# measurement and state updates
	for k in range(1,i):
	    
	    # state update
	    xhat_last[k] = xhat[k-1]
	    P_last[k] = P[k-1]+Q
		
		# measurement update
	    K[k] = P_last[k]/( P_last[k]+R )
	    xhat[k] = xhat_last[k]+K[k]*(z[k]-xhat_last[k])
	    P[k] = (1-K[k])*P_last[k]

	# return the last estimate. Can try to return the median if constant.
	return xhat[-1]

# filtering procedure to sift through data a grab beacon information
def filter(pckRSSI):

	filtRSSI = np.zeros([len(pckRSSI), 4])
	
	for i in range(4):
		ind = np.where(pckRSSI[:,0]==(i+1))
		filtRSSI[ind,i] = pckRSSI[ind,1]

	RSSI_est = np.zeros([4])
	
	for i in range(4):
		beaconRSSI = filtRSSI[:,i]
		beaconRSSI = beaconRSSI[beaconRSSI!=0]
		RSSI_est[i] = kalmanFilterRSSI(beaconRSSI)
	
	return RSSI_est


# ojective (cost) function for minimization
def error(position,distanceEstimate):
    
    x = position[0]
    y = position[1]
    d = distanceEstimate
    b = beacons()
    # varD = [0.08024316, 0.11061203, 0.02423527, 0.04135387] # from offline data
    # varD = [0.01059502, 0.0054296, 0.01023925, 0.01989047]

    err = 0.0
    
    for i in range(len(d)):

    	# regular circle estimate
        err +=  (np.sqrt((b[i][0]- x)**2 + (b[i][1]- y)**2) - d[i])**2

        # weighted circular method
    	# err += ((np.sqrt((b[i][0]- x)**2 + (b[i][1]- y)**2) - d[i])**2) / (varD[i])

    return err


def main():

	# pckSize = 100 # number of readings per estimation
	labBeaconUUID = '525049494F5400000000000000000000'
	Scanner = BLScanner()
	testLength = 25 # total number of estimations
	testData = np.zeros([testLength, 4]) # initialize array to store estimates

	# repeat for however many number of desired estimations
	for j in range(testLength):

		dataPacket = np.zeros([1, 2])
		beaconCnt = np.zeros(4)

		i = 0
		
		# run ble scanner
		for data in Scanner.scan_all():

			dataReading = np.zeros([1,2])
			
			# collect information concerning only lab beacons
			if data[0] == labBeaconUUID:

				# wack filtering
				if (data[4]<-25) and (data[4]>-75) : 
					dataReading[0,0] = data[2] # store minor (beacon) number

					if data[2] == 4:
						data[4] = data[4] + 5

					dataReading[0,1] = data[4] # store RSSI value



					 # if (dataReading[0,0] != 4) or \
					 # 	 (dataReading[0,0] ==4 and dataReading[0,1] > -75): 
					
					dataPacket = np.vstack((dataPacket,dataReading))
					beaconCnt[data[2]-1] += 1
					i +=1 # iteration counter for reference
				
			# execute when sample size of estimates is met
			if np.all(beaconCnt>= 30):

				# filter data packet

				filtPacket = filter(dataPacket)
				print('\nKalman RSSI Estimate:')
				print(filtPacket)

				filtPacket = np.reshape(filtPacket,(len(filtPacket),1))
				distEst = RSSIdistance(filtPacket)
				print('\nDistance Estimate:')
				print(distEst)
				
				# minimization

				print('\nNow estimating (x,y) corrdinate...\n')
				
				positionInitial = np.array([0.40, 0.225]) # inital location guess
				positionInitial = np.reshape(positionInitial,\
					(len(positionInitial),1))
				
				positionEstimate = minimize(error,positionInitial,\
					args=(distEst),method='CG',\
					options={'gtol': 1e-6, 'disp': True})
				
				print('\nPosition Esitmate from BLE Localization:\n')
				print('\tX: %s' % positionEstimate.x[0])
				print('\tY: %s \n\n' % positionEstimate.x[1])

				# determine quad in-

				quadLoc = 'Z'

				b = beacons()

				if positionEstimate.x[0] < (b[2][0])/2.:
					if positionEstimate.x[1] < (b[2][1])/2.:
						quadLoc = 'A'
					else:
						quadLoc = 'B'
				else:
					if positionEstimate.x[1] < (b[2][1])/2.:
						quadLoc = 'D'
					else:
						quadLoc = 'C'

				print('\nPi is in Quadrant: %s' % quadLoc)

				break




		testData[j,:] = positionEstimate.x[0]

	print('\nSaving Data ... \n')	
	np.savetxt('beaconX_Y_.txt', testData, delimiter=',') 
	print(testData)

if __name__ == "__main__":
	main()