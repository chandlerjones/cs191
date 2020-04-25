# cs191
Quantum Circuit Simulation with Realistic Noise
        
### Types of Single Qubit Error ###
#### Dephasing ####
Moving from surface of bloch sphere to the Z axis over time due to magnetic field. jump no-jump p probability of applying Z.

#### Bit Flip ####
Flip across Z plane. Probability of flipping from 1 to 0. Probability p of applying X.

#### Depolarization ####
Moving toward origin of sphere. Equal probability p/3 of applying X, Y, or Z.

#### Amplitude Damping ####
Moving toward north pole `|0〉`. Also called Thermal relaxation. Probability of `|1〉 -> |0〉`

### Implementation Proposal ###
Using qiskit as a ref, give each gate configurable noise and global default noise per op. This might require an overarching
Circuit class like qiskit or individual gate classes. Consider configurable dephasing of each inactive qubit over time with
global default, as usual, time permitting.

### Documentation ###

########################### Qubit.py ##############################

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
-pauli(self, op): performs the pauli matrix given in argument OP {'X', 'Y', 'Z'}
-hadamard(self): performs a single-qubit hadamard operation
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
-self.purity: gives the purity of the state (1 for pure state, 0.5 for maximally mixed)
-self.density: returns the density matrix of the state



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
0.5

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






########################### Gate.py ##############################

Gate Class
-description: represents a generic gate with noise. Can be directly instantiated but it's best to inherit from
              this class to program specific gates.
-initialization:
    inputs: n [Required] : number of bits.
            transform=None : a single 2^n x 2^n matrix transformation applied by the gate.
            noise=None : Noise instance specifies the noise. If not provided, will use no noise.
    output: Gate object
-self.__mul__(other): tensor product between two gates. Also automatically combines the noise models.
-self.apply(register): apply the gate to a specified register nondestructively. Returns new register.

Hadamard Class
-description: Creates a hadamard gate on a single qubit with specified noise channel.

Walsh Class
-description: Creates a walsh gate on n qubits with specified noise channel.

-----------------------------------------------------------------------------------------------------------------

Noise Class
-description: represents a noise channel. Can be directly instantiated but it's best to inherit from this class
              to apply specific kinds of noise.
-initialization:
    inputs: n [Required] : number of bits.
            probabilities [Required] : list of probabilities of each noise transform. Do not include I probability!
            transforms [Required] : list of transforms to be applied with probability specified. Do not include I!
-self.__mul__(other): "tensor product of noise." Returns a noise channel that supports n1 + n2 bits.
-self.eval(): evaluates the noise once. Returns a transformation matrix to be applied to a register.

NoNoise Class
-description: Default noise channel used when no channel is specified. See code for usage.

XNoise Class
-description: Bit flip with probability p on each of n bits. See code for usage.

YNoise Class
-description: Apply Pauli Y with probability p on each of n bits. See code for usage.

ZNoise Class
-description: Apply dephasing with probability p on each of n bits. See code for usage.

PauliNoise Class
-description: Apply one of X, Y, Z with probabilities px, py, pz on each of n bits. See code for usage.
         
        
Examples:
See test.py for example usage.
