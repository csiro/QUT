import numpy as np
import qiskit
from qiskit.quantum_info import DensityMatrix, Choi
from qiskit_aer import AerSimulator
from qut import QUTest
from make_plots import make_plot2
from qiskit_ibm_runtime.fake_provider import FakeSydneyV2
from qiskit_aer.noise import NoiseModel


def subprogram1(circuit):
    # correct program

    cq = circuit.copy()

    nq = 2

    cq.x(0)  # apply Hadamard gate to the first qubit
    cq.h(0)  # apply phase shift gate to the first qubit

    for i in range(1, nq):  # introduce entanglement via controlled-X gates
        cq.cx(0, i)

    return cq


def mutant(circuit, code):
    # mutated qubit index
    # code is in teh range [0, 512)
    # the correct program code is 324


    cq = circuit.copy()
    ind = list(map(int, list(map(int, format(code, '011b')[2:]))))

    if ind[0] == 1: cq.x(0)
    # if ind[1] == 1: cq.y(0)
    if ind[1] == 1: cq.z(0)
    if ind[2] == 1: cq.h(0)
    if ind[3] == 1: cq.x(1)
    # if ind[5] == 1: cq.y(1)
    if ind[4] == 1: cq.z(1)
    if ind[5] == 1: cq.h(1)
    if ind[6] == 1: cq.cx(0, 1)
    if ind[7] == 1: cq.cx(1, 0)
    if ind[8] == 1: cq.cx(0, 1)

    return cq


class MyTests1(QUTest):
    """Class prepares environment for a quantum unit test
    based on the testing experiment performing projective measurements in the computational basis and
    Pearson's chi-squared test on the count frequencies.
    """

    def setUp(self):
        self.input = qiskit.QuantumCircuit(2)
        self.gt_proc = Choi(subprogram1(self.input))
        expected = np.zeros((4, 4))
        expected[0, 0] = 0.5
        expected[3, 3] = 0.5
        expected[0, 3] = -0.5
        expected[3, 0] = -0.5
        self.gt_state = DensityMatrix(expected)

    def test_1(self):
        output = subprogram1(self.input)
        self.assertEqual(output, np.array([0.5, 0.0, 0.0, 0.5]))
        for j in range(512):
            print("test1", j, bin(j))
            output = mutant(self.input, j)
            self.assertEqual(output, np.array([0.5, 0.0, 0.0, 0.5]))


class MyTests2(QUTest):
    """Class prepares environment for a quantum unit test
    based on the testing experiment performing projective measurements in the computational basis and
    Pearson's chi-squared test on the count frequencies.
    """

    def setUp(self):
        self.input = qiskit.QuantumCircuit(2)
        self.gt_proc = Choi(subprogram1(self.input))
        expected = np.zeros((4, 4))
        expected[0, 0] = 0.5
        expected[3, 3] = 0.5
        expected[0, 3] = -0.5
        expected[3, 0] = -0.5
        self.gt_state = DensityMatrix(expected)

    def test_2(self):
        output = subprogram1(self.input)
        self.assertEqual(output, self.gt_state)
        for j in range(512):
            print("test2", j, bin(j))
            output = mutant(self.input, j)
            self.assertEqual(output, self.gt_state)


class MyTests3(QUTest):
    """Class prepares environment for a quantum unit test
    based on the testing experiment performing projective measurements in the computational basis and
    Pearson's chi-squared test on the count frequencies.
    """

    def setUp(self):
        self.input = qiskit.QuantumCircuit(2)
        self.gt_proc = Choi(subprogram1(self.input))
        expected = np.zeros((4, 4))
        expected[0, 0] = 0.5
        expected[3, 3] = 0.5
        expected[0, 3] = -0.5
        expected[3, 0] = -0.5
        self.gt_state = DensityMatrix(expected)

    def test_3(self):
        output = subprogram1(self.input)
        self.assertEqual(output, self.gt_proc)
        for j in range(512):
        # for j in range(10):
            print("test3", j, bin(j))
            output = mutant(self.input, j)
            self.assertEqual(output, self.gt_proc)


