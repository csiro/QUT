import unittest
import io
from contextlib import redirect_stdout
from colorama import Fore
import numpy as np
import qiskit
from qiskit_aer import AerSimulator
import qut

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


class MyTest(qut.QUT_PROJ):
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


class Tests(unittest.TestCase):

    def setUp(self) -> None:
        self.test = MyTest(backend=AerSimulator(), shots=2000)

    def test_subprogram1(self):

        expected = Fore.GREEN + "[PASSED]: with a 0.999 probability of passing." + Fore.RESET

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self.test.run(subprogram1)

        output = buffer.getvalue().strip()  # Get the printed string
        self.assertEqual(output, expected)

    def test_subprogram2(self):

        expected = Fore.RED + "[FAILED]: with a 0.317 probability of passing." + Fore.RESET

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self.test.run(subprogram2)

        output = buffer.getvalue().strip()  # Get the printed string
        self.assertEqual(output, expected)

    def test_subprogram1_less_shots(self):

        self.test.shots = 10
        expected = Fore.RED + "[FAILED]: with a 0.689 probability of passing." + Fore.RESET

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self.test.run(subprogram1)

        output = buffer.getvalue().strip()  # Get the printed string
        self.assertEqual(output, expected)


if __name__ == '__main__':

    unittest.main()