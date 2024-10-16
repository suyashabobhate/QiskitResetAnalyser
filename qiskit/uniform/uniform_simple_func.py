# https://quantumcomputinguk.org/tutorials/16-qubit-random-number-generator

import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

class uniform_simple :

    def __init__(self):
        # Calculate the number of qubits needed to represent the range
        self.size = 3
        # Create a quantum circuit with the required number of qubits
        self.qrng_circuit = QuantumCircuit(self.size, self.size)

    def apply_h(self, qubit) :
        self.qrng_circuit.h(qubit)

    def apply_m(self, qubit) :
        self.qrng_circuit.measure(qubit, qubit)

    def apply_reset(self, qubit) :
        self.qrng_circuit.reset(qubit)

    def run_simulator(self) :
        # Define the backend for simulation
        backend = Aer.get_backend('qasm_simulator')

        # Number of random samples
        num_samples = 10 

        # Execute the circuit on the simulator
        compiled_circuit = transpile(self.qrng_circuit, backend)

        # Simulate the quantum circuit to generate random numbers
        job = backend.run(compiled_circuit, shots=num_samples)
        result = job.result()
        print("here")

us = uniform_simple()
us.__init__()
us.apply_h(0)
us.apply_h(1)
us.apply_h(2)

us.run_simulator()

us.apply_h(0)

us.run_simulator()

