from redbaron import Node, ForNode, DefNode, RedBaron, NameNode, CallNode, AtomtrailersNode, GetitemNode
from typing import List

from src.utils import has_parent_type, get_top_level_ancestor


WARNING_MESSAGE = [
    '# WARNING!!! This code assumes that all types passed to this function are floats.\n',
    '# If the actual types are not all float64, you must edit the \'guvectorize\' decorator.\n',
    '# The order of the types in the decorator is the same as the order of the function parameters\n'
]


def add_import(root: Node) -> None:
    root.insert(0, 'import numba\n')


def get_all_variables(func: DefNode) -> List[str]:
    ret = set([name.value for name in func.value.find_all('name')])

    atomtrailers = func.value.find_all('atomtrailers')
    for atomtrailer in atomtrailers:
        for name in [node for node in atomtrailer.value[:-1] if isinstance(atomtrailer.value[-1], CallNode)]:
            if name.value in ret:
                ret.remove(name.value)

    last_param = None

    assignments = func.value.find_all('assign')
    for assignment in assignments:
        if isinstance(assignment.target, NameNode) and assignment.target.value in ret:
            ret.remove(assignment.target.value)
        if isinstance(assignment.target, AtomtrailersNode):
            last_param = assignment.target[0].value
            ret.remove(last_param)

    for_nodes = func.value.find_all('for')
    for for_node in for_nodes:
        names = for_node.iterator.find_all('name')
        for name in names:
            if name.value in ret:
                ret.remove(name.value)

    return [value for value in ret] + [last_param]


def get_dimension(func: DefNode, variable: str) -> int:
    occurrences = func.value.find_all('name', value=variable)
    ret = 0
    for occurrence in occurrences:
        parent = occurrence.parent
        if isinstance(parent, AtomtrailersNode) and isinstance(parent[-1], GetitemNode):
            dimension = len(parent[-1].value.value)
            if dimension > ret:
                ret = dimension
    return ret


def build_decorator(func: DefNode, variables: List[str]) -> str:
    types = []
    sizes = []

    index = ord('a')
    default_type = 'float64'

    for variable in variables:
        dimension = get_dimension(func, variable)
        if dimension > 0:
            variable_types = 'numba.' + default_type + '[' + ', '.join(':' * dimension) + ']'
        else:
            variable_types = 'numba.' + default_type
        types.append(variable_types)
        chars = [chr(i) for i in range(index, index + dimension)]
        index = index + dimension
        sizes.append('(' + ', '.join(chars) + ')')

    return '@numba.guvectorize([(' + ', '.join(types) + ')], \'' + ', '.join(sizes[:-1]) + '->' + sizes[-1] + '\')'


def build_function(loop: ForNode) -> DefNode:
    name = 'cuda_kernel_from_line_' + str(loop.absolute_bounding_box.top_left.line)
    baron = RedBaron('def ' + name + '():\n    pass\n')
    ret = baron[0]
    ret.value[0] = loop.copy()

    ret.decorators = '@numba.guvectorize([(numba.float64[:, :], numba.float64[:, :])], \'(n, m)->(n, m)\')'

    variables = get_all_variables(ret)
    ret.arguments = ', '.join(variables)

    print(build_decorator(ret, variables))

    return ret


def vectorize_loop(loop: ForNode, root: Node):
    if has_parent_type(loop, 'for'):
        return

    func = build_function(loop)
    add_import(root)

    ancestor = get_top_level_ancestor(loop)

    parent = ancestor.parent
    index_on_parent = ancestor.index_on_parent
    parent.insert(index_on_parent, func)
    for m in reversed(WARNING_MESSAGE):
        parent.insert(index_on_parent, m)

    index = loop.index_on_parent
    p = loop.parent
    p.remove(loop)
    p.insert(index, func.name + '(' + func.arguments.dumps() + ')\n')

