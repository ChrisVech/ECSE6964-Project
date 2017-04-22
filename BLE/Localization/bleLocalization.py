## Localization using Four BLE Beacons

# ECSE 6964 - Internetworking of Things
# Final Project - Localization

# Mitchell Phillips - 661060944
# Chris V


# import libraries
import numpy as np
from ble_scanner import BLScanner
from scipy.optimize import minimize


# BLE beacon parameters
def beacons():
    
    # beacon locations
    # b1 = [-0.56, -0.41]
    b1 = [0.0,0.0]
    # b2 = [-0.56, 0.41]
    b2 = [0.0, 0.820]
    # b3 = [0.56, 0.41] 
    b3 = [1.12, 0.820]
    # b4 = [0.56, -0.41] 
    b4 = [1.120, 0.0]
    
    return [b1, b2, b3, b4]


# convert RSSI value to distance values
def RSSIdistance(pckRSSI):
	
	# tune parameters
	A = 62 # reference recieved signal strength, [dBm]
	n = 1.4 # 1.40 # signal propagation constant
	dist = np.exp(-A/(10*n) - (pckRSSI[:,1]/(10*n))) # [m]
	dist = np.reshape(dist,(len(dist),1))

	return dist


# filter distance values to produce distance estimate 
def distanceEstimate(pckRSSI):

	dist = np.zeros([len(pckRSSI), 4])
	for i in range(4):
		ind = np.where(pckRSSI[:,0]==(i+1))
		dist[ind,i] = pckRSSI[ind,1]

	distEst = np.zeros(4)
	for i in range(4):
		beaconDist = dist[:,i]
		beaconDist = beaconDist[beaconDist!=0]
		distEst[i] = np.median(beaconDist)

	return distEst


# ojective (cost) function for minimization
def error(position,distanceEstimate):
    
    x = position[0]
    y = position[1]
    d = distanceEstimate
    b = beacons()
    varD = [0.08024316, 0.11061203, 0.02423527, 0.04135387]
    
    err = 0.0
    
    for i in range(len(d)):
        # err +=  (np.sqrt((b[i][0]- x)**2 + (b[i][1]- y)**2) - d[i])**2
    	err += ((np.sqrt((b[i][0]- x)**2 + (b[i][1]- y)**2) - d[i])**2
    		) / (varD[i])
    return err


def main():

	pckSize = 100 # number of readings per estimation
	labBeaconUUID = '525049494F5400000000000000000000'
	Scanner = BLScanner()
	testLength = 200 # total number of estimations
	testData = np.zeros([testLength, 4]) # initialize array to store estimates

	# repeat for however many number of desired estimations
	for j in range(testLength):

		dataPacket = np.zeros([pckSize, 2]) # initalize single estimate
		i = 0
		
		# run ble scanner
		for data in Scanner.scan_all():
			
			# collect information concerning only lab beacons
			if data[0] == labBeaconUUID:
				dataPacket[i,0] = data[2] # store minor (beacon) number
				dataPacket[i,1] = data[4] # store RSSI value
				i +=1
			
			# execute when sample size of estimates is met
			if i == pckSize:

				d = RSSIdistance(dataPacket)
				dataPacket[:,1] = d[:,0] # replace RSSI values with distances

				# filter distance values to produce an estimation
				distEst = distanceEstimate(dataPacket)
				distEst = np.reshape(distEst,(len(distEst)),1)
				print(distEst)
				print('\n\nNow estimating (x,y) corrdinate...\n')

				# minimization
				positionInitial = np.array([0.5, 0.5]) # inital location guess
				positionInitial = np.reshape(positionInitial,\
					(len(positionInitial),1))
				
				positionEstimate = minimize(error,positionInitial,\
					args=(distEst),method='CG',\
					options={'gtol': 1e-6, 'disp': True})
				
				print('\nPosition Esitmate from BLE Localization:\n')
				print('\tX: %s' % positionEstimate.x[0])
				print('\tY: %s \n\n' % positionEstimate.x[1])
				break

		testData[j,:] = distEst
		j += 1


if __name__ == "__main__":
	main()