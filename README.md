# QUT (Quantum Unit Testing)

The `qut` framework facilitates writing small and readable unit tests for quantum software. 
The `qut`  framework does not require additional quantum resources beyond those already needed by the application and utilizes quantum tomography or statistical tests on the data obtained from measurements.


## Get started

### Install from source

```bash
git https://github.com/csiro-internal/QUT
cd QUT
pip install -r requirements.txt
pip install .
```

### Create your first test

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix, Choi
from qiskit_aer import AerSimulator
from qut import QUTest, detach


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


class MyTests(QUTest):
    """Class prepares environment for a quantum unit test."""

    def setUp(self):
        self.qinput = QuantumCircuit(2)
        self.distr = [0.5, 0.0, 0.0, 0.5]
        self.state = DensityMatrix([[0.5, 0.0, 0.0, -0.5],
                                       [0.0, 0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0, 0.0],
                                       [-0.5, 0.0, 0.0, 0.5]])
        self.proc = Choi(subroutine_correct(self.qinput))

    def test_1(self):
        self.assertEqual(subroutine_correct(self.qinput), self.distr)
        self.assertEqual(subroutine_correct(self.qinput), self.state)
        self.assertEqual(subroutine_correct(self.qinput), self.proc)

    def test_2(self):
        self.assertEqual(subroutine_error(self.qinput), self.distr)
        self.assertEqual(subroutine_error(self.qinput), self.state)
        self.assertEqual(subroutine_error(self.qinput), self.proc)


# run tests
tests = MyTests(backend=AerSimulator(), shots=3000)
tests.run()
```

This code should produce an output similar to the following:

```
[PASSED]: with a 0.981 probability of passing.
[PASSED]: with a 0.995 probability of passing.
[PASSED]: with a 0.986 probability of passing.
[FAILED]: with a 0.000 probability of passing.
[FAILED]: with a 0.256 probability of passing.
[FAILED]: with a 0.000 probability of passing.
```
