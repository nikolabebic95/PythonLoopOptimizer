from redbaron import Node, ForNode, NameNode


def has_break_or_continue(loop: Node) -> bool:
    return loop.find('break') is not None or loop.find('continue') is not None


def uses_iterator(loop: ForNode) -> bool:
    iterator_value = loop.iterator.value
    x = loop.value.find('name', value=iterator_value)
    return x is not None


def is_range_for(loop: ForNode) -> bool:
    return len(loop.target) == 2 and loop.target.find('name', value='range') is not None
