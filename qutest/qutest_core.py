"""Implementation of QUTest class library."""

from abc import ABC, abstractmethod
import types
import time
from colorama import Fore
import numpy as np
import qiskit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeSydneyV2
from qiskit_experiments.library import StateTomography, ProcessTomography
from qiskit.quantum_info import state_fidelity, process_fidelity
from qutest.aux_functions import make_keys, parse_code
from scipy.stats import chisquare
import inspect
from functools import partial


class Proj(object):
    """This class defines the structure of a testing experiment based on
    the projective measurements in computational basis.
    """

    def __init__(self, qc):
        self.qc = qc

    def run(self, backend, shots=100, seed_simulation=1111):
        circ = qiskit.transpile(self.qc, backend)
        results = backend.run(circ, shots=shots, seed_simulator=seed_simulation).result()
        counts = results.get_counts()

        return counts


class QUT(ABC):
    """Abstract base class for quantum unit test (QUT) orchestrators.

    This class provides a framework for designing orchestrators which facilitates running quantum unit tests.
    Subclasses are expected to implement specific orchestrators that operate in accordance to a chosen test protocols.
    The class manages backend selection, test configuration, and output handling.

    Attributes:
        SEED (int):
            A fixed seed used to initialize all classical random number generators
            during simulation, ensuring reproducibility.
        backend (BackendV1):
            The quantum backend to run the tests on. If not provided, defaults to
            an AerSimulator initialized from the FakeSydneyV2 backend.
        params (list):
            A list of classical parameters passed to the quantum subroutine being tested.
        output_data (dict):
            A dictionary used to store intermediate and final results generated during testing.
        title (str):
            An optional string displayed with the test result for identification or debugging.
        shots (int):
            The number of shots (circuit executions) for each experiment, defaulting to 2000.
        experiment (any):
            A placeholder for the quantum protocol or test case implementation to be defined in subclasses.
    """

    SEED = 100  # seed value for all random number generators on a classical simulator

    def __init__(self, **kwargs):

        default_backend = AerSimulator.from_backend(FakeSydneyV2())  # default backend if 'backend'=None is specified
        self.backend = kwargs.get('backend', default_backend)
        self.params = []  # classical arguments for a subroutine
        self.output_data = {}  # container for intermediate data
        # generated during testing
        self.title = kwargs.get('title', '')  # message to show with the test outcome
        self.shots = kwargs.get('shots', 2000)  # default number of shots for all experiments
        self.experiment = None  # testing experiment

    def setUp(self):
        """Setting up environment parameters and values of arguments for unit testing.
        If not specified, default values for initial state of a quantum register and
        classical arguments will be used.
        """
        pass

    @abstractmethod
    def expected(self):
        """Output the expected values of the tests outcomes consistent with assertion arguments
        of a chosen experiment. This function must be redefined in the child class implementing
        a unit test.
        """
        pass

    @abstractmethod
    def assertEqual(self, arg1, arg2):
        """Defines the method for evaluating the assertion statement that is consistent with
        assertion arguments of a chosen experiment. This function must be redefined in the child class
        that implements a concrete orchestrator or unit test.

        Args:
            arg1, arg2: arguments for the assertion.

        Returns:
            float: probability that the assertion statement is true.
        """
        return 0.0

    @abstractmethod
    def workflow(self, qc):
        """Defines the full testing workflow including operations specified by a experiment,
        data cleaning and post-processing. This function can be also considered as a modifier or
        a wrapper function for the experiment. This function must be redefined in the child class
        implementing a concrete orchestrator or unit test.
        """
        pass

    def run(self, unit):
        """Runs the test orchestrator by implementing standard steps common for all unit tests:
        - setting-up the testing environment,
        - running defined workflow based on the chosen experiment,
        - determining the expected output, and
        - evaluating the assertion statement.

        Args:
            unit: function defining the quantum subroutine under testing.
        """

        unit = parse_code(unit)

        self.print_head()
        qc = self.setUp()

        if isinstance(unit, types.FunctionType):
            try:
                qc = unit(qc, *self.params)
            except TypeError:
                qc = unit(qc)
        elif isinstance(unit, qiskit.circuit.quantumcircuit.QuantumCircuit):
            if isinstance(qc, qiskit.circuit.quantumcircuit.QuantumCircuit):
                qc = qc.compose(unit)
            else:
                qc = unit
        else:
            raise TypeError

        res = self.workflow(qc)
        res_expected = self.expected()
        res = self.assertEqual(res, res_expected)
        self.output_data['fid'] = res
        self.print_result(res)

        return self

    def print_result(self, fid):
        """Prints out the result of test evaluation."""

        if fid >= 0.95:
            print(Fore.GREEN + '[PASSED]: with a {:1.3f} probability of passing.'.format(fid) + Fore.RESET)
        elif 0.96 > fid >= 0.9:
            print(Fore.YELLOW + '[UNCERTAIN]: with a {:1.3f} probability of passing.'.format(fid) + Fore.RESET)
        else:
            print(Fore.RED + '[FAILED]: with a {:1.3f} probability of passing.'.format(fid) + Fore.RESET)

    def print_head(self):
        """Prints out a head message before running the test."""

        print(self.title)


