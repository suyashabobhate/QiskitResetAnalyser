# https://quantumcomputinguk.org/tutorials/16-qubit-random-number-generator

import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Define the range (minimum and maximum values)
min_value = 0  # Minimum value
max_value = 3  # Maximum value

# Calculate the number of qubits needed to represent the range
size = 3

# Number of uniformly generated numbers
print("num of qubits", size)

# Create a quantum circuit with the required number of qubits
qrng_circuit = QuantumCircuit(size, size)

# Apply Hadamard gates to create a uniform superposition of basis states
for qubit in range(size):
   qrng_circuit.h(qubit)

# Measure the qubits to obtain the random number
for qubit in range(size):
   qrng_circuit.measure(qubit)

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

# Extract the random numbers as integers from binary and rescale to the desired range
random_numbers = [int(r, 2) + min_value % size for r in counts.keys()]

# Calculate the frequency of each unique value and map it to the integer version of numbers
value_counts = {}
for i in range(len(counts)):
    value_counts[random_numbers[i]] = counts.get(list(counts.keys())[i])

for qubit in range(2):
   qrng_circuit.reset(qubit)

# qrng_circuit.h(2)

for qubit in range(1):
   qrng_circuit.h(2)





