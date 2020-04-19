import numpy as np
from Qubit import *
from math import ceil, log, sqrt
from collections import Counter




#main; N is number to factor
def main(N, attempts=1):

	#quick check
	# if N % 2 == 0:
	# 	return 2


	a = np.random.randint(1, N)
	print("The random number chosen is {}".format(a))

	# if euclid_alg(a, N) == 1:
	# 	return a

	K, n = ceil(log(N**2, 2)), ceil(log(N, 2))
	Q = 2**K
	source = Register(K)
	source = source.walsh() #can also use qft; walsh slightly faster & doesnt introduce complex

	vals = []
	for q in range(Q):
		b = (a**q) % N
		vals.append(b)
	tally = Counter(vals)
	amps = []
	for i in range(2**n):
		amps.append(sqrt(tally.get(i, 0)/Q))
	target = Register(amplitudes=amps)

	r = target.measure()

	amps = 2**n * [0]
	amps[r] = 1

	target = Register(amplitudes=amps)

	amps = Q*[0]
	for q in range(Q):
		b = (a**q) % N
		if b == r:
			count += 1
			amps[q] = 1
	amps = [sqrt(1/count) * x for x in amps]
	source = Register(amplitudes=amps)






	return source, target




#credit to https://www.geeksforgeeks.org/python-program-for-basic-and-extended-euclidean-algorithms-2/
def euclid_alg(a, b, x=1, y=1):
	if a == 0 :
		x = 0
		y = 1
		return b
	x1 = 1
	y1 = 1
	gcd = euclid_alg(b%a, a, x1, y1)
	x = y1 - (b/a) * x1
	y = x1
	return gcd
