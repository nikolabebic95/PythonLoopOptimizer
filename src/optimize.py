from redbaron import Node

from src.inline import inline_loop
from src.unroll import unroll_for
from src.vectorize import vectorize_loop


def optimize(root: Node) -> None:
    # For loops
    for_loops = root.find_all('for')
    for for_loop in for_loops:
        # TODO: Do not hardcode 10
        # inline_loop(for_loop, root)
        unroll_for(for_loop, 10)
        # vectorize_loop(for_loop, root)

    # While loops
    while_loops = root.find_all('while')
    for while_loop in while_loops:
        inline_loop(while_loop, root)
