import numpy as np
import qiskit
from qiskit.quantum_info import DensityMatrix, Choi
from qiskit_aer import AerSimulator
from qut import QUTest


def subprogram1(circuit):
    """Tested quantum subroutine -
       random number generator with uniform distribution"""

    circuit.rx(np.pi / 2, 0)
    return circuit


def subprogram2(circuit):
    """Tested quantum subroutine -
       random number generator with uniform distribution"""

    circuit.rx(np.pi, 0)
    return circuit


class MyTests(QUTest):
    """Class prepares environment for a quantum unit test
    based on the testing experiment performing projective measurements in the computational basis and
    Pearson's chi-squared test on the count frequencies.
    """

    def setUp(self):
        self.input = qiskit.QuantumCircuit(1)

    def test_1(self):
        output = subprogram1(self.input)
        self.assertEqual(output, np.array([0.5, 0.5]))

    def test_2(self):
        output = subprogram1(self.input)
        self.assertEqual(output, DensityMatrix(np.array([[0.5, 0.5j],
                                                         [-0.5j, 0.5]])))

    def test_3(self):
        output = subprogram1(self.input)
        self.assertEqual(output, Choi(output))

    def test_4(self):
        output = subprogram2(self.input)
        self.assertEqual(output, np.array([0.5, 0.5]))


# run tests
tests = MyTests(backend=AerSimulator(), shots=3000)
tests.run()
