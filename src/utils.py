from redbaron import Node


def has_break_or_continue(loop: Node) -> bool:
    return loop.find('break') is not None or loop.find('continue') is not None
