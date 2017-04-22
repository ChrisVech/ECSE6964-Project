import numpy as np

A = np.array([[1.],[5.]])
B = np.array([[2.],[4.]])
print(A)
print(B)
print(A.shape)
print(B.shape)

C = abs(A - B)
print(C)

if abs(A-B).all()< 2:
	print('yo')