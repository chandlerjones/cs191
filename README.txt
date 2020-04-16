# cs191
Quantum Circuit Simulation with Realistic Noise

# TODO: 1) Algorithm Implementation(s) (probably Shor's? maybe a second?) -Harrison
        2) Noise injection (See lecture 14 notes for possibilities) -Wyatt, Bradley, Jack for three different types
        3) Error suppression methods (See lecture 16 notes) -Everyone, time permitting
        4) Comparison with Cirq -Chandler

### Documentation ###

Utilities
-Pauli Matrices: X, Y, Z
-Hadamard Matrix: H
-binaryToDecimal(x): takes a binary string (x) and converts it to an integer
-dec_to_bin(x): takes an integer (x) and converts it to a binary string

Qubit Class
-initialization: 
      inputs: name=None (currently only 'plus', 'minus', '+', '-')
              vec=(1, 0) (input the amplitudes directly)       
      outputs: Qubit object      
-__mul__: defaults to np.matmul
-measure: returns one of the basis vectors with probability = square of amplitudes

Register Class
-initialization:
      inputs: n=None (initializes a length-n |000...0> register)
              name=None (currently just the bell states)
              qubits=None (a list of tuples corresponding to the constituent QUBITS in the register. Returns the 
                           tensor product of all of the qubits in the order they are input)
              amplitudes=None (a numpy ndarray or a python list of length 2^n with norm 1 that is converted to a
                               REGISTER object)
              bra=False (conjugate transpose of the input)
      output: Register object
-self.__mul__(other): inner product for bra/ket multiplication, outer product for ket/bra multipication
-self.as_vec(): displays the numpy array (vector) representation of the register
-self.bra(): conjugate transpose
-self.CNOT(control=0, target=1): inputs are indices of control/target qubits in set 0,...,N.  returns the output of the CNOT operation
-self.walsh(): performs a Walsh-Hadamard transformation on the qubit
-self.QFT(): performs a quantum fourier transform on the qubit

Examples:

########## WALSH-HADAMARD AND STATE MULTIPLICATION ##########
>>> x = Register(n=2)                         # Create two registers, both initialized to the state |00>
>>> y = Register(n=2)
>>> x
(1)|00>
>>> x = x.walsh()                             # Create an equal superposition over all basis states
>>> x
(0.5)|00> + (0.5)|01> + (0.5)|10> + (0.5)|11>
>>> x.bra()                                   # Take the conjugate transpose of x.
(0.5)<00| + (0.5)<01| + (0.5)<10| + (0.5)<11|
>>> y * x                                     # Equivalent to |y><x|
array([[0.5, 0.5, 0.5, 0.5],
       [0. , 0. , 0. , 0. ],
       [0. , 0. , 0. , 0. ],
       [0. , 0. , 0. , 0. ]])
>>> x * y                                     # Equivalent to <x|y>
0

########## CNOT ##########
>>> amps = [0.5, 0.5, 0, 0, 0, 0, 0.5, 0.5]
>>> x = Register(amplitudes=amps)             # Create a register by passing through a python list of values
>>> x
(0.5)|000> + (0.5)|001> + (0.5)|110> + (0.5)|111>
>>> x.CNOT()                                  # Control = 0 and Target = 1 by default 
(0.5)|000> + (0.5)|001> + (0.5)|100> + (0.5)|101>
>>> x.CNOT()                                  # Performing the operation again restores the original state
(0.5)|000> + (0.5)|001> + (0.5)|110> + (0.5)|111>
>>> x.CNOT(control=2, target=1)               # Third qubit is the control, second is the target.
(0.5)|000> + (0.5)|011> + (0.5)|101> + (0.5)|110>

########## QUANTUM FOURIER TRANSFORM ##########
>>> x = Register.ones(2)                      # Create a 2-qubit register via the ones() method
>>> x
(1)|11>
>>> x.QFT()                                   # Perform QFT, where j is the imaginary unit sqrt(-1) in numpy
((0.5+0j))|00> + ((0-0.5j))|01> + ((-0.5+0j))|10> + ((0+0.5j))|11>






         
        
