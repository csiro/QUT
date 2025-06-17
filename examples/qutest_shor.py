import qutest
import warnings
from qiskit.quantum_info import partial_trace
from qiskit_aer import AerSimulator
import numpy as np
from math import gcd, floor, log
import matplotlib.pyplot as plt
from qutest.aux_functions import make_keys
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import DensityMatrix
from code_samples_shor import mod_mult_cirquit, fourier, fourier_ground_truth, fourier_ground_truth1
from noise_models import noise_model, noise_models


warnings.filterwarnings("ignore")


# cirquit = mod_mult_gate_cirquit(circuit, a, k, N, qubit, target)

class MyTests(qutest.QUT_ST):
    """Tests for Subroutine1 based on the quantum state tomography workflow"""

    def setUp(self):

        a = 2
        N = 9

        if gcd(a, N) > 1:
            raise Exception(f"Error: gcd({a},{N}) > 1")

        n = floor(log(N - 1, 2)) + 1
        m = 2 * n

        control = QuantumRegister(m, name="X")
        target = QuantumRegister(n, name="Y")
        output = ClassicalRegister(m, name="Z")
        circuit = QuantumCircuit(control, target, output)
        # Initialize the target register to the state |1>
        circuit.x(m)
        circuit.h(0)
        circuit.x(0)

        # self.params = [a, 0, N, control[0], target]
        self.params = [0, 9]

        return circuit

    def expected(self):
        circ = self.setUp()
        dens = partial_trace(DensityMatrix(circ), [0, 1, 2, 3, 4, 5, 6, 7])
        return dens


class MyTests_f(qutest.QUT_PROJ):
    """Tests for Subroutine1 based on the projective measurements and statistical tests workflow"""

    def setUp(self):

        a = 2
        N = 9

        if gcd(a, N) > 1:
            raise Exception(f"Error: gcd({a},{N}) > 1")

        n = floor(log(N - 1, 2)) + 1
        m = 2 * n

        control = QuantumRegister(m, name="X")
        circuit = QuantumCircuit(control)
        circuit.h(0)
        self.params = [control]

        return circuit

    def expected(self):
        keys = make_keys(8)
        size = len(keys)
        x = np.linspace(0, np.pi, size, endpoint=False)
        values = fourier_ground_truth1(x, self.shots)

        ans = dict(zip(keys, values))
        return list(ans.values())


def plot(num_shots, data1, data2):
    """Two panel plots"""

    styles = ['.-', '.--', '.--', '.--', '.--', '.--']
    colors = ['darkgreen', 'g', 'forestgreen', 'limegreen', 'lime', 'darkgreen']
    # colors = ['g', 'limegreen', 'limegreen', 'limegreen', 'limegreen', 'limegreen']

    styles = ['.-', '.--']
    colors = ['darkgreen', 'darkgreen']

    fig, axs = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(8, 4))

    for j, item in enumerate(data1):
        axs[0].plot(num_shots, item, styles[j], color=colors[j])
    axs[0].plot([np.min(num_shots), np.max(num_shots)], [0.5, 0.5], ':k')
    axs[0].set_xscale('log')
    axs[0].set_ylabel('Probability', fontsize=12)
    axs[0].set_title(r'Subroutine1, fidelity  $F(\rho_{B_n}, \rho_{expected})$')
    axs[0].set_xscale('log')
    axs[0].set_xlabel('Num. shots', fontsize=12)
    axs[0].tick_params(direction="in")

    for j, item in enumerate(data2):
        axs[1].plot(num_shots, item, styles[j], color=colors[j])
    axs[1].plot([np.min(num_shots), np.max(num_shots)], [0.5, 0.5], ':k')
    axs[1].set_xscale('log')
    axs[1].set_xlabel('Num. shots', fontsize=12)
    axs[1].tick_params(direction="in")
    axs[1].set_xscale('log')
    axs[1].set_title(r'Subroutine2, $R^2 metrics$')
    # axs[1].set_yscale('log')

    axs[1].set_ylim([-0.05, 1.05])

    plt.tight_layout()
    plt.show()


def test1(shots):

    test = MyTests(backend=AerSimulator(),
                   shots=shots,
                   measurement_indices=[8, 9, 10, 11]).run(mod_mult_cirquit)

    return test

