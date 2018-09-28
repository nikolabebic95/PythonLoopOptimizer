from redbaron import Node, ForNode, DefNode, EndlNode, LineProxyList, ReturnNode, AtomtrailersNode, NodeList, RedBaron, \
    CommentNode
from typing import Dict
import re

from src.redbaron_helpers import fix_indentation

NUMBER_REGEX = re.compile('^\s*\(?\s*(-?\d+)\s*\)?\s*$')
VARIABLE_OR_NUMBER_REGEX = re.compile('^\s*\(?\s*(-?[a-zA-Z0-9_]+)\s*\)?\s*$')

PRAGMA_COMMENT = re.compile('^#\s*pragma.*$')
IGNORE_COMMENT = re.compile('^.*ignore.*$')
OPTIMIZE_COMMENT = re.compile('^.*optimize.*$')
UNROLL_COMMENT = re.compile('^.*unroll.*$')
INLINE_COMMENT = re.compile('^.*inline.*$')
CUDA_COMMENT = re.compile('^.*cuda.*$')

COMMENTS = {
    'pragma': PRAGMA_COMMENT,
    'ignore': IGNORE_COMMENT,
    'optimize': OPTIMIZE_COMMENT,
    'unroll': UNROLL_COMMENT,
    'inline': INLINE_COMMENT,
    'cuda': CUDA_COMMENT
}


def has_node_type(loop: Node, node_type: str) -> bool:
    return loop.find(node_type) is not None


def has_parent_type(node: Node, parent_type: str) -> bool:
    return node.parent_find(parent_type) is not None


def has_node_type_and_value(loop: Node, node_type: str, node_value: str) -> bool:
    return loop.find(node_type, value=node_value) is not None


def has_break(loop: Node) -> bool:
    return has_node_type(loop, 'break')


def has_continue(loop: Node) -> bool:
    return has_node_type(loop, 'continue')


def has_break_or_continue(loop: Node) -> bool:
    return has_break(loop) or has_continue(loop)


def uses_iterator(loop: ForNode) -> bool:
    iterator_value = loop.iterator.value
    x = loop.value.find('name', value=iterator_value)
    return x is not None


def is_range_for(loop: ForNode) -> bool:
    return len(loop.target) == 2 and has_node_type_and_value(loop.target, 'name', 'range')


def rename_variables(scope: Node, mapping: Dict[str, str]) -> None:
    nodes = scope.value.find_all('name')
    for node in nodes:
        if node.value not in mapping:
            continue
        node.value = mapping[node.value]


def is_constant(expression: str) -> bool:
    return NUMBER_REGEX.search(expression) is not None


def get_constant(expression: str) -> int:
    return int(NUMBER_REGEX.sub('\\1', expression))


def is_var_or_num(expression: str) -> bool:
    return VARIABLE_OR_NUMBER_REGEX.search(expression) is not None


def get_var_or_num(expression: str) -> str:
    return VARIABLE_OR_NUMBER_REGEX.sub('\\1', expression)


def is_in_global_scope(node: Node) -> bool:
    return node.parent_find('def') is None


def remove_node(node: Node) -> None:
    node.parent.remove(node.parent.value[node.index_on_parent])


def get_lines_from_scope(scope: LineProxyList):
    return [line for line in scope if not isinstance(line, EndlNode)]


def is_single_line_function(func: DefNode) -> bool:
    lines = get_lines_from_scope(func.value)
    return len(lines) == 1


def get_single_line_from_function(func: DefNode) -> Node:
    line = get_lines_from_scope(func.value)[0]
    if isinstance(line, ReturnNode):
        return line.value
    return line


def get_scope_level_ancestor(node: Node) -> Node:
    while not isinstance(node.parent.value, LineProxyList):
        node = node.parent
    return node


def get_top_level_ancestor(node: Node) -> Node:
    while node.parent.parent is not None:
        node = node.parent
    return node


def insert(scope: Node, exp: Node, index: int) -> None:
    if isinstance(exp.value, NodeList) and not isinstance(exp.value[0], EndlNode):
        fix_indentation(exp, len(scope.value[0].indentation))
        scope.insert(index, exp)
    else:
        scope.insert(index, exp)


def is_recursive(func: DefNode) -> bool:
    name_node = func.value.find('name', value=func.name)
    return name_node is not None and isinstance(name_node.parent, AtomtrailersNode)


def is_generator(func: DefNode) -> bool:
    return func.find('yield') is not None


def is_comment_type(comment: CommentNode, comment_type: str) -> bool:
    return COMMENTS[comment_type].search(comment.value) is not None


def should_optimize(loop: Node, optimization_type: str) -> bool:
    comments = loop.value.find_all('comment', recursive=False)
    for comment in comments:
        if is_comment_type(comment, 'pragma') and is_comment_type(comment, 'optimize'):
            if is_comment_type(comment, optimization_type):
                return True
    return False


def should_ignore(loop: Node, optimization_type: str = '') -> bool:
    comments = loop.value.find_all('comment', recursive=False)
    for comment in comments:
        if is_comment_type(comment, 'pragma') and is_comment_type(comment, 'ignore'):
            if optimization_type == '':
                return True
            if is_comment_type(comment, optimization_type):
                return True
    return False
