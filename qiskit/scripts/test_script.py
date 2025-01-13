import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../ast')))

import ast_analyser as ast

@pytest.mark.parametrize("test_file, test_description", [
    ("qiskit/tests/common_test.py", "Common unit tests"),
    ("qiskit/tests/grover_test.py", "Unit tests for grover program"),
    ("qiskit/tests/uniform_test.py", "Unit tests for uniform program")
])
def test_ast_fail(test_file, test_description, capsys):
    print(f"{test_description} started")
    ast.parseFile(test_file)
    print(f"{test_description} ended")

    captured = capsys.readouterr()

    if "Error:" in captured.out: 
        print(
            f"Analyser identified reset errors : qubits were reused without being resetted in {test_file}\n" 
            f"Output:\n {captured.out}"
        )
    else:
        pytest.fail(
            f"Analyser failed to identify any reset errors : in {test_file}\n"
            f"Output:\n {captured.out}"
        )

@pytest.mark.parametrize("test_file, test_description", [
    ("qiskit/tests/qrng_test.py", "Unit tests for qrng program")
])
def test_ast_pass(test_file, test_description, capsys):
    print(f"{test_description} started")
    ast.parseFile(test_file)
    print(f"{test_description} ended")

    captured = capsys.readouterr()

    if "Error:" not in captured.out: 
        print(
            f"Analyser found no reset errors : in {test_file}\n"
            f"Output:\n {captured.out}"
        )
    else:
        pytest.fail(
            f"Analyser identified reset errors : qubits were reused without being resetted in {test_file}\n"
            f"Output:\n {captured.out}"
        )