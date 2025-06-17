import numpy as np
import qiskit
from qiskit_aer import AerSimulator
import qutest

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


class MyTest(qutest.QUT_PROJ):
    """Class prepares environment for a quantum unit test
    based on the testing experiment performing projective measurements in the computational basis and
    Pearson's chi-squared test on the count frequencies.
    """

    def setUp(self):
        """Prepare state for the input quantum register"""
        return qiskit.QuantumCircuit(1)

    def expected(self):
        """Prepare expected output"""
        return np.array([0.5, 0.5])


# run test
test = MyTest(backend=AerSimulator(), shots=2000)
test.run(subprogram1)
test.run(subprogram2)
test.shots = 10
test.run(subprogram1)