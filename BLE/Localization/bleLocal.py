## Localization using BLE Beacons
# ECSE 6964 - Internetworking of Things
# Final Project - Localization

# Using Least Squares for Triangulation
# Mitchell Phillips 661060944
# Chris Ve

# PEP8 Styling with tabs (4 spaces per indentation)
# Last edited April 12, 2017

# Import Libraries
import math, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint

# Based on the setting the equation which is based on measurements:
# Y = AX
# X = (A'A)^(-1)A'Y
# Need to choose weighting matrix W. Theory suggests that when the 
# measurement obtains the inverse of matrix of error variance, the 
# estimated error variance will be the smallest. 

## Using Weight Circular Alorithum
# Based on the circular posistioning technique, but introduces a different
# weight fo each measurement.

# The error in the distance estimation for anchor node i is given by:
#ei = di - di_avg = sqrt((xi - x)^2 + (yi - y)^2) - di_avg

# Need to minimize the weight least squares error criterion,
#eps = e'*S^(-1)*e   '

# where S is the covariance matrix of the random vector
#e = [e1 e2 e3 ........e_N]''

# Assume that the errors ei in the meassurements of the sitances to different
# reference nodes are independent, S is a diagonal matrix with diagonal 
# elements [S]ij = Var(ei), thus the error to be minimized is

# eps = e'*S^(-1)*e   ' = sum from i=1 to N of ei^2 / Var(ei)
#     == sum from i=1 to N of 1// Var(di)


# Read in data packets from bluetooth beacons.

# Parce Bluetooth data packets for data and beacons of interest.
def packetRSSI():

	data = pd.read_csv(
    	'iot_blu_test_2_switchON.txt', sep=" ", names=[
    	'UUID', 'MAJOR', 'MINOR', 'TXPOWER', 'RSSI'])
  
	# Filter for only lab beacons.
 	labBeaconUUID = str("['525049494F5400000000000000000000',")
 	labBeacons = data.loc[data['UUID'] == labBeaconUUID]
	print(labBeacons)

	# Return becacon minor number and RSSI Value.
	minor = np.array(labBeacons['MINOR'])
	for i in range(len(minor)):
		minor[i] = (minor[i].replace(',',''))
	minor = minor.astype(np.float)
	minor = np.reshape(minor,(len(minor),1))

	RSSI = np.array(labBeacons['RSSI'])
	for i in range(len(RSSI)):
		RSSI[i] = (RSSI[i].replace(',',''))
		RSSI[i] = (RSSI[i].replace(']',''))
	RSSI = RSSI.astype(np.float)
	RSSI = np.reshape(RSSI,(len(RSSI),1))

	pckRSSI = np.concatenate((minor, RSSI), axis=1)
	
	return pckRSSI


def RSSIdistance(pckRSSI):
	

def main():
	pckRSSI = packetRSSI()

if __name__ == "__main__":
	main()