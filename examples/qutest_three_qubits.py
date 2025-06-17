import subprocess
import qutest
import numpy as np
from code_samples_three_qubits import *
import warnings
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as colors
from qutest import likelihood
from qiskit_ibm_runtime.fake_provider import FakeSydneyV2
from qiskit_aer.noise import NoiseModel
from make_plots import make_plot


warnings.filterwarnings("ignore")


class MyTests(qutest.QUT_ST):

    def setUp(self):
        nq = 3  # number of qubits
        precondition = qiskit.QuantumCircuit(nq)

        return precondition

    def expected(self):
        expected = np.zeros((8, 8))
        expected[0, 0] = 0.5
        expected[7, 7] = 0.5
        expected[0, 7] = -0.5
        expected[7, 0] = -0.5

        return expected


# class MyTests(qutest.QUT_PT):
#
#     def setUp(self):
#         nq = 3  # number of qubits
#         precondition = qiskit.QuantumCircuit(nq)
#
#         return precondition
#
#     def expected(self):
#         expected = quantum_subprogram(self.setUp())
#
#         # import matplotlib.pyplot as plt
#         # aaa = Choi(expected).output_data
#         # aaa1 =PTM(expected).output_data
#         # plt.imshow(np.real(aaa1))
#         # plt.show()
#
#         return Choi(expected)
#         #
#         # return PTM(expected)


def main():

    print("---------------------------------")
    print("Test on the backend without noise")
    print("---------------------------------")

    num_shots = 20

    test1 = MyTests(backend=AerSimulator(),
                    shots=num_shots)
    test1.run(quantum_subprogram)

    test2 = MyTests(backend=AerSimulator(),
                    shots=num_shots)
    test2.run(quantum_subprogram_mut1)

    test3 = MyTests(backend=AerSimulator(),
                    shots=num_shots)
    test3.run(quantum_subprogram_mut2)

    print("---------------------------------")
    print("Test on the backend with noise")
    print("---------------------------------")

    test1 = MyTests(backend=AerSimulator.from_backend(FakePerth()),
                    shots=num_shots)
    test1.run(quantum_subprogram)

    test2 = MyTests(backend=AerSimulator.from_backend(FakePerth()),
                    shots=num_shots)
    test2.run(quantum_subprogram_mut1)

    test3 = MyTests(backend=AerSimulator.from_backend(FakePerth()),
                    shots=num_shots)
    test3.run(quantum_subprogram_mut2)

