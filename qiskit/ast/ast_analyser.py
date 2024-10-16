import ast

class ResetCheckAnalyzer(ast.NodeVisitor):

    def __init__(self):
        # self.size_value = 0
        self.current_term = 0
        self.used_qubits = {}  # Track which qubits have been used
        self.assigned_vars = {}

    def visit_Assign(self, node):
        # Store all assigned variable values
        if isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            if isinstance(node.value, ast.Constant):
                self.assigned_vars[var_name] = node.value.value
                print(self.assigned_vars)
        
        self.generic_visit(node)

    def visit_For(self, node):
        # Check if for exists for any gate operation or resets
        for node_value in node.body:
            if isinstance(node_value, ast.Expr) and isinstance(node_value.value, ast.Call):
                # Check for operations
                if isinstance(node_value.value.func, ast.Attribute):
                    method_name = node_value.value.func.attr
                    # Proceed only if "range" of for
                    if isinstance(node.iter, ast.Call) and node.iter.func.id == "range":
                        if node.iter.args and isinstance(node.iter.args[0], ast.Constant):
                            var_value = node.iter.args[0].value
                            self.apply_op(method_name, 0, var_value)
                        elif node.iter.args and isinstance(node.iter.args[0], ast.Name):
                            if self.assigned_vars[node.iter.args[0].id]:
                                var_name = node.iter.args[0].id
                                # add functionality for range(lower, upper) :- args[0], args[1] and for formula ranges :- size - 1
                                self.apply_op(method_name, 0, self.assigned_vars[var_name])

                        print(self.used_qubits)
                    
        self.generic_visit(node)

    def apply_op(self, method_name, lower_limit, upper_limit):
        for qubit in range(lower_limit, upper_limit):
            if method_name in ('h', 'x', 'measure', 'cx'):
                if qubit in self.used_qubits and self.used_qubits[qubit] != self.current_term:
                    print(f"Error: Qubit {qubit} is being reused without reset")
                else:
                    self.used_qubits[qubit] = self.current_term
        
            elif method_name == 'reset':
                # Reset qubits by deleting them
                if qubit in self.used_qubits:
                    del self.used_qubits[qubit]
            
            # Increase term everytime run is operated
            elif method_name == 'run':
                self.current_term += 1

    def visit_Call(self, node):
        # Get size of the circuit
        if isinstance(node.func, ast.Name) and node.func.id == 'QuantumCircuit':
            # Check if the assigned value is a constant (like size = 3)
            if isinstance(node.args[0], ast.Constant):
                self.size_value = node.value.value
            elif isinstance(node.args[0], ast.Name):
                var_name = node.args[0].id

                if var_name in self.assigned_vars:
                    self.size_value = self.assigned_vars[var_name]
                else:
                    print(f"No variable named {var_name} has been assigned")

        # Check for operations
        if isinstance(node.func, ast.Attribute):
            method_name = node.func.attr

            if method_name in ('h', 'x', 'measure', 'cx'):
                if isinstance(node.args[0], ast.Constant):
                    qubit_value = node.args[0].value

                    if qubit_value in self.used_qubits and self.used_qubits[qubit_value] != self.current_term:
                        print(f"Error: Qubit {qubit_value} is being reused without reset")
                    else:
                        self.used_qubits[qubit_value] = self.current_term

            elif method_name == 'reset':
                if isinstance(node.args[0], ast.Constant):
                    qubit_value = node.args[0].value

                    # Reset qubits by deleting them
                    if qubit_value in self.used_qubits:
                        del self.used_qubits[qubit_value]

            # Increase term everytime run is operated
            elif method_name == 'run':
                self.current_term += 1


        self.generic_visit(node)



def generate_AST(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    tree = ast.parse(code)  # Parse the code to an AST
    analyzer = ResetCheckAnalyzer()
    analyzer.visit(tree)  # Visit all nodes


generate_AST('qiskit/uniform/uniform.py')