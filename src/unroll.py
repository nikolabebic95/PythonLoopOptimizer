from redbaron import ForNode, WhileNode

from src.utils import uses_iterator, is_range_for


def unroll_for(loop: ForNode, n: int) -> None:
    if uses_iterator(loop):
        return

    if not is_range_for(loop):
        return

    cloned = loop.copy()

    # TODO: Fix this mess, perform better checking
    # TODO: Do better when range_var is constant
    range_var = loop.target[1].value[0].value.value
    loop.target[1].value[0].value.value = range_var + " // " + str(n)
    cloned.target[1].value[0].value.value = range_var + " % " + str(n)

    # Hack needed because redbaron does not indent the first line correctly if it contains code
    loop.insert(0, "\n")

    length = len(loop)
    for i in range(n - 1):
        loop.extend(loop[0:length])

    # Remove the line that was added for the hack
    loop.remove(loop[0])
    loop.parent.insert(loop.index_on_parent, cloned)


# TODO: While loop unroll
def unroll_while(loop: WhileNode):
    pass
