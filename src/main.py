import ast
import astunparse


class TestNodeTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        print(node.name)
        return node


with open("../inputs/hello.py", "r") as in_file:
    content = in_file.read()
p = ast.parse(content)
p = TestNodeTransformer().visit(p)
s = astunparse.unparse(p)

with open("../outputs/hello.py", "w") as out_file:
    out_file.write(s)
