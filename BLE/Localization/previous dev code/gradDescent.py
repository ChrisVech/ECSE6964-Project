import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from pprint import pprint

def gradientDescent(b,distEst,currPos):

	x = currPos[0]
	y = currPos[1]
	#print(x)
	#print(y)

	alpha = 0.005 # learning rate

	e_dx = 0.;
	e_dy = 0.;
	for i in range(len(distEst)):
		#print('beacon')
		e_dx += -2* np.divide(((b[i][0]-x)*(np.sqrt((b[i][0]-x)**2+(b[i][1]-y)**2)-distEst[i])**2),(np.sqrt((b[i][0]-x)**2+(b[i][1]-y)**2)))
		#print(e_dx)
		e_dy += -2*np.divide(((b[i][1]-y)*(np.sqrt((b[i][0]-x)**2+(b[i][1]-y)**2)-distEst[i])**2),(np.sqrt((b[i][0]-x)**2+(b[i][1]-y)**2)))
		#print(e_dy)
	new_x = x - (alpha * e_dx)
	new_y = y - (alpha * e_dy)

	newPos = np.array([new_x,new_y])
	# print(newPos.shape)
	# print(newPos)
	# print('yuck')
	# print(new_x)
	# print(new_y)
	return newPos

# Parce Data
data = pd.read_csv('test02.txt', sep=",", header=None)
data = np.array(data)
print(data)

distEst = data[1]
print(distEst)

tol = 1e-4
currPos = np.array([[0.3],[0.5]]) # initalize position estimate

# beacon locations
b1 = [0.,0.]
b2 = [0., 0.820]
b3 = [1.12, 0.820]
b4 = [1.12, 0.]

b = [b1, b2, b3, b4]

while True:
	newPos = gradientDescent(b,distEst,currPos)
	# print('loop')
	# print(newPos)
	if abs(newPos[0]-currPos[0])<tol and abs(newPos[1]-currPos[1])<tol:
		print(abs(newPos-currPos).all()<tol)
		print('lets go')
		print(newPos)
		print(currPos)
		break
	else:

		print('nope')
		print(currPos)
		print(newPos)
		currPos = newPos

posEstimate = newPos
print('Position Estimate:')
print(posEstimate)