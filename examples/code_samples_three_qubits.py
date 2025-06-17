import matplotlib.pyplot as plt
import qiskit
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakePerth
from qiskit.qasm3 import dumps
from qiskit.quantum_info import DensityMatrix

def quantum_subprogram(circuit):
    # quantum unit

    cq = circuit.copy()

    nq = 3

    cq.x(0)  # apply Hadamard gate to the first qubit
    cq.h(0)  # apply phase shift gate to the first qubit

    for i in range(1, nq):  # introduce entanglement via controlled-X gates
        cq.cx(0, i)

    return cq


def quantum_subprogram_mut1(circuit):
    # quantum unit

    cq = circuit.copy()

    nq = 3

    cq.x(0)  # apply Hadamard gate to the first qubit
    cq.h(1)  # apply phase shift gate to the first qubit

    for i in range(1, nq):  # introduce entanglement via controlled-X gates
        cq.cx(0, i)

    return cq


def quantum_subprogram_mut2(circuit):
    # quantum unit

    cq = circuit.copy()

    nq = 3

    cq.s(0)  # apply Hadamard gate to the first qubit
    cq.h(0)  # apply phase shift gate to the first qubit

    for i in range(1, nq):  # introduce entanglement via controlled-X gates
        cq.cx(0, i)

    return cq


def quantum_subprogram_mut3(circuit):
    # quantum unit

    cq = circuit.copy()

    nq = 3

    cq.x(0)  # apply Hadamard gate to the first qubit
    cq.h(0)  # apply phase shift gate to the first qubit

    cq.cx(1, 2)

    for i in range(1, nq):  # introduce entanglement via controlled-X gates
        cq.cx(0, i)

    return cq


def quantum_subprogram_mut4(circuit):
    # quantum unit

    cq = circuit.copy()

    nq = 3

    cq.z(0)
    # cq.z(1)
    cq.s(0)  # apply Hadamard gate to the first qubit
    cq.h(0)  # apply phase shift gate to the first qubit

    cq.cx(0, 1)
    # cq.cx(1, 0)

    return cq


def quantum_subprogram_mut5(circuit):
    # quantum unit

    cq = circuit.copy()

    nq = 3

    cq.x(0)  # apply Hadamard gate to the first qubit
    cq.h(0)  # apply phase shift gate to the first qubit

    # for i in range(1, nq):  # introduce entanglement via controlled-X gates
    #     cq.cx(0, i)

    cq.cx(0, 1)
    cq.cx(1, 2)

    return cq


if __name__ == '__main__':
    # choose backend
    backend = AerSimulator.from_backend(FakePerth())

    nq = 3  # number of qubits
    qc0 = qiskit.QuantumCircuit(nq)  # define the quantum circuit object
    qc = quantum_subprogram(qc0)
    qc1 = quantum_subprogram_mut1(qc0)
    qc2 = quantum_subprogram_mut2(qc0)
    qc3 = quantum_subprogram_mut3(qc0)

    qc = quantum_subprogram_mut5(qc0)

    from qiskit.visualization import plot_state_city

    state = DensityMatrix(qc)
    print(state)
    plot_state_city(state)
    plt.show()

    # qc.draw('mpl')
    # plt.show()
    #
    # qc1.draw('mpl')
    # plt.show()
    #
    # qc2.draw('mpl')
    # plt.show()
    #
    # qc3.draw('mpl')
    # plt.show()

    # qc_meas = qc.measure_all(inplace=False)
    # qc_meas.draw('mpl')
    # plt.show()
    #
    # circ = qiskit.transpile(qc_meas, backend)
    # results = backend.run(circ, shots=2000).result()
    # counts = results.get_counts(qc_meas)
    # print(counts)
    #
    # plot_histogram(counts)
    # plt.show()
