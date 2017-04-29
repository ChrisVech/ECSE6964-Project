import numpy as np
from ble_scanner import BLScanner
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


def main():

	#pckSize = 75
	labBeaconUUID = '525049494F5400000000000000000000'
	Scanner = BLScanner()
	testLength = 10
	testData = np.zeros([testLength, 4])
	


	# beacon locations
	b1 = [0.,0.]
	b2 = [0., 0.820]
	b3 = [1.12, 0.820]
	b4 = [1.12, 0.]

	b = [b1, b2, b3, b4]

	for j in range(testLength):
		print('resetting data Packet')
		dataPacket = np.zeros([1, 2])
		beaconCnt = np.zeros(4)
		i = 0
		
		for data in Scanner.scan_all():


			dataReading = np.zeros([1,2])
		
			if data[0] == labBeaconUUID:
				dataReading[0,0] = data[2] # beacon number
				dataReading[0,1] = data[4] # RSSI measurement

				dataPacket = np.vstack((dataPacket,dataReading))

				#print(dataPacket)



				beaconCnt[data[2]-1] += 1

				i +=1
		
			if np.all(beaconCnt>= 30):
				print('beaconCOUNT')
				print(beaconCnt)
				print('took this many iterations')
				print(i)
				print( '\n')
				d = RSSIdistance(dataPacket)
				#dataPacket[:,1] = d[:,0] # replace RSSI values with distances
				distEst = distanceEstimate(dataPacket)

				print(distEst)
				print( '\n')

				break

		testData[j,:] = distEst
		j += 1
	
#	print('\nSaving Data ... \n')	
#	np.savetxt('varCalcData.txt', testData, delimiter=',')   # X is an array
#	print(testData)

if __name__ == "__main__":
	main()