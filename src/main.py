from io import TextIOWrapper
from redbaron import RedBaron
import sys
import getopt

from src.optimize import optimize


def read_input_code(input_file: str) -> str:
    if input_file == "":
        return sys.stdin.read()
    else:
        with open(input_file, "r") as input_file_handle:
            return input_file_handle.read()


def write_output_code(output_file: str, code: str) -> None:
    if output_file == "":
        sys.stdout.write(code)
        sys.stdout.flush()
    else:
        with open(output_file, "w") as output_file_handle:
            output_file_handle.write(code)
            output_file_handle.flush()


def print_usage(out_file: TextIOWrapper) -> None:
    out_file.write("Usage: TODO\n")
    out_file.flush()


def main() -> None:
    # region Parse command line

    input_file = ""
    output_file = ""

    opts, args = getopt.getopt(sys.argv[1:], "i:o:h", ["input=", "output=", "help"])

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

    root = RedBaron(content)
    optimize(root)
    write_output_code(output_file, root.dumps())


if __name__ == '__main__':
    main()
