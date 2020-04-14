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
def _make_register(amplitudes):
    """
    :param amplitudes:  numpy array of tuples corresponding to the amplitudes of each qubit in the register
    :return register: numpy array of qubits
    """
    size = len(amplitudes)
    q = np.array(amplitudes[0]).view(Qubit)
    for i in range(size - 1):
        q = np.kron(q, np.array(amplitudes[i + 1]).view(Qubit))
    return q.view(Register)


def binaryToDecimal(binary):
    decimal, i, n = 0, 0, 0
    while binary != 0:
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return decimal


def modifyBit(n, p, b):
    mask = 1 << p
    return (n & ~mask) | ((b << p) & mask)


def dec_to_bin(x):
    return int(bin(x)[2:])


bell_state_names = ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus']


# Qubit() with no arguments gives the |0> state by default
# We assume use of the computational basis by default
# NOTE: Qubits will be ROW VECTORS
class Qubit(np.ndarray):

    def __new__(cls, name=None, vec=(1, 0), shape=2):
        """
        :param vec: a tuple of ALPHA and BETA, the amplitudes of states |0> and |1>, respectively
        :param shape: ensures the qubit is a 2D vector (i.e. sets the size of the numpy array to 2x1)
        :return: a quantum state with amplitudes ALPHA and BETA
        """
        valid_names = ['+', '-', 'plus', 'minus']
        if name == 'plus' or name == '+': return _make_qubit(1 / np.sqrt(2), 1 / np.sqrt(2))
        if name == 'minus' or name == '-': return _make_qubit(1 / np.sqrt(2), -1 / np.sqrt(2))
        alpha = vec[0]
        beta = vec[1]
        return _make_qubit(alpha, beta)

    def __init__(self, name, vec=(1, 0)):
        if name == 'plus' or name == '+':
            vec = (1 / np.sqrt(2), 1 / np.sqrt(2))
        if name == 'minus' or name == '-':
            vec = (1 / np.sqrt(2), -1 / np.sqrt(2))
        self.alpha = vec[0]
        self.beta = vec[1]

    def __mul__(self, matrix):
        return np.matmul(self, matrix)

    def __repr__(self):
        nonzero = []
        if self.alpha != 0: nonzero.append(self.alpha)
        if self.beta != 0: nonzero.append(self.beta)
        ret = ""
        for i in range(len(nonzero)):
            ret += '(' + str(nonzero[i]) + ')' + '|' + str(i) + '>'
            if i != len(nonzero) - 1:
                ret += ' + '
        return ret

    def measure(self):
        x = np.random.random()
        if self.alpha <= x:
            return 0
        return 1


class Register(np.ndarray):

    # Returns the |00> state if no parameters are passed.
    # If just SIZE is given, the register returned is the n-length |000...0>
    def __new__(cls, n=None, name=None, qubits=None, amplitudes=None):
        if name in bell_state_names:
            return Register._make_bell_state(name)
        if qubits is not None:
            return _make_register(qubits)
        if amplitudes is not None:
            x = np.log2(len(amplitudes))
            assert x // 1 == x, 'The size of the register should be a power of 2.'
            return np.asarray(amplitudes).view(Register)
        if name is None:
            return _make_register([(1, 0)] * n)

    def __init__(self, n=None, name=None, qubits=None, amplitudes=None):
        self.name = name
        self.n = n
        self.amplitudes = amplitudes
        self.qubits = qubits
        if name in bell_state_names:
            self.name = name
            self.n = 2
        if amplitudes is not None:
            self.n = len(amplitudes)
        if qubits is not None:
            self.n = len(qubits)


    def as_vec(self):
        return np.asarray(self)

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

    # controls on the first (leftmost) qubit and targets the second (second from left) qubit by default
    def CNOT(self, control=1, target=0):
        # modifyBit method does the modification in the reverse order, so we reverse the order of the bitstring,
        # as well as the control and target, inside the method to compensate. Don't think too much about it.
        # I know it's not elegant; go away. It works. Can't that be enough?
        c = target
        t = control
        N = int(np.log2(self.size))
        v = self.as_vec()
        skip = []
        for i in range(2 ** N):
            if i in skip:
                continue
            bitstring = str(dec_to_bin(i)).zfill(N)
            k = binaryToDecimal(int(bitstring[::-1]))
            if bitstring[c] == '1':
                if bitstring[t] == '0':
                    switched = str(dec_to_bin(modifyBit(k, t, 1))).zfill(N)
                    switched = binaryToDecimal(int(switched[::-1]))
                else:
                    switched = str(dec_to_bin(modifyBit(k, t, 0))).zfill(N)
                    switched = binaryToDecimal(int(switched[::-1]))
                skip.append(switched)
                temp = v[i]
                v[i] = v[switched]
                v[switched] = temp
        return v.view(Register)

    @classmethod
    def _make_bell_state(cls, name):
        if name == 'phi_plus':
            x = _make_register([(1, 0), (1, 0)])
        elif name == 'phi_minus':
            x = _make_register([(0, 1), (1, 0)])
        elif name == 'psi_plus':
            x = _make_register([(1, 0), (0, 1)])
        elif name == 'psi_minus':
            x = _make_register([(0, 1), (0, 1)])
        else:
            raise NameError('Name {} '.format(name) + 'is not recognized.')
        H_I = np.kron(H, np.identity(2))
        x = np.matmul(H_I, x)
        register = x.CNOT().view(Register)
        return register

    @classmethod
    def zeros(cls, n):
        return _make_register([(1, 0)] * n)

    @classmethod
    def ones(cls, n):
        return _make_register([(0, 1)] * n)

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
        w = H
        for i in range(self.n - 1):
            w = np.kron(w, H)
        return np.matmul(w, vec)

    def QFT(self):
        const = 1 / np.sqrt((2 ** self.n))
        amps = []
        for k in range(2 ** self.n):
            total = 0
            for p in range(2 ** self.n):
                total += self[p] * np.exp((2 * np.pi * 1j * p * k) / (2 ** self.n))
            amps.append(total)
        amps = np.asarray(amps)
        amps *= const
        return amps.view(Register)
