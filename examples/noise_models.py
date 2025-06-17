import numpy as np
from qiskit_ibm_runtime.fake_provider import FakeSydneyV2
from qiskit_aer import noise
from qiskit_aer.noise import (NoiseModel, depolarizing_error)

def scale_noise(factor, noise_model):

    # for j in range(len(noise_model._custom_noise_passes)):
    #     noise_model._custom_noise_passes[j]._t1s *= factor
    #     noise_model._custom_noise_passes[j]._t2s *= factor
    #     noise_model._custom_noise_passes[j]._dt *= factor

    for item in noise_model._local_readout_errors:
        offset = 1.0 - noise_model._local_readout_errors[item].probabilities[0, 0]
        offset *= factor
        noise_model._local_readout_errors[item].probabilities[0, 0] = 1.0 - offset
        noise_model._local_readout_errors[item].probabilities[0, 1] = offset
        noise_model._local_readout_errors[item].probabilities[1, 0] = offset
        noise_model._local_readout_errors[item].probabilities[1, 1] = 1.0 - offset


    for item in noise_model._local_quantum_errors:
        for subitem in noise_model._local_quantum_errors[item]:

            offset = 1.0 - noise_model._local_quantum_errors[item][subitem].probabilities[0]
            new_offset = offset * np.float64(factor)
            noise_model._local_quantum_errors[item][subitem].probabilities[0] = 1.0 - new_offset
            fa = new_offset / offset

            for j in range(len(noise_model._local_quantum_errors[item][subitem].probabilities)-1):
                noise_model._local_quantum_errors[item][subitem].probabilities[j+1] *= fa


    return noise_model



def model0():

    return None

def model1(scale=1.0):

    backend = FakeSydneyV2()
    noise_model = NoiseModel.from_backend(backend)

    if scale != 1.0:
        noise_model = scale_noise(scale, noise_model)

    return noise_model


def model2(p):
    # create a bit flip error with probability p = 0.01
    # p = 0.0001
    my_bitflip = noise.pauli_error([('X', p), ('I', 1 - p)])

    # create an empty noise model
    noise_model = noise.NoiseModel()

    # attach the error to the hadamard gate 'h'
    # noise_model.add_quantum_error(my_bitflip, ['h'], [0])
    noise_model.add_all_qubit_quantum_error(my_bitflip, ['u1', 'u2', 'u3', 'uc', 'UCPauliRotGate'])

    return noise_model


def model3():

    noise_model = NoiseModel()

    # Add depolarizing error to all single qubit u1, u2, u3 gates
    error = depolarizing_error(1.1, 1)
    noise_model.add_all_qubit_quantum_error(error, ['u1', 'u2', 'u3'])

    return noise_model


noise_model = model1()
noise_models = {'NoNoise': model0(),
                'BitFlip1': model2(0.001),
                'BitFlip2': model2(0.003),
                'BitFlip3': model2(0.005),
                'BitFlip4': model2(0.007),
                'FakeSydneyV2': model1()
                }

noise_models = {'NoNoise': model0(),
                # 'BitFlip1': model2(0.001),
                # 'BitFlip2': model2(0.003),
                # 'BitFlip3': model2(0.005),
                # 'BitFlip4': model2(0.007),
                'FakeSydneyV2': model1()
                }