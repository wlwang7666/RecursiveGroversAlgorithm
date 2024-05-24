import qiskit
import math
import matplotlib.pyplot as plt
from qiskit import *
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.visualization import plot_histogram
from qiskit.exceptions import MissingOptionalLibraryError
from qiskit_algorithms import Grover, AmplificationProblem
from qiskit.primitives import Sampler
from qiskit.circuit.library import PhaseOracle, GroverOperator, MCMT
from collections import defaultdict

expression = "A & B & C & ~D & ~E & F & G & H & I & J & K"
power = math.floor(math.pi/4 * math.sqrt(2**11))
print("power: ", power)

oracle = PhaseOracle(expression)
problem = AmplificationProblem(oracle, is_good_state=oracle.evaluate_bitstring)
grover = Grover(iterations=power, sampler=Sampler())
#grover = Grover(ampler=Sampler())
result = grover.amplify(problem)
print(result)
#display(plot_histogram(result.circuit_result[0]))

counts = defaultdict(int)

for inst in problem.grover_operator.decompose().decompose().decompose().decompose().decompose().decompose().decompose().decompose().data:
     counts[len(inst.qubits)] += 1
print("Gate", counts)
