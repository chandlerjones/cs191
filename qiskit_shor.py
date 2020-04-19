from qiskit import IBMQ
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms import Shor

"""
Code for shor's algorithm using Qiskit found here:
https://quantumcomputinguk.org/tutorials/shors-algorithm-with-code
"""


def run_shor():
    token = 'e22b17863fe0ab0a707122dd9aeec8b0f99aaed329dd8639ed5d0dab947d0170e7331df51167088e51c4be2266ee0933ce41624392b14a84b9076c0d72325d66'

    IBMQ.enable_account(token)  # Enter your API token here
    provider = IBMQ.get_provider(hub='ibm-q')

    backend = provider.get_backend('ibmq_qasm_simulator')  # Specifies the quantum device

    print('\n Shors Algorithm')
    print('--------------------')
    print('\nExecuting...\n')

    factors = Shor(21)  # Function to run Shor's algorithm where 21 is the integer to be factored

    result_dict = factors.run(QuantumInstance(backend, shots=1, skip_qobj_validation=False))

    print(result_dict)