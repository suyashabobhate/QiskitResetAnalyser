import ast

class ResetCheckAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.current_term = 0 # Track the current term
        self.used_qubits = {}  # Track which qubits have been used
        self.assigned_vars = {} # Track all assigned variable names and their values
        self.op_name = None # Track the name of the current operation
        self.inside_loop = False # Track whether current statement is inside a loop

    # Function to add used qubits to the dict after applying any operations
    def apply_op(self, qubit):
        # Found any operations like gates
        if self.op_name in ('h', 'x', 'measure', 'cx'):
            # Found mismatch between the current term and qubit term
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
                # Add it to the dict
                self.assigned_vars["op_name"] = self.op_name
        # This is for single statement operations
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            self.op_name = node.func.attr
            # Add it to the dict
            self.assigned_vars["op_name"] = self.op_name

    # Return the value of the node depending on the data type of the node
    def checkType(self, node_value):
        # For constants like 3
        if isinstance(node_value, ast.Constant):
            var_value = node_value.value
        # For variables like size
        elif isinstance(node_value, ast.Name):
            if self.assigned_vars[node_value.id]:
                var_name = node_value.id
                var_value = self.assigned_vars[var_name]
        # No such variable
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
        
        self.generic_visit(node)

    def visit_For(self, node):
        # For loop started
        self.inside_loop = True

        # Get lower and upper limits of for loop based on its range parameter
        if isinstance(node.iter, ast.Call) and node.iter.func.id == "range":
            # One parameter like range(2)
            if node.iter.args and len(node.iter.args) == 1:
                lower_limit = 0
                upper_limit = self.checkType(node.iter.args[0])
            # Two parameters like range(1,2)
            elif node.iter.args and len(node.iter.args) == 2:
                lower_limit = self.checkType(node.iter.args[0])
                upper_limit = self.checkType(node.iter.args[1])

            # Proceed only if lower and upper limits are vaild
            if lower_limit >= 0 and upper_limit >= 0:
                for qubit in range(lower_limit, upper_limit):
                    # Go over every statement in the for loop
                    for node_value in node.body: 
                        # Get the name of the operation
                        self.getOpName(node_value)
                        if isinstance(node_value.value.args[0], ast.Constant):
                            # For circuit.operation(constant_value)
                            self.apply_op(node_value.value.args[0].value)
                        else:
                            # For circuit.operation(variable_name)
                            self.apply_op(qubit)

        self.generic_visit(node)

        # For loop traversed
        self.inside_loop = False

    def visit_Call(self, node):
        # Get name of operation if any
        self.getOpName(node)

        # Increase term everytime run is operated
        if self.op_name == 'run':
            self.current_term += 1
            print(f"Circuit run. Updated new term is {self.current_term}")
        else:
            # Check for other operations in single statement
            if len(node.args) > 0 and isinstance(node.func, ast.Attribute):
                # Proceed only if the statement is not inside a loop
                if not self.inside_loop and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, int):
                    self.apply_op(node.args[0].value)
                    
        self.generic_visit(node)

def generate_AST(code):
    # Parse the code to an AST
    tree = ast.parse(code)
    analyzer = ResetCheckAnalyzer()
    # Visit all nodes
    analyzer.visit(tree)

# Start point of program
def parseFile(file_path):
    if file_path:
        # Read the contents of file
        with open(file_path, 'r') as file:
            code = file.read()
    if code:
        # Pass the code to generate the AST
        generate_AST(code)