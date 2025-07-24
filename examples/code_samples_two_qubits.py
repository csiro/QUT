def subprogram(circuit):
    # correct program

    cq = circuit.copy()

    nq = 2

    cq.x(0)  # apply Hadamard gate to the first qubit
    cq.h(0)  # apply phase shift gate to the first qubit

    for i in range(1, nq):  # introduce entanglement via controlled-X gates
        cq.cx(0, i)

    return cq


def subprogram_mut1(circuit):
    # mutated qubit index

    cq = circuit.copy()

    nq = 2

    cq.x(0)  # apply Hadamard gate to the first qubit
    cq.h(1)  # apply phase shift gate to the first qubit

    for i in range(1, nq):  # introduce entanglement via controlled-X gates
        cq.cx(0, i)

    return cq


def subprogram_mut2(circuit):
    # mutated gate specification

    cq = circuit.copy()

    nq = 2

    cq.s(0)  # apply Hadamard gate to the first qubit
    cq.h(0)  # apply phase shift gate to the first qubit

    for i in range(1, nq):  # introduce entanglement via controlled-X gates
        cq.cx(0, i)

    return cq


def subprogram_mut3(circuit):
    # injected extra two-qubit gate

    cq = circuit.copy()

    nq = 2

    cq.cx(0, 1)

    cq.x(0)  # apply Hadamard gate to the first qubit
    cq.h(0)  # apply phase shift gate to the first qubit

    for i in range(1, nq):  # introduce entanglement via controlled-X gates
        cq.cx(0, i)

    return cq


