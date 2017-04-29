import numpy as np
from ble_scanner import BLScanner
from time import sleep


# def RSSIdistance(pckRSSI):
	
# 	# tune parameters
# 	A = 62 # reference recieved signal strength, [dBm]
# 	n = 1.40 # signal propagation constant
# 	dist = np.exp(-A/(10*n) - (pckRSSI[:,1]/(10*n))) # [m]
# 	dist = np.reshape(dist,(len(dist),1))

# 	return dist


# def distanceEstimate(pckRSSI):

# 	dist = np.zeros([len(pckRSSI), 4])
# 	for i in range(4):
# 		ind = np.where(pckRSSI[:,0]==(i+1))
# 		dist[ind,i] = pckRSSI[ind,1]

# 	distEst = np.zeros([4])
# 	for i in range(4):
# 		beaconDist = dist[:,i]
# 		beaconDist = beaconDist[beaconDist!=0]
# 		distEst[i] = np.median(beaconDist)

# 	return distEst


def main():

	labBeaconUUID = '525049494F5400000000000000000000'
	Scanner = BLScanner()
	testLength = 500
	dataPacket = np.zeros([testLength, 2])
	beacon = 1
	i = 0


	
		
	for data in Scanner.scan_all():
		#print(data)
		if data[0] == labBeaconUUID and data[2] == beacon:
			dataPacket[i,0] = data[2]
			dataPacket[i,1] = data[4]
			print(dataPacket[i,:])
			i +=1
			if i > testLength-1:
				break

		
	
	print('\nSaving Data ... \n')	
	np.savetxt('kalData.txt', dataPacket, delimiter=',')   # X is an array
	print(dataPacket)

if __name__ == "__main__":
	main()
