from redbaron import Node

from src.inline import inline_loop
from src.unroll import unroll_for
from src.utils import should_ignore, should_optimize
from src.vectorize import vectorize_loop


def optimize(root: Node, opts) -> None:
    # For loops
    for_loops = root.find_all('for')
    for for_loop in for_loops:
        if should_ignore(for_loop):
            continue
        if (opts.unroll or should_optimize(for_loop, 'unroll')) and not should_ignore(for_loop, 'unroll'):
            unroll_for(for_loop, int(opts.unroll_by))
        if (opts.inline or should_optimize(for_loop, 'inline')) and not should_ignore(for_loop, 'inline'):
            inline_loop(for_loop, root)
        if (opts.cuda or should_optimize(for_loop, 'cuda')) and not should_ignore(for_loop, 'cuda'):
            vectorize_loop(for_loop, root)

    # While loops
    while_loops = root.find_all('while')
    for while_loop in while_loops:
        if (opts.inline or should_optimize(while_loop, 'inline')) and not should_ignore(while_loop, 'inline'):
            inline_loop(while_loop, root)
