############## VERY VERY UNTESTED REFERENCE CODE! RUN AT YOUR OWN RISK! #############################


from Qubit import *
import numpy as np

default_noise = None


# countermeasure for forseeable floating point issues when doing tensor products.
def append_last_p(p):
    return np.append(p, [1.0 - sum(p)])

class Noise:
    def __init__(self, n, probabilities, transforms):
        """
        :n: gate dimension
        :probabilities: k vector. k probabilities of each transform. sum(probabilities) < 1.0
        :transforms: k x 2^n x 2^n ndarray. k transorms of dimension 2^n x 2^n

        No verifications / validations done atm
        """
        self.t = np.append(transforms, [np.eye(n**2)])
        self.p = probabilities
        self.k = len(self.p)
        self.n = n

    def __mul__(self, other):
        if not isinstance(other, Noise):
            raise TypeError('Cannot multiply type Gate with ' + type(other).__name__)

        self.t = np.kron(self.t, other.t)
        self.p = np.kron(append_last_p(self.p), append_last_p(other.p))[:-1]
        self.k = len(self.p)
        self.n += other.n

    
    def eval(self):
        """
        Randomly chooses a noise transformation to be applied. Auto gen an I transform if no 
        transform is selected. Watch out for those nasty floating point errors!

        :return: transform matrix 2^n x 2^n
        """
        row_i = np.random.choice(len(self.t), p=append_last_p(self.p))
        return self.t[row_i]



class Gate:
    def __init__(self, n, transform = np.eye(2), noise = default_noise):
        """
        :n:          gate dimension
        :transform:  2^n x 2^n unitary matrix
        :noise:      noise channel to apply after gate

        No verifications / validations done on transform(unitary) matrix atm
        """
        self.u = transform
        self.noise = noise
        self.n = n

    def __mul__(self, other):
        """
        Tensor product of two gates.
        """
        if not isinstance(other, Gate):
            raise TypeError('Cannot multiply type Gate with ' + type(other).__name__)

        self.u = np.kron(self.u, other.u)
        self.noise = self.noise * other.noise
        self.n += other.n

    def apply(self, register):
        """
        Apply the gate to a given register.

        :register: Register object to apply gate

        :return: Register returned. Or maybe vector. Same thing....
        """
        return self.noise.eval() * self.u * register.as_vec()
