import numpy as np
import qiskit
import qutest
from qiskit_aer import AerSimulator


def quantum_subprogram(circuit):
    """Tested quantum subroutine -
       random number generator with uniform distribution"""

    circuit.rx(np.pi / 2, 0)
    return circuit


class MyTests(qutest.QUTest):

    def test_1(self):
        quantum_input = qiskit.QuantumCircuit(1)
        quantum_input = quantum_subprogram(quantum_input)
        self.assertEqual(quantum_input, np.array([0.5, 0.5]))


# run tests
MyTests(backend=AerSimulator(), shots=2000).run()
