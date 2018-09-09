from redbaron import Node


def inline_loop(loop: Node, root: Node) -> None:
    # TODO: Solve problem when there is too much endlines and redbaron puts wrong indentation
    # TODO: Inline functions with parameters and return values
    atomtrailers = loop.value.find_all('atomtrailers')
    for atomtrailer in atomtrailers:
        if len(atomtrailer.value) != 2:
            # If the function is not defined in the same file, it cannot be inlined
            continue

        name = atomtrailer.value[0].value

        definition = root.find('def', name=name)

        parent = atomtrailer.parent
        index_on_parent = atomtrailer.index_on_parent
        parent.remove(parent[index_on_parent])

        for index, item in enumerate(definition.value):
            parent.insert(index_on_parent + index, item)
