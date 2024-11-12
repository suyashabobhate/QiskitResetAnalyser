import ast

class ResetCheckAnalyzer(ast.NodeVisitor):

    def __init__(self):
        # self.size_value = 0
        self.current_term = 0
        self.used_qubits = {}  # Track which qubits have been used
        self.assigned_vars = {}
        self.op_name = None
        self.inside_for = False

    # Function to add used qubits to the dict after applying any operations
    def apply_op(self, qubit):
        # for qubit in range(lower_limit, upper_limit):
        # Found any operations like gates
        if self.op_name in ('h', 'x', 'measure', 'cx'):
            if qubit in self.used_qubits and self.used_qubits[qubit] != self.current_term:
                print(f"Error: Qubit {qubit} is being reused without reset")
            # Found unused qubit or resetted qubit
            else:
                self.used_qubits[qubit] = self.current_term
                print(f"Qubit {qubit} is assigned operation {self.op_name} in term {self.current_term}")
    
        # Found reset operation
        elif self.op_name == 'reset':
            # Reset qubits by deleting them from the dict
            if qubit in self.used_qubits:
                print(f"Qubit {qubit} is resetted to use in term {self.current_term}")
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

    def checkType(self, node_value):
        if isinstance(node_value, ast.Constant):
            var_value = node_value.value
        elif isinstance(node_value, ast.Name):
            if self.assigned_vars[node_value.id]:
                var_name = node_value.id
                var_value = self.assigned_vars[var_name]
        else:
            return -1

        return var_value
            
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

    def visit_For(self, node):
        self.inside_for = True
        if isinstance(node.iter, ast.Call) and node.iter.func.id == "range":
                if node.iter.args and len(node.iter.args) == 1:
                    lower_limit = 0
                    upper_limit = self.checkType(node.iter.args[0])
                elif node.iter.args and len(node.iter.args) == 2:
                    lower_limit = self.checkType(node.iter.args[0])
                    upper_limit = self.checkType(node.iter.args[1])

        if lower_limit != -1 and upper_limit != -1:
            for qubit in range(lower_limit, upper_limit):
                # Go over every statement in the for loop
                for node_value in node.body: 
                    # Get the name of the operation
                    self.getOpName(node_value)
                    if isinstance(node_value.value.args[0], ast.Constant):
                        self.apply_op(node_value.value.args[0].value)
                    else:
                        self.apply_op(qubit)

        self.generic_visit(node)
        self.inside_for = False

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
            print(f"Updated new term is {self.current_term}")
        else:
            # Check for other operations in single statement
            if len(node.args) > 0 and isinstance(node.func, ast.Attribute):
                if not self.inside_for and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, int):
                    self.apply_op(node.args[0].value)
                    
        self.generic_visit(node)

def generate_AST(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    tree = ast.parse(code)  # Parse the code to an AST
    analyzer = ResetCheckAnalyzer()
    analyzer.visit(tree)  # Visit all nodes

# Start point of running main program
generate_AST('qiskit/uniform/uniform.py')