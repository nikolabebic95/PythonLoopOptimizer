from redbaron import Node, ForNode


def has_node_type(loop: Node, node_type: str) -> bool:
    return loop.find(node_type) is not None


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
