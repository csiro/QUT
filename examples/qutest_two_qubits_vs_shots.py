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


def subprogram2(circuit):
    # mutated qubit index

    cq = circuit.copy()

    nq = 2

    cq.x(0)  # apply Hadamard gate to the first qubit
    cq.h(1)  # apply phase shift gate to the first qubit

    for i in range(1, nq):  # introduce entanglement via controlled-X gates
        cq.cx(0, i)

    return cq



class MyTests(QUTest):
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
        output = subprogram2(self.input)
        self.assertEqual(output, np.array([0.5, 0.0, 0.0, 0.5]))

    def test_2(self):
        output = subprogram1(self.input)
        self.assertEqual(output, self.gt_state)
        output = subprogram2(self.input)
        self.assertEqual(output, self.gt_state)

    def test_3(self):
        output = subprogram1(self.input)
        self.assertEqual(output, self.gt_proc)
        output = subprogram2(self.input)
        self.assertEqual(output, self.gt_proc)

    # def test_4(self):
    #     output = subprogram2(self.input)
    #     self.assertEqual(output, np.array([0.5, 0.5]))


# run tests
# tests = MyTests(backend=AerSimulator(), shots=3000)
# tests.run()


def main():

    num_shots = np.arange(10) + 1
    num_shots1 = np.arange(20, 100, 10)
    num_shots2 = np.arange(200, 1000, 100)
    num_shots3 = np.array([1e3, 1e4, 1e5])
    num_shots = np.concatenate((num_shots, num_shots1, num_shots2, num_shots3))
    num_shots.sort()
    # num_shots = num_shots3

    fidelity_noiseless = []
    fidelity_noisy = []
    time_noiseless = []
    time_noisy = []

    for shots in num_shots:

        print("---------------------------------")
        print("Test on the backend without noise")
        print("---------------------------------")

        backend_options = {'max_parallel_threads': 1,
                           'max_parallel_experiments': 1,
                           'max_parallel_shots': 1}

        tests = MyTests(backend=AerSimulator(**backend_options), shots=shots)
        tests.run(save_data=True)
        fidelity_noiseless.append([item.workflow_data['fid'] for item in tests.tests])
        time_noiseless.append([item.workflow_data['time'] for item in tests.tests])

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

        tests = MyTests(backend=backend, shots=shots)
        tests.run(save_data=True)
        fidelity_noisy.append([item.workflow_data['fid'] for item in tests.tests])
        time_noisy.append([item.workflow_data['time'] for item in tests.tests])

    np.save('fidelity_noiseless_rng.npy', np.array(fidelity_noiseless))
    np.save('fidelity_noisy_rng.npy', np.array(fidelity_noisy))
    np.save('time_noiseless_rng.npy', np.array(time_noiseless))
    np.save('time_noisy_rng.npy', np.array(time_noisy))
    np.save('shots_rng.npy', num_shots)


if __name__ == '__main__':

    # main()
    make_plot2()