# using scipy cookbook example
# 1D kalman filter
# http://scipy-cookbook.readthedocs.io/items/KalmanFiltering.html

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('kalData.txt', sep=",", header=None) # beacon 1 at 1 m away
data = np.array(data)
RSSI = data[:,1]

# intial parameters
i = len(RSSI)

x = -62 # truth value (typo in example at top of p. 13 calls this z)
z = RSSI # observations (normal about x, sigma=0.1)

Q = 1e-5 # process covarience matrix
R = 0.1 # measurement covarience  

# allocate space for arrays
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

plt.figure()
plt.plot(z,'k+',label='RSSI Measurement')
plt.plot(xhat,'b-',label='Kalman Estimate')
plt.axhline(x,color='g',label='Ground Truth')
plt.legend()
plt.title('Kalman Filter for Beacon 1 @ 1m Away', fontweight='bold')
plt.xlabel('Data Sample')
plt.ylabel('RSSI')

plt.show()