import numpy as np
import qiskit
from qiskit_aer import AerSimulator
from qutest import QUTest


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


# class MyTest(qutest.QUT_PROJ):
#     """Class prepares environment for a quantum unit test
#     based on the testing experiment performing projective measurements in the computational basis and
#     Pearson's chi-squared test on the count frequencies.
#     """
#
#     def setUp(self):
#         """Prepare state for the input quantum register"""
#         return qiskit.QuantumCircuit(1)
#
#     def expected(self):
#         """Prepare expected output"""
#         return np.array([0.5, 0.5])


class MyTests(QUTest):
    """Class prepares environment for a quantum unit test
    based on the testing experiment performing projective measurements in the computational basis and
    Pearson's chi-squared test on the count frequencies.
    """

    def test_1(self):
        """Prepare expected output"""
        input = qiskit.QuantumCircuit(1)
        output = subprogram1(input)
        self.assertEqual(output, np.array([0.5, 0.5]))

    def test_2(self):
        """Prepare expected output"""
        input = qiskit.QuantumCircuit(1)
        output = subprogram2(input)
        self.assertEqual(output, np.array([0.5, 0.5]))

    def test_3(self):
        """Prepare expected output"""
        input = qiskit.QuantumCircuit(1)
        output = subprogram1(input)
        self.assertEqual(output,
                         qiskit.quantum_info.DensityMatrix(np.array([[0.5, 0.5j], [-0.5j, 0.5]])))

    def test_4(self):
        """Prepare expected output"""
        qc = qiskit.QuantumCircuit(1)
        qc = subprogram1(qc)
        expected = qiskit.quantum_info.Choi(qc)
        self.assertEqual(qc, expected)

# run tests
tests = MyTests(backend=AerSimulator(), shots=3000)
tests.run()

# run test
# test = MyTest(backend=AerSimulator(), shots=2000)
# test.run(quantum_subprogram1)
# test.run(quantum_subprogram2)
# test.shots = 10
# test.run(quantum_subprogram1)