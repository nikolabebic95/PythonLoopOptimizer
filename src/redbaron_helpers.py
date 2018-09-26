from redbaron import IfelseblockNode


def count_leading_spaces(string: str) -> int:
    return len(string) - len(string.lstrip(' '))


def fix_indentation(if_else_node: IfelseblockNode, starting_indent: int) -> None:
    dump = if_else_node.dumps()
    lines = dump.split('\n')
    indentation = -1
    result = []
    for line in lines:
        res = line
        if indentation == -1:
            indentation = count_leading_spaces(line)
            result.append(' ' * starting_indent + line.lstrip())
            continue
        new_indent = count_leading_spaces(line)
        if new_indent > indentation:
            indentation = indentation + 4
            res = ' ' * (starting_indent + indentation) + line.lstrip(' ')
        result.append(res)
    code = '\n'.join(result).rstrip()
    if_else_node.replace(code)
