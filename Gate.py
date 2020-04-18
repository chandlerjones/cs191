############## VERY VERY UNTESTED REFERENCE CODE! RUN AT YOUR OWN RISK! #############################


from Qubit import *
import numpy as np

# countermeasure for forseeable floating point issues when doing tensor products.
def append_last_p(p):
    return np.append(p, [1.0 - sum(p)])

# Noise class that holds an array of possible transforms and probabilities of each. I is auto 
# generated and need not be included.
class Noise:

    def __init__(self, n, probabilities, transforms):
        """
        :n:             gate dimension
        :probabilities: k vector. k probabilities of each transform. sum(probabilities) < 1.0
        :transforms:    k x 2^n x 2^n ndarray. k transorms of dimension 2^n x 2^n

        No verifications / validations done atm
        """
        self.t = np.concatenate([transforms, [np.eye(2**n)]])
        self.p = probabilities # not adding probability of I due to potential floating point issues
        self.k = len(self.p)
        self.n = n

    def __mul__(self, other):
        """
        :other: The other element...
        """
        if not isinstance(other, Noise):
            raise TypeError('Cannot multiply type Gate with ' + type(other).__name__)

        t = np.kron(self.t, other.t)
        p = np.kron(append_last_p(self.p), append_last_p(other.p))[:-1] # remove I probability because...
        n = self.n + other.n
        return Noise(n, p, t)


    # Randomly chooses a noise transformation to be applied. Watch out for those nasty floating point errors!
    def eval(self):
        """
        :return: transform matrix 2^n x 2^n
        """
        row_i = np.random.choice(len(self.t), p=append_last_p(self.p))
        return self.t[row_i]

# No Noise class. Essentially an I matrix with probability 1
class NoNoise(Noise):
    def __init__(self, n):
        super().__init__(n, np.empty(0), np.empty((0, 2**n, 2**n)))

# Generic Gate class. by default it is Identity with default noise model
class Gate:
    def __init__(self, n, transform = None, noise = None):
        """
        :n:          gate dimension
        :transform:  2^n x 2^n unitary matrix
        :noise:      noise channel to apply after gate

        No verifications / validations done on transform(unitary) matrix atm
        """
        if not noise:
            noise = NoNoise(n)
        if not transform:
            transform = np.eye(n)
        self.u = transform
        self.noise = noise
        self.n = n

    # Tensor product of two gates.
    def __mul__(self, other):
        """
        :other: Its the other element...
        """
        if not isinstance(other, Gate):
            raise TypeError('Cannot multiply type Gate with ' + type(other).__name__)

        u = np.kron(self.u, other.u)
        t = self.noise * other.noise 
        n = self.n + other.n
        return Gate(n, u, t) # had to do it

    # Apply the gate to a given register.
    def apply(self, register):
        """
        :register: Register object to apply gate

        :return: Register returned. Or maybe vector. Same thing....
        """
        if self.noise:
            return self.noise.eval() * self.u * register.as_vec()
        else:
            return self.u * register.as_vec()