def main():

    shots = 1e3

    print("---------------------------------")
    print("Test on the backend without noise")
    print("---------------------------------")

    backend_options = {'max_parallel_threads': 1,
                       'max_parallel_experiments': 1,
                       'max_parallel_shots': 1}

    tests1 = MyTests1(backend=AerSimulator(**backend_options), shots=shots)
    tests1.run(save_data=True)
    results_noiseless1 = np.array([item.workflow_data['fid'] for item in tests1.tests])
    np.save('results_noiseless1.npy', results_noiseless1)

    tests2 = MyTests2(backend=AerSimulator(**backend_options), shots=shots)
    tests2.run(save_data=True)
    results_noiseless2 = np.array([item.workflow_data['fid'] for item in tests2.tests])
    np.save('results_noiseless2.npy', results_noiseless2)

    tests3 = MyTests3(backend=AerSimulator(**backend_options), shots=shots)
    tests3.run(save_data=True)
    results_noiseless3 = np.array([item.workflow_data['fid'] for item in tests3.tests])
    np.save('results_noiseless3.npy', results_noiseless3)

    print("---------------------------------")
    print("Test on the backend with noise")
    print("---------------------------------")

    backend = FakeSydneyV2()
    noise_model = NoiseModel.from_backend(backend)

    backend_options = {'max_parallel_threads': 1,
                       'max_parallel_experiments': 1,
                       'max_parallel_shots': 1,
                       'noise_model': noise_model}

    backend = AerSimulator(**backend_options)

    tests1 = MyTests1(backend=backend, shots=shots)
    tests1.run(save_data=True)
    results_noise1 = np.array([item.workflow_data['fid'] for item in tests1.tests])
    np.save('results_noise1.npy', results_noise1)

    tests2 = MyTests2(backend=backend, shots=shots)
    tests2.run(save_data=True)
    results_noise2 = np.array([item.workflow_data['fid'] for item in tests2.tests])
    np.save('results_noise2.npy', results_noise2)

    tests3 = MyTests3(backend=backend, shots=shots)
    tests3.run(save_data=True)
    results_noise3 = np.array([item.workflow_data['fid'] for item in tests3.tests])
    np.save('results_noise3.npy', results_noise3)


if __name__ == '__main__':

    main()

    results_noiseless1 = np.load('results_noiseless1.npy')
    results_noiseless2 = np.load('results_noiseless2.npy')
    results_noiseless3 = np.load('results_noiseless3.npy')
    results_noise1 = np.load('results_noise1.npy')
    results_noise2 = np.load('results_noise2.npy')
    results_noise3 = np.load('results_noise3.npy')

    import matplotlib.pyplot as plt

    num_mutants = len(results_noiseless1) - 3
    thr = 0.25

    print('----------------------------')

    print("FNR", 1.0 - results_noiseless1[0])
    print("FNR", 1.0 - results_noiseless2[0])
    print("FNR", 1.0 - results_noiseless3[0])
    print("FNR", 1.0 - results_noise1[0])
    print("FNR", 1.0 - results_noise2[0])
    print("FNR", 1.0 - results_noise3[0])

    print('----------------------------')

    print("FPR", np.average(results_noiseless1[results_noiseless1 < (1-thr)]))
    print("FPR", np.average(results_noiseless2[results_noiseless2 < (1-thr)]))
    print("FPR", np.average(results_noiseless3[results_noiseless3 < (1-thr)]))
    print("FPR", np.average(results_noise1[results_noise1 < (1-thr)]))
    print("FPR", np.average(results_noise2[results_noise2 < (1-thr)]))
    print("FPR", np.average(results_noise3[results_noise3 < (1-thr)]))

    plt.figure(1)
    plt.plot(results_noiseless1)
    results_noiseless1 = results_noiseless1[0] - results_noiseless1
    results_noiseless1 = results_noiseless1[results_noiseless1 > thr]
    # plt.plot(results_noiseless1)
    plt.plot(results_noise1)
    results_noise1 = results_noise1[0] - results_noise1
    results_noise1 = results_noise1[results_noise1 > thr]
    # plt.plot(results_noise1)

    plt.figure(2)
    plt.plot(results_noiseless2)
    results_noiseless2 = results_noiseless2[0] - results_noiseless2
    results_noiseless2 = results_noiseless2[results_noiseless2 > thr]
    # plt.plot(results_noiseless2)
    plt.plot(results_noise2)
    results_noise2 = results_noise2[0] - results_noise2
    results_noise2 = results_noise2[results_noise2 > thr]
    # plt.plot(results_noise2)

    plt.figure(3)
    plt.plot(results_noiseless3)
    results_noiseless3 = results_noiseless3[0] - results_noiseless3
    results_noiseless3 = results_noiseless3[results_noiseless3 > thr]
    # plt.plot(results_noiseless3)
    plt.plot(results_noise3)
    results_noise3 = results_noise3[0] - results_noise3
    results_noise3 = results_noise3[results_noise3 > thr]
    # plt.plot(results_noise3)
    plt.show()

    print('----------------------------')

    print("Average J", np.average(results_noiseless1))
    print("Average J", np.average(results_noiseless2))
    print("Average J", np.average(results_noiseless3))

    print("Average J", np.average(results_noise1))
    print("Average J", np.average(results_noise2))
    print("Average J", np.average(results_noise3))

    print('----------------------------')

    print("Mutants eliminated, %", len(results_noiseless1) / num_mutants)
    print("Mutants eliminated, %", len(results_noiseless2) / num_mutants)
    print("Mutants eliminated, %", len(results_noiseless3) / num_mutants)

    print("Mutants eliminated, %", len(results_noise1) / num_mutants)
    print("Mutants eliminated, %", len(results_noise2) / num_mutants)
    print("Mutants eliminated, %", len(results_noise3) / num_mutants)