class QUT_PT(QUT, ABC):
    """This class defines quantum orchestrator based on the quantum process tomography as a testing experiment.
       The children of this class are unit tests based on the quantum process tomography."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.experiment = ProcessTomography

    def assertEqual(self, arg1, arg2):
        return process_fidelity(arg1, arg2, require_tp=False)

    def workflow(self, qc):
        qstexp = self.experiment(qc)
        start = time.time()
        qstdata = qstexp.run(self.backend, seed_simulation=QUT.SEED, shots=self.shots).block_for_results()
        res = qstdata.analysis_results("state").value
        end = time.time()
        self.output_data['time'] = end - start
        self.output_data['rho'] = res

        return res


class QUT_ST(QUT, ABC):
    """This class defines quantum orchestrator based on the quantum state tomography as a testing experiment.
       The children of this class are unit tests based on the quantum state tomography."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.experiment = StateTomography
        self.basis_indices = kwargs.get('basis_indices', None)
        self.measurement_indices = kwargs.get('measurement_indices', None)

    def assertEqual(self, arg1, arg2):
        return state_fidelity(arg1, arg2)

    def workflow(self, qc):
        qstexp = self.experiment(qc,
                                 basis_indices=self.basis_indices,
                                 measurement_indices=self.measurement_indices)

        start = time.time()
        # qstdata = qstexp.run(self.backend, seed_simulation=SEED, shots=self.shots, fitter="cvxpy_gaussian_lstsq").block_for_results()
        qstdata = qstexp.run(self.backend, seed_simulation=QUT.SEED, shots=self.shots).block_for_results()
        res = qstdata.analysis_results("state").value
        end = time.time()
        self.output_data['time'] = end - start
        self.output_data['rho'] = res

        return res


