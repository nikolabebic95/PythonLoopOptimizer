from redbaron import Node


def optimize(root: Node) -> None:
    # For loops
    for_loops = root.find_all('for')
    for for_loop in for_loops:
        for_loop.help()

    # While loops
    while_loops = root.find_all('while')
    for while_loop in while_loops:
        while_loop.help()
