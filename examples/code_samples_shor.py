import random
from math import gcd, floor, log
from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt
from qiskit.circuit.library import UnitaryGate
from qiskit.circuit.library import QFT
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from noise_models import noise_model


def fourier_ground_truth(x, shots):
    """"""
    values = np.cos(x) ** 2
    values = normalize(shots, values)

    return values


def fourier_ground_truth1(x, shots):
    """"""
    values = np.cos(x) ** 2
    values = normalize1(shots, values)

    return values


def fourier(circuit):
    """
    Subroutine 2

    :param circuit: input quantum register
    :return:        qiskit circuit for Subroutine 1
    """
    control = circuit.qubits[0]._register

    circuit.compose(
        QFT(len(control), inverse=True),
        qubits=control,
        inplace=True)

    # control1 = QuantumRegister(8, name="X")
    # circuit1 = QuantumCircuit(control1)
    # circuit1.compose(
    #     QFT(8, inverse=True),
    #     qubits=control1,
    #     inplace=True)
    #
    # circuit1 = circuit1.decompose()
    # circuit1.draw(output="mpl")
    # plt.show()

    return circuit


def prepare_init_state(a, N):
    if gcd(a, N) > 1:
        print(f"Error: gcd({a},{N}) > 1")
    else:
        n = floor(log(N - 1, 2)) + 1
        m = 2 * n

        control = QuantumRegister(m, name="X")
        target = QuantumRegister(n, name="Y")
        output = ClassicalRegister(m, name="Z")
        circuit = QuantumCircuit(control, target, output)

        # Initialize the target register to the state |1>
        circuit.x(m)

        return circuit


def mod_mult_cirquit(circ, theta, N, a=2):
    """
    Subroutine 1

    :param circ:  input quantum register
    :param theta: input classical argument, orders of the unitary matrix, k=0..7
    :param N:     input parameter, number to factorize
    :param a:     a random integer 2 <= a < N such that gcd(a,N) > 1
    :return:      qiskit circuit for Subroutine 1
    """

    qubit = circ.qubits[theta]
    target = circ.qubits[-1]._register
    circ.h(theta)
    b = pow(a, 2 ** theta, N)

    if gcd(b, N) > 1:
        print(f"Error: gcd({b},{N}) > 1")
    else:
        n = floor(log(N - 1, 2)) + 1
        U = np.full((2 ** n, 2 ** n), 0)
        for x in range(N): U[b * x % N][x] = 1
        for x in range(N, 2 ** n): U[x][x] = 1
        G = UnitaryGate(U)
        G.name = f"M_{b}"

    circ.compose(
        G.control(),
        qubits=[qubit] + list(target),
        inplace=True)

    # bb = G.params[0]
    # plt.imshow(np.abs(bb))
    # plt.show()

    # print(matrix2latex(np.real(bb).astype(int)))

    # from qiskit.transpiler import generate_preset_pass_manager
    # pm = generate_preset_pass_manager(optimization_level=3, basis_gates=['x', 'h', 'rx', 'ry', 'rz', 'cx'])
    # transpiled_circ = pm.run(circ)
    # transpiled_circ.draw()
    # plt.show()

    return circ


def normalize(num_shots, values):
    norm = num_shots / np.sum(values)
    values *= norm
    values = np.round(values).astype(int)
    diff = num_shots - np.sum(values)

    keys = np.arange(len(values))

    for _ in range(int(abs(diff))):
        k = random.choice(keys)
        if diff < 0:
            while values[k] == 0:
                k = random.choice(keys)
        values[k] += 1 * np.sign(diff)

    return values


def normalize1(num_shots, values):
    values *= 1.0 / np.sum(values)

    return values

def order_finding_circuit(a, N):
    if gcd(a, N) > 1:
        print(f"Error: gcd({a},{N}) > 1")
    else:
        n = floor(log(N - 1, 2)) + 1
        m = 2 * n

        control = QuantumRegister(m, name="X")
        target = QuantumRegister(n, name="Y")
        output = ClassicalRegister(m, name="Z")
        circuit = QuantumCircuit(control, target, output)

        # Initialize the target register to the state |1>
        circuit.x(m)

        # Add the Hadamard gates and controlled versions of the
        # multiplication gates
        for k, qubit in enumerate(control):
            cirquit = mod_mult_cirquit(circuit, k, N, a=a)

        # Apply the inverse QFT to the control register
        circuit = fourier(circuit)

        # Measure the control register
        circuit.measure(control, output)

        return circuit


def find_order(a, N):
    if gcd(a, N) > 1:
        print(f"Error: gcd({a},{N}) > 1")
    else:
        n = floor(log(N - 1, 2)) + 1
        m = 2 * n
        circuit = order_finding_circuit(a, N)
        transpiled_circuit = transpile(circuit, AerSimulator(noise_model=noise_model))
        # transpiled_circuit = transpile(circuit, AerSimulator())

        while True:
            result = AerSimulator().run(
                transpiled_circuit,
                shots=1,
                memory=True).result()
            y = int(result.get_memory()[0], 2)
            print(result.get_memory()[0])
            print(y)
            r = Fraction(y / 2 ** m).limit_denominator(N).denominator
            if pow(a, r, N) == 1: break

        return r


def main():
    # order_finding_circuit(2, 9).draw(output="mpl")
    # plt.show()

    N = 39

    FACTOR_FOUND = False

    # First we'll check to see if N is even or a nontrivial power.
    # Order finding won't help for factoring a *prime* power, but
    # we can easily find a nontrivial factor of *any* nontrivial
    # power, whether prime or not.

    if N % 2 == 0:
        print("Even number")
        d = 2
        FACTOR_FOUND = True
    else:
        for k in range(2, round(log(N, 2)) + 1):
            d = int(round(N ** (1 / k)))
            if d ** k == N:
                FACTOR_FOUND = True
                print("Number is a power")
                break

    # Now we'll iterate until a nontrivial factor of N is found.

    while not FACTOR_FOUND:
        a = random.randint(2, N - 1)
        d = gcd(a, N)
        if d > 1:
            FACTOR_FOUND = True
            print(f"Lucky guess of {a} modulo {N}")
        else:
            r = find_order(a, N)
            print(f"The order of {a} modulo {N} is {r}")
            if r % 2 == 0:
                x = pow(a, r // 2, N) - 1
                d = gcd(x, N)
                if d > 1: FACTOR_FOUND = True

    print(f"Factor found: {d}")


if __name__ == '__main__':
    main()
