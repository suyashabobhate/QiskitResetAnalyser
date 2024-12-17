# Import the necessary module
import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../ast')))

import ast_analyser as ast

@pytest.mark.parametrize("test_file, test_description", [
    ("qiskit/tests/common_test.py", "Common unit tests"),
    ("qiskit/tests/qrng_test.py", "Unit tests for qrng program"),
    ("qiskit/tests/grover_test.py", "Unit tests for grover program"),
    ("qiskit/tests/uniform_test.py", "Unit tests for uniform program")
])
def test_ast(test_file, test_description, capsys):
    print(f"{test_description} started")
    ast.parseFile(test_file)
    print(f"{test_description} ended")

    captured = capsys.readouterr()

    assert "Error:" not in captured.out, f"Test failed because qubits were reused without being resetted in {test_file}\n Output:\n {captured.out}"