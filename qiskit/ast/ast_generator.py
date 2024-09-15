import ast
import astpretty

# Write path to source file
source_file_path = 'qiskit/uniform/uniform.py'

# Write path to store AST
ast_file_path = 'qiskit/ast/ast_output.txt'

# Read source code from file
with open(source_file_path, 'r') as source_file:
    source_code = source_file.read()

# Parse source code into AST
tree = ast.parse(source_code)

# Print AST and convert it to string
ast_string = astpretty.pformat(tree)

# Write AST string to output file
with open(ast_file_path, 'w') as ast_file:
    ast_file.write(ast_string)

print(f"AST has been written to {ast_file_path}")
