from redbaron import Node, ForNode, DefNode, RedBaron, NameNode, CallNode, AtomtrailersNode
from typing import List

from src.utils import has_parent_type, get_top_level_ancestor


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


def build_function(loop: ForNode) -> DefNode:
    name = 'cuda_kernel_from_line_' + str(loop.absolute_bounding_box.top_left.line)
    baron = RedBaron('def ' + name + '():\n    pass\n')
    ret = baron[0]
    ret.value[0] = loop.copy()

    ret.decorators = '@numba.guvectorize([(numba.float64[:, :], numba.float64[:, :])], \'(n, m)->(n, m)\')'

    variables = get_all_variables(ret)
    ret.arguments = ', '.join(variables)

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
    parent.insert(index_on_parent, '# comment')

    index = loop.index_on_parent
    p = loop.parent
    p.remove(loop)
    p.insert(index, func.name + '(' + func.arguments.dumps() + ')\n')

