# ECSE 6964 - Internetworking of Things
# Final Project - Localization

# Preliminary Testing with BLE
# Mitchell Phillips 661060944
# Chris Ve

# PEP8 Styling 2 spaces per indentation
# Last edited April 4, 2017

# Import Libraries
import math, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint

labBeaconUUID = str("['525049494F5400000000000000000000',")

def main():
  data = pd.read_csv(
  	'iot_blu_test_2_switchON.txt', sep=" ", names=[
  	'UUID', 'MAJOR', 'MINOR', 'TXPOWER', 'RSSI'])
  print(data)
  
  # filter for only lab beacons
  labBeacons = data.loc[data['UUID'] == labBeaconUUID]
  print(labBeacons)
  
  # note the MINORs
  print(labBeacons.MINOR.unique())

if __name__ == "__main__":
  main()
