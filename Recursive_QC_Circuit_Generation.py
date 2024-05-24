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

# recursive function
def buildComponent(circuit, m, n, np):
    gate = QuantumCircuit(np)
    if m == 2:
        gate.ccx(0, 1, int((np+1)/2))
        return circuit.compose(gate)
    else:
        gate.ccx(m-1, n-2, n-1)
        circuit = circuit.compose(gate)
        circuit = ((buildComponent(circuit, m-1, n-1, np))).compose(gate)
        return circuit

# function to build circuit
def build(circuit, m, n, np):
    component = buildComponent(circuit, m-1, n-1, np)
    for x in range(2):
        circuit.ccx(m-1, n-2, n-1)
        circuit = circuit.compose(component)
    return circuit

# function to build boolean oracle
def boolean_oracle(marked_state):
    n = len(marked_state[0])
    qc = QuantumCircuit(n, name='bit-flip oracle')
    qc = build(qc, int((n+1)/2), n, n)
    return qc

# define solution to search for
marked_state =["00111"]

# number of qubits
n = len(marked_state[0])
w = int((n+1)/2)

# define Z gate according to marked state
zGate = QuantumCircuit(n)
zGate.x(3)
zGate.x(4)
zGate = zGate.compose(MCMT('z', num_ctrl_qubits=n-1, num_target_qubits=1))
zGate.x(3)
zGate.x(4)

# create bit-flip boolean oracle based on solution
bitFlipOracle = QuantumCircuit(n)
bitFlipOracle = bitFlipOracle.compose(boolean_oracle(marked_state))

# use Z gate to convert from bit-flip oracle into phase-flip oracle
phaseFlipOracle = QuantumCircuit(n, name='phase-flip oracle')
phaseFlipOracle = phaseFlipOracle.compose(bitFlipOracle)
phaseFlipOracle.barrier()
phaseFlipOracle = phaseFlipOracle.compose(zGate)
phaseFlipOracle.barrier()
phaseFlipOracle.draw()
#print("Phase Flip Oracle Circuit\n", phaseFlipOracle)

# calculate power
power = math.floor(math.pi/4 * math.sqrt(2**w))

# run Grover's algorithm
problem = AmplificationProblem(phaseFlipOracle, is_good_state=marked_state)
#print("Grover Op", problem.grover_operator.decompose())

grover = Grover(sampler=Sampler())
result = grover.amplify(problem)
display(plot_histogram(result.circuit_results, figsize=(20,5)))
      