def main1():

    # num_shots = np.arange(20, 98) + 1
    num_shots = np.arange(10) + 1
    num_shots1 = np.arange(20, 100, 10)
    num_shots2 = np.arange(200, 1000, 100)
    num_shots3 = np.array([1e3, 1e4, 1e5])
    num_shots = np.concatenate((num_shots, num_shots1, num_shots2, num_shots3))
    num_shots.sort()

    res_1 = []
    res_2 = []
    res_3 = []
    res_4 = []
    res_1_n = []
    res_2_n = []
    res_3_n = []
    res_4_n = []

    rho_1 = []
    rho_2 = []
    rho_3 = []
    rho_4 = []
    rho_1_n = []
    rho_2_n = []
    rho_3_n = []
    rho_4_n = []


    data_1 = []
    data_2 = []
    data_3 = []
    data_4 = []
    data_1_n = []
    data_2_n = []
    data_3_n = []
    data_4_n = []


    for shots in num_shots:

        print(shots)

        print("---------------------------------")
        print("Test on the backend without noise")
        print("---------------------------------")

        backend = AerSimulator()

        test1 = MyTests(backend=backend,
                        shots=shots)
        test1.run(quantum_subprogram)

        test2 = MyTests(backend=backend,
                        shots=shots)
        test2.run(quantum_subprogram_mut1)

        test3 = MyTests(backend=backend,
                        shots=shots)
        test3.run(quantum_subprogram_mut2)

        test4 = MyTests(backend=backend,
                        shots=shots)
        test4.run(quantum_subprogram_mut3)

        res_1.append(test1.output_data['fid'])
        res_2.append(test2.output_data['fid'])
        res_3.append(test3.output_data['fid'])
        res_4.append(test4.output_data['fid'])

        rho_1.append(test1.output_data['rho'])
        rho_2.append(test2.output_data['rho'])
        rho_3.append(test3.output_data['rho'])
        rho_4.append(test4.output_data['rho'])

        data_1.append(test1.output_data)
        data_2.append(test2.output_data)
        data_3.append(test3.output_data)
        data_4.append(test4.output_data)

        print("---------------------------------")
        print("Test on the backend with noise")
        print("---------------------------------")

        backend = FakeSydneyV2()
        noise_model = NoiseModel.from_backend(backend)
        backend = AerSimulator(noise_model=noise_model)

        # backend = AerSimulator.from_backend(FakeSydneyV2())

        test1 = MyTests(backend=backend,
                        shots=shots)
        test1.run(quantum_subprogram)

        test2 = MyTests(backend=backend,
                        shots=shots)
        test2.run(quantum_subprogram_mut1)

        test3 = MyTests(backend=backend,
                        shots=shots)
        test3.run(quantum_subprogram_mut2)

        test4 = MyTests(backend=backend,
                        shots=shots)
        test4.run(quantum_subprogram_mut3)

        res_1_n.append(test1.output_data['fid'])
        res_2_n.append(test2.output_data['fid'])
        res_3_n.append(test3.output_data['fid'])
        res_4_n.append(test4.output_data['fid'])

        rho_1_n.append(test1.output_data['rho'])
        rho_2_n.append(test2.output_data['rho'])
        rho_3_n.append(test3.output_data['rho'])
        rho_4_n.append(test4.output_data['rho'])

        data_1_n.append(test1.output_data)
        data_2_n.append(test2.output_data)
        data_3_n.append(test3.output_data)
        data_4_n.append(test4.output_data)

    l1 = []
    l2 = []
    l3 = []
    l4 = []

    for j in range(len(rho_1)):
        l1.append(likelihood(rho_1[j], rho_1[-1]))
        l2.append(likelihood(rho_2[j], rho_1[-1]))
        l3.append(likelihood(rho_3[j], rho_1[-1]))
        l4.append(likelihood(rho_4[j], rho_1[-1]))

    l1 = np.array(l1)
    l2 = np.array(l2)
    l3 = np.array(l3)
    l4 = np.array(l4)

    t1 = []
    t2 = []
    t3 = []
    t4 = []

    for j in range(len(rho_1)):
        t1.append(likelihood(rho_1[j], rho_1[-1]))
        t2.append(likelihood(rho_2[j], rho_2[-1]))
        t3.append(likelihood(rho_3[j], rho_3[-1]))
        t4.append(likelihood(rho_4[j], rho_4[-1]))

    t1 = np.array(t1)
    t2 = np.array(t2)
    t3 = np.array(t3)
    t4 = np.array(t4)

    l1_n = []
    l2_n = []
    l3_n = []
    l4_n = []

    for j in range(len(rho_1_n)):
        l1_n.append(likelihood(rho_1_n[j], rho_1_n[-1]))
        l2_n.append(likelihood(rho_2_n[j], rho_1_n[-1]))
        l3_n.append(likelihood(rho_3_n[j], rho_1_n[-1]))
        l4_n.append(likelihood(rho_4_n[j], rho_1_n[-1]))

    l1_n = np.array(l1_n)
    l2_n = np.array(l2_n)
    l3_n = np.array(l3_n)
    l4_n = np.array(l4_n)

    t1_n = []
    t2_n = []
    t3_n = []
    t4_n = []

    for j in range(len(rho_1_n)):
        t1_n.append(likelihood(rho_1_n[j], rho_1_n[-1]))
        t2_n.append(likelihood(rho_2_n[j], rho_2_n[-1]))
        t3_n.append(likelihood(rho_3_n[j], rho_3_n[-1]))
        t4_n.append(likelihood(rho_4_n[j], rho_4_n[-1]))

    t1_n = np.array(t1_n)
    t2_n = np.array(t2_n)
    t3_n = np.array(t3_n)
    t4_n = np.array(t4_n)

    plt.plot(l1)
    plt.plot(l2)
    plt.plot(l3)
    plt.plot(l4)
    plt.show()

    plt.plot(res_1)
    plt.plot(res_2)
    plt.plot(res_3)
    plt.plot(res_4)
    plt.plot(res_1_n, '--')
    plt.plot(res_2_n, '--')
    plt.plot(res_3_n, '--')
    plt.plot(res_4_n, '--')
    plt.show()

    np.save('res_1.npy', res_1)
    np.save('res_2.npy', res_2)
    np.save('res_3.npy', res_3)
    np.save('res_4.npy', res_4)
    np.save('res_1_n.npy', res_1_n)
    np.save('res_2_n.npy', res_2_n)
    np.save('res_3_n.npy', res_3_n)
    np.save('res_4_n.npy', res_4_n)


    np.save('data_1.npy', data_1)
    np.save('data_2.npy', data_2)
    np.save('data_3.npy', data_3)
    np.save('data_4.npy', data_4)
    np.save('data_1_n.npy', data_1_n)
    np.save('data_2_n.npy', data_2_n)
    np.save('data_3_n.npy', data_3_n)
    np.save('data_4_n.npy', data_4_n)


    np.save('l1.npy', l1)
    np.save('l2.npy', l2)
    np.save('l3.npy', l3)
    np.save('l4.npy', l4)
    np.save('t1.npy', t1)
    np.save('t2.npy', t2)
    np.save('t3.npy', t3)
    np.save('t4.npy', t4)
    np.save('l1_n.npy', l1_n)
    np.save('l2_n.npy', l2_n)
    np.save('l3_n.npy', l3_n)
    np.save('l4_n.npy', l4_n)
    np.save('t1_n.npy', t1_n)
    np.save('t2_n.npy', t2_n)
    np.save('t3_n.npy', t3_n)
    np.save('t4_n.npy', t4_n)
    np.save('num_shots.npy', num_shots)

    make_plot()


if __name__ == '__main__':

    main1()


