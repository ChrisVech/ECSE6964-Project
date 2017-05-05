import iwlist
import numpy as np
from scipy.optimize import minimize


# objective (cost) function for minimization
def error(position,distanceEstimate):
    
    x = position[0]
    y = position[1]
    d = distanceEstimate
    b = AP_LOC
    # varD = [0.08024316, 0.11061203, 0.02423527, 0.04135387] # from offline data
    # varD = [0.01059502, 0.0054296, 0.01023925, 0.01989047]

    err = 0.0
    
    for i in range(len(d)):

        # regular circle estimate
        err +=  (np.sqrt((b[i][0]- x)**2 + (b[i][1]- y)**2) - d[i])**2

    return err

# objective (cost) function for minimization
def error_weighted(position,distanceEstimate):
    
    x = position[0]
    y = position[1]
    d = distanceEstimate
    b = AP_LOC
    # varD = [0.08024316, 0.11061203, 0.02423527, 0.04135387] # from offline data
    # varD = [0.01059502, 0.0054296, 0.01023925, 0.01989047]

    err = 0.0
    
    for i in range(len(d)):

        # weighted circular method
        err += ((np.sqrt((b[i][0]- x)**2 + (b[i][1]- y)**2) - d[i])**2) / (varD[i])

    return err

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

# Parameters for data collection
NUM_BEACONS = 4
NUM_DB_SAMPLES = 20
NUM_ESTs = 10

# Parameters for distance equation
A = 24.117
n = 1.624
#A = 26.975
#n = 1.167

# Parameters for location estimation
AP_LOC = np.array([ [0,6.91], [5.335,6.35], [5.335,1.40], [0,1.73] ])
CENTER = np.array([ np.mean(AP_LOC[:,0]), np.mean(AP_LOC[:,1]) ])
height = 1.12 #meters



if __name__=='main':
    
    for est_num in range(NUM_ESTs):

        # Collect RSSI data from each access point
        db_data_raw = np.zeros([NUM_BEACONS, NUM_DB_SAMPLES])
        for i in range(NUM_DB_SAMPLES):
            points = iwlist.scan('wlan0')
            cells = iwlist.parse(points)
            for j in range(len(cells)):
                if cells[j]['essid'][0:6] == 'IOT-AP':
                    db_data_raw[int(cells[j]['essid'][6:8])-1][i] = int(cells[j]['db'])

        # Filter the raw RSSI values
        db_data = np.zeros(NUM_BEACONS)
        for i in range(NUM_BEACONS):
            #db_data[i] = np.median(db_data_raw[i])         #median
            db_data[i] = kalmanFilterRSSI(db_data_raw[i])  #kalman filter

        # Convert RSSI values to distance estimates
        sphr_dist_data = np.exp((-A-db_data)/(10*n))
        circ_dist_data = np.zeros(NUM_BEACONS)
        for i in range(NUM_BEACONS):
            if sphr_dist_data[i] > height:
                circ_dist_data[i] = np.sqrt( (sphr_dist_data[i]*sphr_dist_data[i]) - (height**2) )
            else:
                circ_dist_data[i] = 0

        # Compute the variance of the data
        sphr_dist_data_raw = np.exp((-A-db_data_raw)/(10*n))
        circ_dist_data_raw = np.zeros([NUM_BEACONS, NUM_DB_SAMPLES])
        for i in range(NUM_BEACONS):
            for j in range(NUM_DB_SAMPLES):
                if sphr_dist_data_raw[i][j] > height:
                    circ_dist_data_raw[i][j] = np.sqrt( (sphr_dist_data_raw[i][j]*sphr_dist_data_raw[i][j]) - (height**2) )
                else:
                    circ_dist_data_raw[i][j] = 0
        varD = np.zeros(NUM_BEACONS)
        for i in range(NUM_BEACONS):
            varD[i] = np.var(circ_dist_data_raw[i])
            if varD[i] < 0.0001:
                varD[i] = 0.01

        # Estimate the position
        pos_est = minimize(error, CENTER, args=circ_dist_data, method='CG', options={'gtol':1e-6, 'disp':False})
        pos_est_weighted = minimize(error_weighted, CENTER, args=circ_dist_data, method='CG', options={'gtol':1e-6, 'disp':False})

        # Print results
        print '\n'*100
        for i in range(NUM_BEACONS):
            print 'AP'+str(i+1)+': '+str(db_data_raw[i])
            print 'AP'+str(i+1)+' filtered RSSI value: '+str(db_data[i])+' dBm'
            print 'AP'+str(i+1)+' estimated distance:  '+str(circ_dist_data[i])+' meters'
            print 'AP'+str(i+1)+' variance:            '+str(varD[i])+' meters'
            print

        #print('\nPosition Esitmate from WiFi Localization:\n')
        #print('\tX: %s' % pos_est.x[0])
        #print('\tY: %s \n\n' % pos_est.x[1])
        
        print 'WiFi Estimate #' + str(est_num+1)
        print str(pos_est.x[0])+','+str(pos_est.x[1])+','+str(pos_est_weighted.x[0])+','+str(pos_est_weighted.x[1])
