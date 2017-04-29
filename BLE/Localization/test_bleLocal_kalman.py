import numpy as np
from ble_scanner import BLScanner
from time import sleep


def RSSIdistance(pckRSSI):
	
	# tune parameters
	A = 60 #62 # reference recieved signal strength, [dBm]
	n = 1.60 #1.40 # signal propagation constant
	pckRSSI = np.reshape(pckRSSI,(len(pckRSSI),1))

	dist = np.exp(-A/(10*n) - (pckRSSI[:,0]/(10*n))) # [m]
	dist = np.reshape(dist,(1,len(dist)))

	return dist

def kalmanFilterRSSI(beaconRSSI):
	
	i = len(beaconRSSI)
	z = beaconRSSI

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

	for k in range(1,i):
	    
	    # time update
	    xhat_last[k] = xhat[k-1]
	    P_last[k] = P[k-1]+Q
		
		# measurement update
	    K[k] = P_last[k]/( P_last[k]+R )
	    xhat[k] = xhat_last[k]+K[k]*(z[k]-xhat_last[k])
	    P[k] = (1-K[k])*P_last[k]

	#print(xhat[-1])
	return xhat[-1]

def filter(pckRSSI):

	filtRSSI = np.zeros([len(pckRSSI), 4])
	for i in range(4):
		ind = np.where(pckRSSI[:,0]==(i+1))
		filtRSSI[ind,i] = pckRSSI[ind,1]

	RSSI_est = np.zeros([4])
	#print(RSSI_est)
	for i in range(4):
		beaconRSSI = filtRSSI[:,i]
		beaconRSSI = beaconRSSI[beaconRSSI!=0]
		RSSI_est[i] = kalmanFilterRSSI(beaconRSSI)
	return RSSI_est


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

	pckSize = 100
	labBeaconUUID = '525049494F5400000000000000000000'
	Scanner = BLScanner()
	testLength = 20
	testData = np.zeros([testLength, 4])


	# beacon locations
	b1 = [0.,0.]
	b2 = [0., 0.820]
	b3 = [1.12, 0.820]
	b4 = [1.12, 0.]

	b = [b1, b2, b3, b4]

	for j in range(testLength):

		dataPacket = np.zeros([pckSize, 2])
		i = 0
		
		for data in Scanner.scan_all():
		
			if data[0] == labBeaconUUID:
				dataPacket[i,0] = data[2]
				dataPacket[i,1] = data[4]
				i +=1

			if i == pckSize:

				filtPacket = filter(dataPacket)
				filtPacket = np.reshape(filtPacket,(len(filtPacket),1))
				#print(filtPacket)
				distEst = RSSIdistance(filtPacket)
				print(distEst[0])
				
				break

		testData[j,:] = distEst
		j += 1
	

if __name__ == "__main__":
	main()