class QUT_PROJ(QUT, ABC):
    """This class defines quantum orchestrator based on the projective measurements
    in the computational basis as a testing experiment. The children of this class are
    unit tests based on the projective measurements and Pearson's chi-squared test on the obtained data.

        Example:
    >>> import math
    >>> import qiskit
    >>> import qutest
    >>> from qiskit_aer import AerSimulator
    >>>
    >>> def quantum_subprogram(circuit):
    ...     circuit.rx(math.pi / 2, 0)
    ...     return circuit
    >>>
    >>> class MyTests(qutest.QUTest):
    ...
    ...     def test_1(self):
    ...         quantum_input = qiskit.QuantumCircuit(1)
    ...         quantum_input = quantum_subprogram(quantum_input)
    ...         self.assertEqual['RelFreqCounts'](quantum_input, [0.5, 0.5])
    >>>
    >>> MyTests(backend=AerSimulator(), shots=2000).run()
    <BLANKLINE>
    {GREEN}[PASSED]: with a 0.999 probability of passing.{RESET}
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.experiment = Proj

    def assertEqual(self, arg1, arg2):
        arg1 = np.array(arg1) + 0.0001
        arg2 = np.array(arg2) + 0.0001

        ind = np.where(arg2 != 0)

        arg1 = arg1[ind] / self.shots
        arg2 = arg2[ind]

        fid = chisquare(f_obs=arg1, f_exp=arg2, sum_check=False, ddof=len(arg1) - 2)
        return fid.pvalue

    def workflow(self, qc):
        qc.measure_all()
        qstexp = self.experiment(qc)
        start = time.time()
        res = qstexp.run(self.backend, seed_simulation=QUT.SEED, shots=self.shots)
        end = time.time()
        self.output_data['time'] = end - start
        keys = set(make_keys(qc.num_qubits))
        diff_keys = keys.difference(res.keys())
        res.update(dict(zip(diff_keys, [0] * len(diff_keys))))
        res = dict(sorted(res.items()))
        self.output_data['rho'] = res

        return list(res.values())


def colors_in_doctests(func): # wrapper func that alters the docstring
    func.__doc__ = func.__doc__.format(**{"GREEN": Fore.GREEN, "RED": Fore.RED, "RESET": Fore.RESET})
    return func

@colors_in_doctests
class QUTest(object):
    """
    Base class for quantum test suites. It also implements context-aware orchestration of the testing process,
    where the context is determined by the assertion function being used. The context determines the testing
    protocol to be invoked.

    Currently, the assertion methods evaluate the equivalence of:

    - Measurement outcome relative frequencies
    - Density matrices (quantum states)
    - Choi matrices (quantum processes)

    Example:
    >>> import math
    >>> import qiskit
    >>> import qutest
    >>> from qiskit_aer import AerSimulator
    >>>
    >>> def quantum_subprogram(circuit):
    ...     circuit.rx(math.pi / 2, 0)
    ...     return circuit
    >>>
    >>> class MyTests(qutest.QUTest):
    ...
    ...     def test_1(self):
    ...         quantum_input = qiskit.QuantumCircuit(1)
    ...         quantum_input = quantum_subprogram(quantum_input)
    ...         self.assertEqual['RelFreqCounts'](quantum_input, [0.5, 0.5])
    >>>
    >>> MyTests(backend=AerSimulator(), shots=2000).run()
    <BLANKLINE>
    {GREEN}[PASSED]: with a 0.999 probability of passing.{RESET}
    """

    def __init__(self, **kwargs):

        self.tests: list[QUT] = []  # container for the test object containing all the tests' intermediate data

        # unpack the specified parameters into the object attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def assertEqual(self, circuit, value):

        context = self._identify_context(circuit, value)
        self._assertEqual(circuit, value, context=context)

    def _identify_context(self, circuit, value):

        if isinstance(value, np.ndarray) and value.ndim == 1:
            print('QUT_PROJ')
            return QUT_PROJ
        if (isinstance(value, qiskit.quantum_info.DensityMatrix) or
                (isinstance(value, np.ndarray) and value.ndim == 2)):
            print('QUT_ST')
            return QUT_ST
        if isinstance(value, qiskit.quantum_info.Choi):
            print('QUT_PT')
            return QUT_PT
        else:
            raise ValueError("Can't identify context for the assertion")


    def _assertEqual(self, circuit, value, context):

        if 'setUp' in dir(self):
            set_setup = getattr(self, 'setUp')
        else:
            def set_setup():
                pass

        class MyTest(context):
            """Class prepares environment for quantum unit tests
            which is determined by the contextual information"""

            def setUp(self):
                set_setup()

            def expected(self):
                return value

        strategy = MyTest(**self.__dict__)
        strategy.run(circuit)
        self.tests.append(strategy)

    def run(self):
        """Executes all test methods in this class whose names start with 'test'."""

        attrs = (getattr(self, self.__class__.__name__) for self.__class__.__name__ in dir(self))
        test_methods = filter(inspect.ismethod, attrs)

        for test_method in test_methods:
            try:
                if test_method.__name__.startswith('test'):
                    test_method()
            except TypeError:
                # Can't handle methods with required arguments.
                pass


if __name__ == '__main__':
    class MyTest(QUT_PT):
        def setUp(self):
            pass

        def expected(self):
            pass


    aaa = MyTest()
    aaa.run()


    class MyTests(QUTest):
        def setUp(self):
            pass

        def test_1(self):
            pass

        def test_2(self):
            pass


    bbb = MyTests()
    bbb.run()
