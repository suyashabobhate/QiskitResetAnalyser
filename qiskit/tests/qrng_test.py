# https://quantumcomputinguk.org/tutorials/16-qubit-random-number-generator

import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np

# Create a quantum circuit with a single qubit
qrng_circuit = QuantumCircuit(1)

# Apply a Hadamard gate to create a superposition of |0⟩ and |1⟩ states
qrng_circuit.h(0)

# Measure the qubit
qrng_circuit.measure(0)

# Define the backend for simulation
backend = Aer.get_backend('qasm_simulator')

# Number of random samples
num_samples = 3

compiled_circuit = transpile(qrng_circuit, backend)

# Execute the circuit on the simulator
job = backend.run(compiled_circuit, shots=1024)
result = job.result()
counts = result.get_counts()

print("counts :", counts)

# Get a random index for fetching the key from the dictionary
r = (int)(np.random.randint(2))

# Extract the random bit (0 or 1)
random_bit = list(counts.keys())[r]

print("Random bit:", random_bit)

qrng_circuit.h(0)
