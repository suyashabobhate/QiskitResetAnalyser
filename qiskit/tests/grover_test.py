import math
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import GroverOperator, MCMT, ZGate
from qiskit.visualization import plot_histogram
from qiskit_aer import Aer

marked_states = ["011", "100", "110"]

"""Build a Grover oracle for multiple marked states."""
if not isinstance(marked_states, list):
    marked_states = [marked_states]

num_qubits = 3

oracle = QuantumCircuit(num_qubits)

for target in marked_states:
    rev_target = target[::-1]
    zero_inds = [ind for ind in range(num_qubits) if rev_target.startswith("0", ind)]
    oracle.x(zero_inds)
    oracle.compose(MCMT(ZGate(), num_qubits - 1, 1), inplace=True)
    oracle.x(zero_inds)

grover_op = GroverOperator(oracle)

optimal_num_iterations = math.floor(math.pi / (4 * math.asin(math.sqrt(len(marked_states) / 2**grover_op.num_qubits))))

qc = QuantumCircuit(num_qubits)

for q in range(num_qubits):
    qc.h(q)

qc.compose(grover_op.power(optimal_num_iterations), inplace=True)

for q in range(num_qubits):
    qc.measure(q)

backend = Aer.get_backend('aer_simulator')
compiled_circuit = transpile(qc, backend)

# Execute the circuit on the simulator
job = backend.run(compiled_circuit, shots=1024)
result = job.result()

# Get the counts of each state
counts = result.get_counts(compiled_circuit)

# Print the counts
print(f"Counts with reset: {counts}")
plot_histogram(counts, filename="grover/grover")

for q in range(num_qubits):
    qc.h(q)

for q in range(num_qubits):
    qc.measure(q)
