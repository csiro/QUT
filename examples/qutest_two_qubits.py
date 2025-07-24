from inspect import getmembers, isfunction
import numpy as np
import code_samples_two_qubits
import warnings
import qiskit
from qut import QUTest
from qut import likelihood
from qiskit_ibm_runtime.fake_provider import FakeSydneyV2
from qiskit_aer.noise import NoiseModel
from make_plots import make_plot1
from qiskit.quantum_info import Choi, DensityMatrix
from qiskit_aer import AerSimulator


warnings.filterwarnings("ignore")

# extract list of code samples from the module code_samples_two_qubits
code_samples = [item[1] for item in getmembers(code_samples_two_qubits, isfunction)]


class MyTests(QUTest):
    """Class prepares environment for a quantum unit test"""

    def setUp(self):
        self.input = qiskit.QuantumCircuit(2)
        self.gt_proc = Choi(code_samples[0](self.input))
        expected = np.zeros((4, 4))
        expected[0, 0] = 0.5
        expected[3, 3] = 0.5
        expected[0, 3] = -0.5
        expected[3, 0] = -0.5
        self.gt_state = DensityMatrix(expected)

    def test_1(self):
        print("\n-----------------------------------")
        print("Tests for a subroutine as a state")
        print("---------------------------------")
        for code_item in code_samples:
            output = code_item(self.input)
            self.assertEqual(output, self.gt_state)

    def test_2(self):
        print("\n-----------------------------------")
        print("Tests for a subroutine as a process")
        print("-----------------------------------")
        for code_item in code_samples:
            output = code_item(self.input)
            self.assertEqual(output, self.gt_proc)

def main():

    num_shots = np.arange(10) + 1
    num_shots1 = np.arange(20, 100, 10)
    num_shots2 = np.arange(200, 1000, 100)
    num_shots3 = np.array([1e3, 1e4, 1e5])
    # num_shots = np.concatenate((num_shots, num_shots1))
    num_shots = np.concatenate((num_shots, num_shots1, num_shots2, num_shots3))
    num_shots.sort()

    fidelity_noiseless = []
    fidelity_noisy = []

    for shots in num_shots:

        print("---------------------------------")
        print("Test on the backend without noise")
        print("---------------------------------")

        tests = MyTests(backend=AerSimulator(), shots=shots)
        tests.run(save_data=True)
        fidelity_noiseless.append([item.workflow_data['fid'] for item in tests.tests])

        print("---------------------------------")
        print("Test on the backend without noise")
        print("---------------------------------")

        backend = FakeSydneyV2()
        noise_model = NoiseModel.from_backend(backend)
        backend = AerSimulator(noise_model=noise_model)

        tests = MyTests(backend=backend, shots=shots)
        tests.run(save_data=True)
        fidelity_noisy.append([item.workflow_data['fid'] for item in tests.tests])

    np.save('fidelity_noiseless.npy', np.array(fidelity_noiseless))
    np.save('fidelity_noisy.npy', np.array(fidelity_noisy))
    np.save('shots.npy', num_shots)


if __name__ == '__main__':

    # main()
    make_plot1()

