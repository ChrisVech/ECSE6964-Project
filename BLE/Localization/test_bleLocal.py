import numpy as np
#from ble_scanner import BLScanner
from time import sleep


def RSSIdistance(pckRSSI):
	
	# tune parameters
	A = 62 # reference recieved signal strength, [dBm]
	n = 1.40 # signal propagation constant
	dist = np.exp(-A/(10*n) - (pckRSSI[:,1]/(10*n))) # [m]
	dist = np.reshape(dist,(len(dist),1))

	return dist


def distanceEstimate(pckRSSI):

	dist = np.zeros([len(pckRSSI), 4])
	for i in range(4):
		ind = np.where(pckRSSI[:,0]==(i+1))
		dist[ind,i] = pckRSSI[ind,1]

	distEst = np.zeros([4])
	for i in range(4):
		beaconDist = dist[:,i]
		beaconDist = beaconDist[beaconDist!=0]
		distEst[i] = np.median(beaconDist)

	return distEst

def circleLocal(distEst, x, y):

	# beacon locations
	b1 = [0,0]
	b2 = [0, 0.820]
	b3 = [1.12, 0.820]
	b4 = [1.12, 0]

	b = [b1, b2, b3, b4]

	# loss function: sum of the squared errors of the distances
	error = 0;
	for i in range(len(distEst)):
		error +=  (sqrt( (b[i][0]- x)**2 + (b[i][1]- x)**2) - distEst[i])**2

def gradientDescent():

	alpha = 0.5 # learning rate

	e_dx = 0.;
	e_dy = 0.;
	for i in range(len(distanceEstimate)):
		e_dx += -2*((b[i][0]-x)*(
			np.sqrt((b[i][0]-x)**2+(b[i][1]-x)**2)-distEst[i])**2)/(
			np.sqrt((b[i][0]-x)**2+(b[i][1]-x)**2))
		e_dx += -2*((b[i][0]-x)*(
			np.sqrt((b[i][0]-x)**2+(b[i][1]-x)**2)-distEst[i])**2)/(
			np.sqrt((b[i][0]-x)**2+(b[i][1]-x)**2))

	new_x = x - (alpha * e_dx)
	new_y = y - (alpha * e_dy)

	if 
	# break when new_x - x is small 
	# break when
	gradientDescent		

def main():

	pckSize = 75
	labBeaconUUID = '525049494F5400000000000000000000'
	Scanner = BLScanner()
	testLength = 20
	testData = np.zeros([testLength, 4])

	# weighted circular path parameter
	x_int = float(0)
	y_int = float(0)
	alpha = 0.1

	for j in range(testLength):

		dataPacket = np.zeros([pckSize, 2])
		i = 0
		
		for data in Scanner.scan_all():
		
			if data[0] == labBeaconUUID:
				dataPacket[i,0] = data[2]
				dataPacket[i,1] = data[4]
				i +=1
		
			if i == pckSize:

				d = RSSIdistance(dataPacket)
				dataPacket[:,1] = d[:,0] # replace RSSI values with distances

				distEst = distanceEstimate(dataPacket)

				print(distEst)

				break

		testData[j,:] = distEst
		j += 1
	
	print('\nSaving Data ... \n')	
	np.savetxt('test.txt', testData, delimiter=',')   # X is an array
	print(testData)

if __name__ == "__main__":
	main()