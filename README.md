# QUTest (Quantum Unit Testing)

The `qutest` framework facilitates writing small and readable unit tests for quantum software. 
The `qutest`  framework does not require additional quantum resources beyond those already needed by the application and utilizes quantum tomography or statistical tests on the data obtained from measurements.


## Get started

### Install from source

```bash
git https://github.com/freude/QUTest.git
cd QUT
pip install -r requirements.txt
pip install .
```

### Create your first test

```python
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


# run test
test = MyTest(backend=AerSimulator(), shots=2000)
test.run(subprogram1)
test.run(subprogram2)
test.shots = 10
test.run(subprogram1)
```

This code should produce an output similar to the following:

```
[PASSED]: with a 0.999 probability of passing.

[FAILED]: with a 0.317 probability of passing.

[FAILED]: with a 0.689 probability of passing.
```
