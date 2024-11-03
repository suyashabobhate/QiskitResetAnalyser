import ast

class ResetCheckAnalyzer(ast.NodeVisitor):

    def __init__(self):
        # self.size_value = 0
        self.current_term = 0
        self.used_qubits = {}  # Track which qubits have been used
        self.assigned_vars = {}
        self.op_name = None

    # Function to add used qubits to the dict after applying any operations
    def apply_op(self, lower_limit, upper_limit):
        for qubit in range(lower_limit, upper_limit):
            # Found any operations like gates
            if self.op_name in ('h', 'x', 'measure', 'cx'):
                if qubit in self.used_qubits and self.used_qubits[qubit] != self.current_term:
                    print(f"Error: Qubit {qubit} is being reused without reset")
                # Found unused qubit or resetted qubit
                else:
                    self.used_qubits[qubit] = self.current_term
        
            # Found reset operation
            elif self.op_name == 'reset':
                # Reset qubits by deleting them from the dict
                if qubit in self.used_qubits:
                    del self.used_qubits[qubit]

    # Get operation name
    def getOpName(self, node):
        # This is for "for" loop operations
        if (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)):
            if isinstance(node.value.func, ast.Attribute):
                self.op_name = node.value.func.attr
                self.assigned_vars["op_name"] = self.op_name
        # For the single statement operations
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            self.op_name = node.func.attr
            self.assigned_vars["op_name"] = self.op_name
            
    def visit_Assign(self, node):
        # Store all assigned variable values
        if isinstance(node.targets[0], ast.Name):
            # Get name of the variable
            var_name = node.targets[0].id
            if isinstance(node.value, ast.Constant):
                # Add it to the dict
                self.assigned_vars[var_name] = node.value.value
                print(self.assigned_vars)
        
        self.generic_visit(node)

    # TO DO: add functionality for range(lower, upper) :- args[0], args[1] and for formula ranges :- size - 1
    def visit_For(self, node):
        # Go over every statement in the for loop
        for node_value in node.body: 
            # Get the name of the operation
            self.getOpName(node_value)
            if isinstance(node.iter, ast.Call) and node.iter.func.id == "range":
                # The range of for loop is between 0 and an integer
                if node.iter.args and isinstance(node.iter.args[0], ast.Constant):
                    var_value = node.iter.args[0].value
                    self.apply_op(0, var_value)
                # Range of for loop is between 0 and value of an variable
                elif node.iter.args and isinstance(node.iter.args[0], ast.Name):
                    if self.assigned_vars[node.iter.args[0].id]:
                        var_name = node.iter.args[0].id
                        self.apply_op(0, self.assigned_vars[var_name])
                    
        self.generic_visit(node)

    def visit_Call(self, node):
        # Get size of the circuit
        if isinstance(node.func, ast.Name) and node.func.id == 'QuantumCircuit':
            # Check if the assigned value is a constant (like size = 3)
            if isinstance(node.args[0], ast.Constant):
                self.size_value = node.value.value
            # If the assigned value belongs to variable
            elif isinstance(node.args[0], ast.Name):
                var_name = node.args[0].id
                if var_name in self.assigned_vars:
                    self.size_value = self.assigned_vars[var_name]
                else:
                    print(f"No variable named {var_name} has been assigned")

        # Get name of operation if any
        self.getOpName(node)

        # Increase term everytime run is operated
        if self.op_name == 'run':
            self.current_term += 1
        else:
            # Check for other operations in single statement
            if len(node.args) > 0 and isinstance(node.func, ast.Attribute):
                if isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, int):
                    self.apply_op(node.args[0].value, node.args[0].value + 1)
                    
        self.generic_visit(node)

def generate_AST(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    tree = ast.parse(code)  # Parse the code to an AST
    analyzer = ResetCheckAnalyzer()
    analyzer.visit(tree)  # Visit all nodes

# Start point of running main program
generate_AST('qiskit/uniform/uniform.py')