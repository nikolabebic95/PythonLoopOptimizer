from redbaron import RedBaron
import sys
from optparse import OptionParser

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


def print_version() -> None:
    print("1.0.0.")


def build_parser() -> OptionParser:
    parser = OptionParser()
    parser.add_option('-f', '--file', dest='filename', help='input file name')
    parser.add_option('-o', '--output', dest='output', help='output file name')
    parser.add_option('-v', '--version', action='store_true', dest='version', default=False,
                      help='print version of optimizer')
    parser.add_option('-u', '--unroll', action='store_true', dest='unroll', default=False,
                      help='perform unroll optimization')
    parser.add_option('-k', '--unroll_by', dest='unroll_by', default=8, help='unroll')
    parser.add_option('-i', '--inline', action='store_true', dest='inline', default=False,
                      help='perform inline optimization')
    parser.add_option('-c', '--cuda', action='store_true', dest='cuda', default=False,
                      help='perform cuda optimization')
    return parser


def main() -> None:
    # region Parse command line

    parser = build_parser()
    opts, args = parser.parse_args()

    if opts.filename is None and len(args) > 0:
        opts.filename = args.pop(0)

    if opts.output is None and len(args) > 0:
        opts.output = args.pop(0)

    # endregion

    if opts.version:
        print_version()
        exit(0)

    content = read_input_code(opts.filename)

    root = RedBaron(content)
    optimize(root, opts)
    write_output_code(opts.output, root.dumps())


if __name__ == '__main__':
    main()
