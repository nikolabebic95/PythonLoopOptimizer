from redbaron import Node

from src.unroll import unroll_for


def optimize(root: Node) -> None:
    # For loops
    for_loops = root.find_all('for')
    for for_loop in for_loops:
        # TODO: Do not hardcode 10
        unroll_for(for_loop, 10)

    # While loops
    while_loops = root.find_all('while')
    for while_loop in while_loops:
        pass
