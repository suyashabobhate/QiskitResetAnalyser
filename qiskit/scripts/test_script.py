# Import the necessary module
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../ast')))

import ast_analyser as ast

print("Common unit test started")
ast.parseFile("qiskit/tests/common_test.py")
print("Common unit test ended")

print("-----------------------------------------------------------------------------------------")

print("Unit tests for qrng program started")
ast.parseFile("qiskit/tests/qrng_test.py")
print("Unit tests for qrng program ended")

print("-----------------------------------------------------------------------------------------")

print("Unit tests for grover program started")
ast.parseFile("qiskit/tests/grover_test.py")
print("Unit tests for grover program ended")