# QiskitResetAnalyser
This repo contains our work on a reset error-checking analyser for Qiskit. 

## Introduction
Resetting qubits is the process of bringing a qubit back to a ∣0⟩ during or after a quantum computation. This ensures that the qubit is ready for reuse or proper measurement.
It is crucial for **error mitigation**, as residual information from previous computations can cause cascading errors. It also ensures **reusability** by allowing limited qubits to be reused, enabling more complex algorithms with fewer resources. Resetting also guarantees **state initialization**, starting qubits in a defined state (∣0⟩), which is essential for many quantum algorithms.

### Qiskit Reset
IBM Qiskit is an open-source software development kit for working with quantum computers at the level of circuits, pulses, and algorithms.

The _reset()_ function in Qiskit adds a reset instruction to the quantum circuit, ensuring qubits are returned to the ∣0⟩ state. This operation is managed by Qiskit's internal logic and is executed by the quantum backend, whether a simulator or actual hardware. It is independent of the Python compiler or the IDE you use, relying solely on the Qiskit library and the backend's ability to process quantum instructions. Qiskit does not inherently validate whether a qubit is properly reset before reuse. It does not enforce strict constraints, allowing advanced users to experiment with quantum algorithms, even in cases where reusing qubits without reset might be intentional.

### Our work
Our reset error-checking analyser is used to assert the Qiskit user that they are reusing non resseted qubits. This enables them to strictly use the Qiskit _reset()_ function if reusing the same qubits in next term(term defines the time from when there are zero active qubits till when the circuit is run using the _run()_ operation in Qiskit). This ultimately mitigates any possible noise thereby increasing the reliability. Our analyser uses the AST of the program to identify any qubits being reused before resetted.

## Repo Structure
The analyser was tested on below four tests located at **_QiskitResetAnalyser/qiskit/tests/_** :
- _common_test.py_
  * This program contains all different combinations of gate operations on a quantum circuit using Qiskit. This also showcases different conditions on which our analyser can correctly identify the errors, for example: gate operations in for loops, single statement gate operations and their combination.
- _grover_test.py_
  * This is a famous quantum computing search algorithm implemented using Qiskit.
- _qrng_test.py_
  * This is a quantum random number generator using Qiskit.
- _uniform_simple_test.py_
  * This is a quantum program used to generate a uniform distribution using Qiskit.
    
The analyser main code and helper files are located at **_QiskitResetAnalyser/qiskit/ast/_** :
- _ast_analyser.py_
  * This is the main code of analyser. It uses _ast_generator.py_ to generate AST of program and then proceeds to go through different node classes of generated AST. It uses Python dictionary to track the active qubits in each term. It is primarily used to verify if the qubits are being resetted before resuing them again in the next term.
- _ast_generator.py_
  * This generates AST of programs.
- _ast_output.txt_
  * Example output of AST.

The test script for running the above tests is located at **_QiskitResetAnalyser/qiskit/scripts_** :
- _pytest_output.txt_
  * This shows the output of _test_script.py_ using the command
    ```
    pytest -s qiskit/scripts/test_script.py
    ```
- _test_output.txt_
- _test_output_quiet.txt_
- _test_script.py_
  * This is a script which uses _pytest_ module to perform testing on two functions:
    - test_ast_fail() - This test passes if the analyser is successfully able to identify any reset errors in the program.
    - test_ast_pass() - This test passes if the analyser is successfully able to assert that no reset errors are found in the program.

## Instructions
To run _test_script.py_, simply use the following command in the terminal or command line. Note that this command is run from the root folder.
```
pytest -s qiskit/scripts/test_script.py
```
The -s flag helps to display the print statements used in the test script. This also contains the output log of the analyser. The output is located at **_QiskitResetAnalyser/qiskit/scripts/pytest_output.txt_**.

If you want to run separate functions, use the following commands:
```
pytest -s qiskit/scripts/test_script.py::test_ast_fail
```

```
pytest -s qiskit/scripts/test_script.py::test_ast_pass
```

Running the test script using the follwing command:
```
pytest qiskit/scripts/test_script.py
```
will generate output:
```
============================================ test session starts =============================================
platform darwin -- Python 3.9.7, pytest-8.3.4, pluggy-1.5.0
collected 4 items                                                                                            

qiskit/scripts/test_script.py ....                                                                     [100%]

============================================= 4 passed in 0.06s ==============================================
```

## Things to remember
While working with our analyser, following guidelines are to be strictly followed:
- Use of functions
  * Program code with functions which are used to create quantum circuits and operate on qubits using gates are not compatible with our analyser. Please make sure to run the analyser only on the main function of the program.
  * Example of a non working code:
    ```
    def grover_oracle(marked_states):
      """Build a Grover oracle for multiple marked states."""
      if not isinstance(marked_states, list):
          marked_states = [marked_states]
      num_qubits = len(marked_states[0])
      qc = QuantumCircuit(num_qubits)
      for target in marked_states:
          rev_target = target[::-1]
          zero_inds = [ind for ind in range(num_qubits) if rev_target.startswith("0", ind)]
          qc.x(zero_inds)
          qc.compose(MCMT(ZGate(), num_qubits - 1, 1), inplace=True)
          qc.x(zero_inds)
      return qc

    marked_states = ["0111", "100", "110"]
    oracle = grover_oracle(marked_states)
    grover_op = GroverOperator(oracle)
    
    optimal_num_iterations = math.floor(math.pi / (4 * math.asin(math.sqrt(len(marked_states) / 2**grover_op.num_qubits))))
    
    qc = QuantumCircuit(grover_op.num_qubits)
    qc.h(range(grover_op.num_qubits))
    qc.compose(grover_op.power(optimal_num_iterations), inplace=True)
    qc.measure_all()
    
    backend = Aer.get_backend('aer_simulator')
    compiled_circuit = transpile(qc, backend)
    
    # Execute the circuit on the simulator
    job = backend.run(compiled_circuit, shots=1024)
    ```
- Use of built in python functions
  * When using built in function like _range()_, it is advised to pass either a constant or a defined variable. Passing an arithemetic expression or some other built in functions like _len()_ will break the analyser.
  * Example of a non working code:
    ```
    for q in range(2 + 8):
    qc.h(q)
    ```

    ```
    for q in range(size - 2):
    qc.h(q)
    ```

    ```
    marked_states = ["0111", "100", "110"]
    num_qubits = len(marked_states[0])
    qc = QuantumCircuit(num_qubits)
    ```

## Documentation

## Citations
```bibtex
@misc{qiskit2024,
      title={Quantum computing with {Q}iskit},
      author={Javadi-Abhari, Ali and Treinish, Matthew and Krsulich, Kevin and Wood, Christopher J. and Lishman, Jake and Gacon, Julien and Martiel, Simon and Nation, Paul D. and Bishop, Lev S. and Cross, Andrew W. and Johnson, Blake R. and Gambetta, Jay M.},
      year={2024},
      doi={10.48550/arXiv.2405.08810},
      eprint={2405.08810},
      archivePrefix={arXiv},
      primaryClass={quant-ph}
}
```

## References
[Qiskit](https://www.ibm.com/quantum/qiskit)</br>
[Qiskit Wikipedia](https://en.wikipedia.org/wiki/Qiskit)</br>
[Grover](https://qiskit-community.github.io/qiskit-algorithms/tutorials/07_grover_examples.html)</br>
[Quantum Random Number Generator](https://quantumcomputinguk.org/tutorials/16-qubit-random-number-generator)</br>



