import ast

class ResetCheckAnalyzer(ast.NodeVisitor):

    def __init__(self):
        # self.size_value = 0
        self.current_term = 0
        self.used_qubits = {}  # Track which qubits have been used


    # def visit_Assign(self, node):
    #     # Check for size block
    #     if isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'size':
    #         # Check if the assigned value is a constant (like size = 3)
    #         if isinstance(node.value, ast.Constant):
    #             self.size_value = node.value.value
        
    #     self.generic_visit(node)

    def visit_Call(self, node):
        # Check for operations
        if isinstance(node.func, ast.Attribute):
            method_name = node.func.attr

            if method_name in ('h', 'x', 'measure', 'cx'):
                if isinstance(node.args[0], ast.Constant):
                    qubit_value = node.args[0].value

                    if qubit_value in self.used_qubits and self.used_qubits[qubit_value] != self.current_term:
                        print(f"Error: Qubit {qubit_value} is being reused without reset")
                    self.used_qubits[qubit_value] = self.current_term

            elif method_name == 'reset':
                if isinstance(node.args[0], ast.Constant):
                    qubit_value = node.args[0].value

                    # Reset qubits by deleting them
                    if qubit_value in self.used_qubits:
                        del self.used_qubits[qubit_value]

            # Increase term everytime run is operated
            elif isinstance(node.func, ast.Attribute) and node.func.attr == 'run':
                self.current_term += 1


        self.generic_visit(node)



def generate_AST(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    tree = ast.parse(code)  # Parse the code to an AST
    analyzer = ResetCheckAnalyzer()
    analyzer.visit(tree)  # Visit all nodes


generate_AST('qiskit/uniform/uniform_simple.py')

# case 1: no reset
# current_term = 0
# {0:[0], 1: [0], 2:[0]}
# no reset 
# current_term = 1
# {0:[0], 1: [0], 2:[0]}
# current_term and key's last value doesnt match - throw error

# case 2: partial reset 
# current_term = 0
# {0:[0], 1: [0], 2:[0]}
# reset on 0 and 2
# {0:[], 1: [0], 2:[]}
# current_term = 1
# operation on 0 and 2
# {0:[1], 1: [0], 2:[1]}
# operation on 1
# current_term and key's last value doesnt match - throw error

# case 3: reset 
# current_term = 0
# {0:[0], 1: [0], 2:[0]}
# reset on 0, 1 and 2
# {0:[], 1: [], 2:[]}
# current_term = 1
# {0:[1], 1: [1], 2:[1]}
# one more operation in same current_term 1
# current_term and key's last value match - no problem