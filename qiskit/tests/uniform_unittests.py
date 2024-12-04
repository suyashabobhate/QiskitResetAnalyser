# https://quantumcomputinguk.org/tutorials/16-qubit-random-number-generator

import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

####################################### PREPARE THE CIRCUIT #####################################################

# Define the range (minimum and maximum values)
min_value = 0  # Minimum value
max_value = 3  # Maximum value

# Calculate the number of qubits needed to represent the range
size = 3

# Create a quantum circuit with the required number of qubits
qrng_circuit = QuantumCircuit(size, size)

# Define the backend for simulation
backend = Aer.get_backend('qasm_simulator')

# Number of random samples
num_samples = 10 

# Execute the circuit on the simulator
compiled_circuit = transpile(qrng_circuit, backend)

######################################### TESTS BEGIN ###########################################################
'''
TEST NAME : FOR LOOP NO RESET
RESET OPERATIONS ON: NO QUBITS
EXPECTED TO THROW: ERRORS FOR REUSING NON RESETTED QUBITS IN NEW TERM
'''
print("FOR LOOP NO RESET TEST BEGINS")
# TERM 0 BEGINS
# Apply Hadamard gates in Term 0
for qubit in range(size):
   qrng_circuit.h(qubit)

# Apply Measurement gates in Term 0
for qubit in range(size):
   qrng_circuit.measure(qubit)

# Run the cicuit
job = backend.run(compiled_circuit, shots=num_samples)
result = job.result()

# TERM 1 BEGINS
# Apply Hadamard gates in Term 1
for qubit in range(size):
   qrng_circuit.h(qubit)

################################################################################################################
# RESET THE CIRCUIT FOR THE NEXT TEST
for qubit in range(size):
   qrng_circuit.reset(qubit)
################################################################################################################
'''
TEST NAME : FOR LOOP PARTIAL RESET
RESET OPERATIONS ON: SOME QUBITS BUT NOT ALL
EXPECTED TO THROW: ERRORS FOR REUSING NON RESETTED QUBITS IN NEW TERM
'''
print("FOR LOOP PARTIAL RESET TEST BEGINS")

# TERM 0 BEGINS
# Apply Hadamard gates in Term 0
for qubit in range(size):
   qrng_circuit.h(qubit)

# Apply Measurement gates in Term 0
for qubit in range(size):
   qrng_circuit.measure(qubit)

# Run the cicuit
job = backend.run(compiled_circuit, shots=num_samples)
result = job.result()

# TERM 1 BEGINS
# Apply Reset in Term 1 for qubits q0 and q1 but not q2
for qubit in range(0,2):
   qrng_circuit.reset(qubit)

# Apply Hadamard gates in Term 1
for qubit in range(size):
   qrng_circuit.h(qubit)

################################################################################################################
# RESET THE CIRCUIT FOR THE NEXT TEST
for qubit in range(size):
   qrng_circuit.reset(qubit)
################################################################################################################
'''
TEST NAME : FOR LOOP COMPLETE RESET
RESET OPERATIONS ON: ALL QUBITS
EXPECTED TO THROW: NO ERRORS
'''
print("FOR LOOP COMPLETE RESET TEST BEGINS")

# TERM 0 BEGINS
# Apply Hadamard gates in Term 0
for qubit in range(size):
   qrng_circuit.h(qubit)

# Apply Measurement gates in Term 0
for qubit in range(size):
   qrng_circuit.measure(qubit)

# Run the cicuit
job = backend.run(compiled_circuit, shots=num_samples)
result = job.result()

# TERM 1 BEGINS
# Apply Reset in Term 1 for all qubits
for qubit in range(size):
   qrng_circuit.reset(qubit)

# Apply Hadamard gates in Term 1
for qubit in range(size):
   qrng_circuit.h(qubit)

################################################################################################################
# RESET THE CIRCUIT FOR THE NEXT TEST
for qubit in range(size):
   qrng_circuit.reset(qubit)
################################################################################################################
'''
TEST NAME : SINGLE STATEMENT NO RESET
RESET OPERATIONS ON: NO QUBITS
EXPECTED TO THROW: ERRORS FOR REUSING NON RESETTED QUBITS IN NEW TERM
'''
print("SINGLE STATEMENT NO RESET TEST BEGINS")

# TERM 0 BEGINS
# Apply Hadamard gates in Term 0
qrng_circuit.h(0)
qrng_circuit.h(1)
qrng_circuit.h(2)

# Apply Measurement gates in Term 0
qrng_circuit.measure(0)
qrng_circuit.measure(1)
qrng_circuit.measure(2)

# Run the cicuit
job = backend.run(compiled_circuit, shots=num_samples)
result = job.result()

# TERM 1 BEGINS
# Apply Hadamard gates in Term 1
qrng_circuit.h(0)
qrng_circuit.h(1)
qrng_circuit.h(2)

################################################################################################################
# RESET THE CIRCUIT FOR THE NEXT TEST
for qubit in range(size):
   qrng_circuit.reset(qubit)
################################################################################################################
'''
TEST NAME : SINGLE STATEMENT PARTIAL RESET
RESET OPERATIONS ON: SOME QUBITS BUT NOT ALL
EXPECTED TO THROW: ERRORS FOR REUSING NON RESETTED QUBITS IN NEW TERM
'''
print("SINGLE STATEMENT PARTIAL RESET TEST BEGINS")

