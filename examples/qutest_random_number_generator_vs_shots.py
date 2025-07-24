import numpy as np
import qiskit
from qiskit.quantum_info import DensityMatrix, Choi
from qiskit_aer import AerSimulator
from qut import QUTest
from make_plots import make_plot2
from qiskit_ibm_runtime.fake_provider import FakeSydneyV2
from qiskit_aer.noise import NoiseModel


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


class MyTests(QUTest):
    """Class prepares environment for a quantum unit test
    based on the testing experiment performing projective measurements in the computational basis and
    Pearson's chi-squared test on the count frequencies.
    """

    def setUp(self):
        self.input = qiskit.QuantumCircuit(1)

    def test_1(self):
        output = subprogram1(self.input)
        self.assertEqual(output, np.array([0.5, 0.5]))
        output = subprogram2(self.input)
        self.assertEqual(output, np.array([0.5, 0.5]))

    def test_2(self):
        output = subprogram1(self.input)
        self.assertEqual(output, DensityMatrix(np.array([[0.5, 0.5j],
                                                         [-0.5j, 0.5]])))
        output = subprogram2(self.input)
        self.assertEqual(output, DensityMatrix(np.array([[0.5, 0.5j],
                                                         [-0.5j, 0.5]])))

    def test_3(self):
        output = subprogram1(self.input)
        self.assertEqual(output, Choi(output))
        output1 = subprogram2(self.input)
        self.assertEqual(output1, Choi(output))
    #
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

    fidelity_noiseless = []
    fidelity_noisy = []
    time_noiseless = []
    time_noisy = []

    for shots in num_shots:

        print("---------------------------------")
        print("Test on the backend without noise")
        print("---------------------------------")

        tests = MyTests(backend=AerSimulator(), shots=shots)
        tests.run(save_data=True)
        fidelity_noiseless.append([item.workflow_data['fid'] for item in tests.tests])
        time_noiseless.append([item.workflow_data['time'] for item in tests.tests])

        print("---------------------------------")
        print("Test on the backend without noise")
        print("---------------------------------")

        backend = FakeSydneyV2()
        noise_model = NoiseModel.from_backend(backend)
        backend = AerSimulator(noise_model=noise_model)

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

    main()
    make_plot2()