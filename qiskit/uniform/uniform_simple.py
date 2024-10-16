# https://quantumcomputinguk.org/tutorials/16-qubit-random-number-generator

import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Calculate the number of qubits needed to represent the range
size = 3

# Create a quantum circuit with the required number of qubits
qrng_circuit = QuantumCircuit(size, size)

# Apply Hadamard gates to create a uniform superposition of basis states
qrng_circuit.h(0)
qrng_circuit.h(1)
qrng_circuit.h(2)

# Measure the qubits to obtain the random number
qrng_circuit.measure(0)
qrng_circuit.measure(1)
qrng_circuit.measure(2)

# Define the backend for simulation
backend = Aer.get_backend('qasm_simulator')

# Number of random samples
num_samples = 10 

# Execute the circuit on the simulator
compiled_circuit = transpile(qrng_circuit, backend)

# Simulate the quantum circuit to generate random numbers
job = backend.run(compiled_circuit, shots=num_samples)
result = job.result()
counts = result.get_counts()

# Reset qubits
qrng_circuit.reset(0)
qrng_circuit.reset(1)
qrng_circuit.reset(2)

# Reuse qubits
qrng_circuit.h(0)
qrng_circuit.h(1)
qrng_circuit.h(2)
