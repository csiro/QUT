import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix, Choi
from qiskit_aer import AerSimulator
from qut import detach
from qiskit_experiments.library import StateTomography, ProcessTomography
from qiskit.quantum_info import state_fidelity, process_fidelity
from qiskit import transpile
from scipy.stats import chisquare
from qut.aux_functions import make_keys, parse_code
from colorama import Fore

@detach
def subroutine_correct(circuit):
    circuit.x(0)  # apply Hadamard gate to the first qubit
    circuit.h(0)  # apply phase shift gate to the first qubit
    circuit.cx(0, 1)
    return circuit


@detach
def subroutine_error(circuit):
    circuit.x(0)  # apply Hadamard gate to the first qubit
    circuit.h(1)  # apply phase shift gate to the first qubit
    circuit.cx(0, 1)
    return circuit

# ----------------------------------------------------------------------------------------------------------

def print_result(fid):
    """Prints out the result of test evaluation."""

    if fid >= 0.95:
        print(Fore.GREEN + '[PASSED]: with a {:1.3f} probability of passing.'.format(fid) + Fore.RESET)
    elif 0.96 > fid >= 0.9:
        print(Fore.YELLOW + '[UNCERTAIN]: with a {:1.3f} probability of passing.'.format(fid) + Fore.RESET)
    else:
        print(Fore.RED + '[FAILED]: with a {:1.3f} probability of passing.'.format(fid) + Fore.RESET)



SEED=100
shots = 3000
backend = AerSimulator()

def test_proj(subroutine, qc, expected):

    qc = subroutine(qc)
    qc.measure_all()
    circ = transpile(qc, backend)
    results = backend.run(circ, shots=shots, seed_simulator=SEED).result()
    counts = results.get_counts()
    keys = set(make_keys(qc.num_qubits))
    diff_keys = keys.difference(counts.keys())
    counts.update(dict(zip(diff_keys, [0] * len(diff_keys))))
    counts = dict(sorted(counts.items()))
    count_freq = np.array(list(counts.values())) / shots
    delta = 0.0001
    expected = np.array(expected) + delta
    count_freq = np.array(count_freq) + delta
    metric = chisquare(f_obs=expected, f_exp=count_freq, sum_check=False, ddof=len(expected) - 2)
    metric = metric.pvalue
    print_result(metric)


def test_st(subroutine, qc, expected):

    qc = subroutine(qc)
    qstexp = StateTomography(qc)
    qstdata = qstexp.run(backend, seed_simulation=SEED, shots=shots).block_for_results()
    res = qstdata.analysis_results("state").value
    metric = state_fidelity(res, expected)
    print_result(metric)


def test_pt(subroutine, qc, expected):

    qc = subroutine(qc)
    qstexp = ProcessTomography(qc)
    qstdata = qstexp.run(backend, seed_simulation=SEED, shots=shots).block_for_results()
    res = qstdata.analysis_results("state").value
    metric = process_fidelity(res, expected, require_tp=False)
    print_result(metric)


if __name__=='__main__':

    qinput = QuantumCircuit(2)
    expected_count_freq = np.array([0.5, 0, 0, 0.5])
    expected_dens_mat = DensityMatrix([[0.5, 0.0, 0.0, -0.5],
                                    [0.0, 0.0, 0.0, 0.0],
                                    [0.0, 0.0, 0.0, 0.0],
                                    [-0.5, 0.0, 0.0, 0.5]])
    expected_choi = Choi(subroutine_correct(qinput))

    test_proj(subroutine_correct, qinput, expected_count_freq)
    test_st(subroutine_correct, qinput, expected_dens_mat)
    test_pt(subroutine_correct, qinput, expected_choi)
    test_proj(subroutine_error, qinput, expected_count_freq)
    test_st(subroutine_error, qinput, expected_dens_mat)
    test_pt(subroutine_error, qinput, expected_choi)






