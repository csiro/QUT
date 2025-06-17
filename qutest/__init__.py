"""
This module contains core classes for the quantum unit testing framework QUTest.
The classes implement a library of testing protocols for quantum subroutines for various assertion arguments.

Example of usage:
    import numpy as np
    import qiskit
    import qutest
    from qiskit_aer import AerSimulator


    def quantum_subprogram(circuit):

        circuit.rx(np.pi / 2, 0)
        return circuit


    class MyTests(qutest.QUT_PROJ):
        #unit test based on the workflow QUT_PROJ

        def setUp(self):
            #Prepare state for the input quantum register
            circuit = qiskit.QuantumCircuit(1)
            return circuit

        def expected(self):
            #Prepare expected output
            return np.array([0.5, 0.5])


    # run tests
    MyTests(backend=AerSimulator(), shots=2000).run(quantum_subprogram1)

Author:
    Mykhailo Klymenko, CSIRO's Data61 (mike.klymenko@data61.csiro.au)
Version:
    0.0.1
"""

__all__ = ['QUT_ST', 'QUT_PT', 'QUT_PROJ', 'QUTest']

from .qutest_core import QUT_ST, QUT_PT, QUT_PROJ, QUTest
from .aux_functions import make_keys, parse_code, likelihood