def test1_with_noise(shots):

    # from rustworkx.visualization import mpl_draw
    # mpl_draw(backend.coupling_map.graph)
    # plt.show()

    test = MyTests(backend=AerSimulator(noise_model=noise_model),
                   shots=shots,
                   measurement_indices=[8, 9, 10, 11]).run(mod_mult_cirquit)

    return test

def test2(shots):

    test = MyTests_f(backend=AerSimulator(),
                     shots=shots,
                     title='Test on the backend with noise').run(fourier)

    return test

def test2_with_noise(shots):

    test = MyTests_f(backend=AerSimulator(noise_model=noise_model),
                     shots=shots,
                     title='Test on the backend with noise').run(fourier)

    return test


def test_suit_subroutine1(num_shots):

    ans_res = []
    ans_times = []

    for noise in noise_models:

        res = []
        times = []

        for shots in num_shots:

            test = MyTests(backend=AerSimulator(noise_model=noise_models[noise]),
                           shots=shots,
                           measurement_indices=[8, 9, 10, 11],
                           title='Noise model is ' + noise).run(mod_mult_cirquit)

            res.append(test.output_data['fid'])
            times.append(test.output_data['time'] / shots)

        ans_res.append(res)
        ans_times.append(times)

    return num_shots, ans_res, ans_times


def test_suit_subroutine2(num_shots):

    ans_res = []
    ans_times = []

    for noise in noise_models:

        res = []
        times = []

        for shots in num_shots:

            test = MyTests_f(backend=AerSimulator(noise_model=noise_models[noise]),
                             shots=shots,
                             title='Test on the backend with noise').run(fourier)

            res.append(test.output_data['fid'])
            times.append(test.output_data['time'] / shots)

        ans_res.append(res)
        ans_times.append(times)

    return num_shots, ans_res, ans_times


def test_suit(test_ref, test_ref_noise):

    num_shots = np.arange(10) + 1
    num_shots1 = np.arange(20, 100, 10)
    num_shots2 = np.arange(200, 1000, 100)
    num_shots3 = np.array([1e3, 1e4, 1e5])
    num_shots = np.concatenate((num_shots, num_shots1, num_shots2, num_shots3))

    num_shots = np.array([1e3, 1e4, 1e5])
    num_shots.sort()

    res = []
    res_noise = []
    times = []
    times_noise = []

    for shots in num_shots:

        print(shots)

        print("---------------------------------")
        print("Test on the backend without noise")
        print("---------------------------------")

        test = test_ref(shots)
        res.append(test.output_data['fid'])
        times.append(test.output_data['time'] / shots)

        print("---------------------------------")
        print("Test on the backend with noise")
        print("---------------------------------")

        test = test_ref_noise(shots)
        res_noise.append(test.output_data['fid'])
        times_noise.append(test.output_data['time'] / shots)

    return num_shots, res, res_noise, times, times_noise

def main():

    # testing controlled unitary using the workflow
    # based on the quantum state tomography

    num_shots, data, times = test_suit(test1, test1_with_noise)
    np.save('data_sub1.npy', data)

    # testing IQFT using the workflow based on
    # R^2 statistical tests

    # num_shots, data3, data4, times, times_noise = test_suit(test2, test2_with_noise)
    # print(times)
    # plt.plot(times)
    # plt.plot(times_noise)
    # plt.show()
    plot(num_shots, data, data)


def main1():

    num_shots = np.arange(10) + 1
    num_shots1 = np.arange(20, 100, 10)
    num_shots2 = np.arange(200, 1000, 100)
    num_shots3 = np.array([1e3, 1e4, 1e5])
    num_shots = np.concatenate((num_shots, num_shots1, num_shots2, num_shots3))

    # num_shots = np.array([1e3, 1e4, 1e5])
    num_shots.sort()

    # testing controlled unitary using the workflow
    # based on the quantum state tomography

    num_shots, data1, times1 = test_suit_subroutine1(num_shots)
    np.save('data_sub1.npy', data1)
    num_shots, data2, times2 = test_suit_subroutine2(num_shots)
    np.save('data_sub2.npy', data2)
    np.save('num_shots.npy', num_shots)


    # testing IQFT using the workflow based on
    # R^2 statistical tests

    # num_shots, data3, data4, times, times_noise = test_suit(test2, test2_with_noise)
    # print(times)
    # plt.plot(times)
    # plt.plot(times_noise)
    # plt.show()

    # data1 = np.load('data_sub1.npy')
    plot(num_shots, data2, data2)


if __name__ == '__main__':

    main1()







