import numpy as np

# Hadamard Gate
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])

# X, Y, Z Pauli Matrices
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])


# Constructs a qubit using numpy array architecture.
def _make_qubit(alpha, beta):
    """
    :param alpha: amplitude corresponding to |0>
    :param beta: amplitude corresponding to |1>
    :return qubit: numpy array with entries alpha and beta
    """
    Q = np.zeros(2)
    Q[0] = alpha
    Q[1] = beta
    return Q.view(Qubit)


# Constructs a quantum register using a numpy array of QUBIT objects
def _make_register(size, amplitudes):
    """
    :param size: the length of the register
    :param amplitudes:  numpy array of tuples corresponding to the amplitudes of each qubit in the register
    :return register: numpy array of qubits
    """
    q = np.array(amplitudes[0]).view(Qubit)
    for i in range(size - 1):
        q = np.kron(q, np.array(amplitudes[i + 1]).view(Qubit))
    return q.view(Register)


def dec_to_bin(x):
    return int(bin(x)[2:])


# Qubit() with no arguments gives the |0> state by default
# We assume use of the computational basis by default
# NOTE: Qubits will be ROW VECTORS
class Qubit(np.ndarray):

    def __new__(cls, vec=(1, 0), shape=2):
        """
        :param vec: a tuple of ALPHA and BETA, the amplitudes of states |0> and |1>, respectively (default |0>)
        :param shape: ensures the qubit is a 2D vector (i.e. sets the size of the numpy array to 2x1)
        :return: a quantum state with amplitudes ALPHA and BETA
        """
        alpha = vec[0]
        beta = vec[1]
        return _make_qubit(alpha, beta)

    def __init__(self, vec=(1, 0)):
        self.alpha = vec[0]
        self.beta = vec[1]

    def __mul__(self, matrix):
        return np.matmul(self, matrix)

    def measure(self):
        x = np.random.random()
        if self.alpha <= x:
            return 0
        return 1


class Register(np.ndarray):

    # Returns the |00> state if no parameters are passed.
    # If just SIZE is given, the register returned is the n-length |000...0>
    def __new__(cls, name=None, size=2):
        bell_state_names = ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus']
        if name in bell_state_names:
            return Register._make_bell_state(name)
        return _make_register(size, [(1, 0)] * size)

    def __init__(self, size=2):
        self.n = size

    def as_vec(self):
        return np.asarray(self).view(Register)

    # Changes the representation of the Register to KET sum formalism
    # (e.g. (a_1)|000...> + (a_2)|00...01> + ... + (a_2^n)|111...1> )
    def __repr__(self):
        N = int(np.log2(self.size))
        nonzero_indices = []
        for i in range(self.size):
            if self[i] != 0:
                nonzero_indices.append(i)
        bins = [dec_to_bin(i) for i in nonzero_indices]
        ret = ""
        for i in range(len(bins)):
            ret += ('(' + str(self[nonzero_indices[i]]) + ')' + '|' + str(bins[i]).zfill(N) + '>')
            if i != len(bins) - 1:
                ret += ' + '
        return ret

    # controls on the first (leftmost) qubit by default
    def CNOT(self, control=0):
        if control == 1:
            CNOT = np.array([[1, 0, 0, 0],
                             [0, 0, 0, 1],
                             [0, 0, 1, 0],
                             [0, 1, 0, 0]])
        else:
            CNOT = np.array([[1, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 0, 1],
                             [0, 0, 1, 0]])
        return np.matmul(CNOT, self)

    @classmethod
    def zeros(cls, n):
        return _make_register(n, [(1, 0)] * n)

    @classmethod
    def ones(cls, n):
        return _make_register(n, [(0, 1)] * n)

    @classmethod
    def _make_bell_state(cls, name):
        if name == 'phi_plus':
            x = _make_register(2, [(1, 0), (1, 0)])
        elif name == 'phi_minus':
            x = _make_register(2, [(0, 1), (1, 0)])
        elif name == 'psi_plus':
            x = _make_register(2, [(1, 0), (0, 1)])
        elif name == 'psi_minus':
            x = _make_register(2, [(0, 1), (0, 1)])
        else:
            raise NameError('Name {} '.format(name) + 'is not recognized.')
        H_I = np.kron(H, np.identity(2))
        x = np.matmul(H_I, x)
        x = np.matmul(x.CNOT())
        return x

    @classmethod
    def as_register(cls, x):
        if type(x) is not np.ndarray and type(x) is not list:
            raise TypeError('Cannot convert {}'.format(type(x)) + 'to Register.'
                                                                  ' Data type must be Python list or numpy ndarray.')
        x = np.asarray(x)
        if np.linalg.norm(x) != 1:
            raise ValueError('Cannot convert to Register. Squared amplitudes must sum to 1.')
        return x.view(Register)

    # Performs Walsh-Hadamard on the register
    def walsh(self):
        vec = self.reshape(2 ** self.n)
        w = np.array([[1, 1], [1, -1]])
        for i in range(self.n - 1):
            w = np.kron(w, H)
        return (1 / np.sqrt(2) ** self.n) * np.matmul(w, vec)