# TERM 0 BEGINS
# Apply Hadamard gates in Term 0
qrng_circuit.h(0)
qrng_circuit.h(1)
qrng_circuit.h(2)

# Apply Measurement gates in Term 0
qrng_circuit.measure(0)
qrng_circuit.measure(1)
qrng_circuit.measure(2)

# Run the cicuit
job = backend.run(compiled_circuit, shots=num_samples)
result = job.result()

# TERM 1 BEGINS
# Apply Reset in Term 1 for qubits q0 and q1 but not q2
qrng_circuit.reset(0)
qrng_circuit.reset(1)

# Apply Hadamard gates in Term 1
qrng_circuit.h(0)
qrng_circuit.h(1)
qrng_circuit.h(2)

################################################################################################################
# RESET THE CIRCUIT FOR THE NEXT TEST
for qubit in range(size):
   qrng_circuit.reset(qubit)
################################################################################################################
'''
TEST NAME : SINGLE STATEMENT COMPLETE RESET
RESET OPERATIONS ON: ALL QUBITS
EXPECTED TO THROW: NO ERRORS
'''
print("SINGLE STATEMENT COMPLETE RESET TEST BEGINS")

# TERM 0 BEGINS
# Apply Hadamard gates in Term 0
qrng_circuit.h(0)
qrng_circuit.h(1)
qrng_circuit.h(2)

# Apply Measurement gates in Term 0
qrng_circuit.measure(0)
qrng_circuit.measure(1)
qrng_circuit.measure(2)

# Run the cicuit
job = backend.run(compiled_circuit, shots=num_samples)
result = job.result()

# TERM 1 BEGINS
# Apply Reset in Term 1 for all qubits
qrng_circuit.reset(0)
qrng_circuit.reset(1)
qrng_circuit.reset(2)

# Apply Hadamard gates in Term 1
qrng_circuit.h(0)
qrng_circuit.h(1)
qrng_circuit.h(2)

################################################################################################################
# RESET THE CIRCUIT FOR THE NEXT TEST
for qubit in range(size):
   qrng_circuit.reset(qubit)
################################################################################################################
'''
TEST NAME : MULTIPLE FOR LOOP STATEMENTS RESET
RESET OPERATIONS ON: ALL QUBITS
EXPECTED TO THROW: NO ERRORS
'''
print("MULTIPLE FOR LOOP STATEMENTS RESET TEST BEGINS")

# TERM 0 BEGINS
# Apply Hadamard and Measurement gates in Term 0
for qubit in range(size):
   qrng_circuit.h(qubit)
   qrng_circuit.measure(qubit)

# Run the cicuit
job = backend.run(compiled_circuit, shots=num_samples)
result = job.result()

# TERM 1 BEGINS
# Apply Reset in Term 1 for all qubits
for qubit in range(size):
   qrng_circuit.reset(qubit)

################################################################################################################
# RESET THE CIRCUIT FOR THE NEXT TEST
for qubit in range(size):
   qrng_circuit.reset(qubit)
################################################################################################################
'''
TEST NAME : MULTIPLE FOR LOOP AND SINGLE STATEMENTS RESET
RESET OPERATIONS ON: SOME QUBITS BUT NOT ALL
EXPECTED TO THROW: ERRORS FOR NON RESETTED QUBITS IN NEW TERM
'''
print("MULTIPLE FOR LOOP AND SINGLE STATEMENTS RESET TEST BEGINS")

# TERM 0 BEGINS
# Apply Hadamard and Measurement gates in Term 0
for qubit in range(size):
   qrng_circuit.h(qubit)
   qrng_circuit.measure(qubit)

# Run the cicuit
job = backend.run(compiled_circuit, shots=num_samples)
result = job.result()

# TERM 1 BEGINS
# Apply Reset in Term 1 for qubit q0 and Hadamard gate for all qubits including qubit q0
for qubit in range(size):
   qrng_circuit.reset(0)
   qrng_circuit.h(qubit)

################################################################################################################
# RESET THE CIRCUIT FOR THE NEXT TEST
for qubit in range(size):
   qrng_circuit.reset(qubit)
################################################################################################################
'''
TEST NAME : MULTIPLE FOR LOOP AND SINGLE STATEMENTS RESET FOR MULTIPLE TERMS
RESET OPERATIONS ON: ALL QUBITS IN FIRST TERM AND SOME QUBITS IN SECOND TERM
EXPECTED TO THROW: ERRORS FOR NON RESETTED QUBITS IN NEW TERM
'''
print("MULTIPLE FOR LOOP AND SINGLE STATEMENTS RESET FOR MULTIPLE TERMS TEST BEGINS")

# TERM 0 BEGINS
# Apply Hadamard and Measurement gates in Term 0
for qubit in range(size):
   qrng_circuit.h(qubit)
   qrng_circuit.measure(qubit)

# Run the cicuit
job = backend.run(compiled_circuit, shots=num_samples)
result = job.result()

# TERM 1 BEGINS
# Apply Reset in Term 1 for all qubits
for qubit in range(size):
   qrng_circuit.reset(qubit)

# Apply Hadamard and Measurement gates in Term 0
for qubit in range(size):
   qrng_circuit.h(qubit)
   qrng_circuit.measure(qubit)

# Run the cicuit
job = backend.run(compiled_circuit, shots=num_samples)
result = job.result()

# TERM 2 BEGINS
# Apply Hadamard gates in Term 2 for all qubits
for qubit in range(size):
   qrng_circuit.h(qubit)

