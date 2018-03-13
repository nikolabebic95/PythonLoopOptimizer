import ast
import astunparse
import sys
import getopt


class TestNodeTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        print(node.name)
        return node


def read_input_code(input_file):
    if input_file == "":
        return sys.stdin.read()
    else:
        with open(input_file, "r") as input_file_handle:
            return input_file_handle.read()


def write_output_code(output_file, code):
    if output_file == "":
        sys.stdout.write(code)
        sys.stdout.flush()
    else:
        with open(output_file, "w") as output_file_handle:
            output_file_handle.write(code)
            output_file_handle.flush()


def print_usage(out_file):
    out_file.write("Usage: TODO\n")
    out_file.flush()


def main():
    # region Parse command line

    input_file = ""
    output_file = ""

    opts, args = getopt.getopt(sys.argv[1:], "i:o:h", ["--input=", "--output", "--help"])

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage(sys.stdout)
            return
        elif opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-o", "--output"):
            output_file = arg

    if input_file == "" and len(args) > 0:
        input_file = args.pop(0)

    if output_file == "" and len(args) > 0:
        output_file = args.pop(0)

    # endregion

    content = read_input_code(input_file)

    p = ast.parse(content)
    p = TestNodeTransformer().visit(p)
    s = astunparse.unparse(p)
    print(astunparse.dump(p))

    write_output_code(output_file, s)


if __name__ == '__main__':
    main()
