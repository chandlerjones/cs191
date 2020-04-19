import numpy
from qiskit_shor import *
# import shors
from qiskit import QuantumCircuit, QuantumRegister
from Qubit import *
from qiskit import IBMQ
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms import Shor


def main():
    print('################################################################')
    print('############ Noiseless Implementation Demonstration ############')
    print('################################################################', '\n')
    print('We begin with single Qubit objects:')
    phi = Qubit()
    print('phi =', phi.__repr__(), '\n')
    print('We can apply transformations such as the Pauli matrices and the Hadamard Gate:')
    px = phi.pauli('X')
    py = phi.pauli('Y')
    pz = phi.pauli('Z')
    ph = phi.Hadamard()
    print('X * phi = ', px.__repr__())
    print('Y * phi = ', py.__repr__())
    print('Z * phi = ', pz.__repr__())
    print('H * phi = ', ph.__repr__(), '\n', '\n')

    print('We now initialize two 3-qubit registers (x and y) to the zero state:')
    x = Register(3)
    y = Register(3)
    print('x =', x.__repr__())
    print('y =', y.__repr__(), '\n')
    print('Create an equal superposition over all of the basis states with register x', '\n',
          ' and take the conjugate transpose of register y to make it a bra:')
    x = x.walsh()
    print('x =', x.__repr__())
    y.bra()
    print('y =', y.__repr__(), '\n')
    print('We expect the purity of x and y to be 1/8 (1/2^n, where n=3) and 1, respectively...')
    print('purity of x: ', x.purity)
    print('purity of y:', y.purity, '\n')
    print('Taking their inner product (bra/ket) should result in a scalar value.', '\n',
          'Taking their outer product (ket/bra) should result in an 8x8 matrix operator, which we omit for brevity',
          '\n')
    p1 = y * x
    p2 = x * y
    print('<y|x> =', p1, '\n')
    # print('|x><y| =', p2, '\n', '\n')

    print('Measuring our register will return the index of the state measured.', '\n'
          'e.g.) if x.measure() returns 4, we have effectively measured the state |100>')
    m = x.measure()
    my = y.measure()
    print('x after measurement: ', m,
          '--> State measured: ', str(dec_to_bin(m)), '\n')
    print('We should observe the zero state with certainty when measuring y:')
    print('y after measurement: ', my, '\n', '\n')

    print('############################################################################')
    print('############ Basic Functionality Tests Against Control (Qiskit) ############')
    print("############################################################################", '\n')

    qis_x = QuantumCircuit(2, 2)
    qis_x.h(0)
    qis_x.cx(0, 1)
    qis_x.measure([0, 1], [0, 1])
    print("Qiskit bell state construction:")
    print(qis_x)

    x = Register(name='phi_plus')
    print("Our bell state construction:")
    print(x.name, ': ', x.__repr__(), '\n', '\n')

    print('###############################################################################################')
    print('############ Test of Noiseless Implementation of Quantum Factoring Against Control ############')
    print('###############################################################################################', '\n')

    print('Qiskit implementation (N=21)')
    run_shor()


if __name__ == "__main__":
    main()
