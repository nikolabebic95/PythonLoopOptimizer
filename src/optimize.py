from optparse import Values

from redbaron import Node

from src.inline import inline_loop
from src.unroll import unroll_for
from src.vectorize import vectorize_loop


def optimize(root: Node, opts) -> None:
    # For loops
    for_loops = root.find_all('for')
    for for_loop in for_loops:
        if opts.unroll:
            unroll_for(for_loop, opts.unroll_by)
        if opts.inline:
            inline_loop(for_loop, root)
        if opts.cuda:
            vectorize_loop(for_loop, root)

    # While loops
    while_loops = root.find_all('while')
    for while_loop in while_loops:
        if opts.inline:
            inline_loop(while_loop, root)
