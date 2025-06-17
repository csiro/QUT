import numpy as np
import types


def parse_code(data):

    from qiskit.qasm2 import load as load2
    from qiskit.qasm2 import loads as loads2
    from qiskit.qasm3 import load as load3
    from qiskit.qasm3 import loads as loads3
    from qiskit.circuit.quantumcircuit import QuantumCircuit

    def func(my_func):
        if isinstance(my_func, types.FunctionType):
            return my_func
        else:
            raise Exception

    def circ(my_func):
        if isinstance(my_func, QuantumCircuit):
            return my_func
        else:
            raise Exception

    parsers = [loads3, load3, loads2, load2, func, circ]

    for parser in parsers:
        try:
            return parser(data)
        except Exception:
            continue

    print("All parsing attempts failed.")
    return None


def make_keys(nn):
    ans = []
    nn += 1
    def genbin(n, bs = ''):

        if n-1:
            genbin(n-1, bs + '0')
            genbin(n-1, bs + '1')
        else:
            # print('1' + bs)
            ans.append(bs)

    genbin(nn, bs='')

    return ans


def fro_norm(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.linalg.norm(np.abs(a - b), ord='fro')


def likelihood(aa: np.ndarray, bb: np.ndarray) -> float:

    aa_real = np.real(aa).flatten()
    aa_imag = np.imag(aa).flatten()

    bb_real = np.real(bb).flatten()
    bb_imag = np.imag(bb).flatten()

    ans = 1

    for j in range(len(aa_real)):
        if np.abs(aa_real[j]) > 1e-5:
            ans1 = np.exp(-((aa_real[j] - bb_real[j]) ** 2) / np.abs(aa_real[j]) / 2 / 64)
        else:
            ans1 = 1

        if np.abs(aa_imag[j]) > 1e-5:
            ans2 = np.exp(-((aa_imag[j] - bb_imag[j]) ** 2) / np.abs(aa_imag[j]) / 2 / 64)
        else:
            ans2 = 1

        ans *= (ans1 * ans2)

    return ans