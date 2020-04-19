import numpy as np
from Qubit import *
from math import ceil, log, sqrt
from collections import Counter
from statistics import mode


"""Simulation of Shor's Algorithm based off of the "Register Class" written by Chandler Jones.
Some code below is not used in the actual "implementation" but still written to remain faithful
to the actual steps of the algorithm

Author: Harrison Costantino"""



#Main loop; N is number to factor
def main(N, attempts=None):

	#quick check of small primes
	#turned off to demonstrate quantum pieces of alg
	if False:
		if N % 2 == 0:
			return 2
		elif N % 3 == 0:
			return 3
		elif N % 5 == 0:
			return 5

	if not attempts:
		attempts = int(log(N, 2))

	it = attempts + 1
	guesses = []
	while attempts:
		print("Iteration {}".format(it - attempts))
		guess = shors_alg(N)
		if guess:
			guesses.append(guess)
		attempts -= 1
	factor = mode(guesses)

	return factor


#Credit to https://www.geeksforgeeks.org/python-program-for-basic-and-extended-euclidean-algorithms-2/
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



def shors_alg(N):

	a = np.random.randint(1, N)

	#Again turned off to focus on quantum aspects of alg; checks to see if factor randomly chosen
	if False:
		if euclid_alg(a, N) != 1:
			return euclid_alg(a, N)

	K, n = ceil(log(N**2, 2)), ceil(log(N, 2))
	Q = 2**K
	source = Register(K)
	source = source.walsh() #can also use qft; walsh slightly faster & doesnt introduce complex
	target = Register(K)

	#Quantum oracle U_f where f(x) = a^x mod N
	vals = []
	for q in range(Q):
		b = (a**q) % N
		vals.append(b)

	#Storing result of oracle in second register
	tally = Counter(vals)
	amps = []
	for i in range(Q):
		amps.append(sqrt(tally.get(i, 0)/Q))
	target = Register(amplitudes=amps)

	#Choosing an order r and setting second register to align with measurement
	r = target.measure()
	amps = 2**n * [0]
	amps[r] = 1
	target = Register(amplitudes=amps)
	#Second register no longer relevant

	#Collapse first register to be consistent with measurement
	total = 0
	amps = Q*[0]
	for q in range(Q):
		b = (a**q) % N
		if b == r:
			total += 1
			amps[q] = 1
	amps = [sqrt(1/total) * x for x in amps]
	source = Register(amplitudes=amps)

	#Apply QFT to first register to bring out the period
	source = source.QFT()

	#Measurement used in finding the period
	C = source.measure()

	#Determining the period
	ratio = C/Q
	r = box_8_1(ratio, Q)




	if not ((r % 2 == 0) and ((a**(r//2) % N) == N-1)):
		print("The random number chosen was {} which resulted in a degenerate case\n".format(a))
		return None



	print("The random number chosen was {} which yielded the guess {}\n".format(a, guess))
	return guess





N = input("Which number would you like to factor?\n")
attempts = input("\n\nHow many iterations of Shor's Algorithm would you like to run?\nMore gives higher probability of success; type 'd' for the default.\n")
if attempts == "d":
	attempts = None
else:
	attempts = int(attempts)

factor = main(int(N), attempts)
print("\n\nWe found the factors {}, {}. There may be others".format(factor, N//factor))
