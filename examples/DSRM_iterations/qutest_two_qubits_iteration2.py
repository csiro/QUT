from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix, Choi
from qiskit_aer import AerSimulator
from qut import QUT_PROJ, QUT_ST, QUT_PT, detach


@detach
def subroutine_correct(circuit):
    circuit.x(0)  # apply Hadamard gate to the first qubit
    circuit.h(0)  # apply phase shift gate to the first qubit
    circuit.cx(0, 1)
    return circuit


@detach
def subroutine_error(circuit):
    circuit.x(0)  # apply Hadamard gate to the first qubit
    circuit.h(1)  # apply phase shift gate to the first qubit
    circuit.cx(0, 1)
    return circuit


class MyTestsProj(QUT_PROJ):
    """Class prepares environment for a quantum unit test."""

    def setUp(self):

        return QuantumCircuit(2)

    def expected(self):
        """Prepare expected output"""
        return [0.5, 0.0, 0.0, 0.5]


class MyTestsST(QUT_ST):
    """Class prepares environment for a quantum unit test."""

    def setUp(self):
        return QuantumCircuit(2)

    def expected(self):
        """Prepare expected output"""
        return DensityMatrix([[0.5, 0.0, 0.0, -0.5],
                                    [0.0, 0.0, 0.0, 0.0],
                                    [0.0, 0.0, 0.0, 0.0],
                                    [-0.5, 0.0, 0.0, 0.5]])


class MyTestsPT(QUT_PT):
    """Class prepares environment for a quantum unit test."""

    def setUp(self):
        return QuantumCircuit(2)

    def expected(self):
        """Prepare expected output"""
        return Choi(subroutine_correct(self.setUp()))


# run tests
test_proj = MyTestsProj(backend=AerSimulator(), shots=3000)
test_st = MyTestsST(backend=AerSimulator(), shots=3000)
test_pt = MyTestsPT(backend=AerSimulator(), shots=3000)

test_proj.run(subroutine_correct)
test_st.run(subroutine_correct)
test_pt.run(subroutine_correct)

test_proj.run(subroutine_error)
test_st.run(subroutine_error)
test_pt.run(subroutine_error)




