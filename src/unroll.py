from redbaron import ForNode, WhileNode, Node

from src.utils import uses_iterator, is_range_for, has_continue


def get_range_params(range_node: Node) -> (str, str, str):
    print(range_node.help())
    start = '0'
    end = '1'
    step = '1'

    if len(range_node) == 1:
        end = range_node[0].value.dumps()
    if len(range_node) == 2:
        start = range_node[0].value.dumps()
        end = range_node[1].value.dumps()
    if len(range_node) == 3:
        start = range_node[0].value.dumps()
        end = range_node[1].value.dumps()
        step = range_node[2].value.dumps()

    start = '(' + start + ')'
    end = '(' + end + ')'
    step = '(' + step + ')'
    return start, end, step


def unroll_for_prologue(loop: ForNode, n: int) -> None:
    cloned = loop.copy()
    range_var = loop.target[1].value[0].value.value
    cloned.target[1].value[0].value.value = range_var + " % " + str(n)
    loop.parent.insert(loop.index_on_parent, cloned)


def unroll_for_prologue_constant(loop: ForNode, n: int) -> None:
    pass


def unroll_for_prologue_expression(loop: ForNode, n: int) -> None:
    pass


def unroll_for(loop: ForNode, n: int) -> None:
    if uses_iterator(loop):
        return

    if not is_range_for(loop):
        return

    if has_continue(loop):
        return

    start, end, step = get_range_params(loop.target[1])
    print(start, end, step)

    # TODO: Determine if N is a constant
    unroll_for_prologue(loop, n)

    # TODO: Fix this mess, perform better checking
    # TODO: Do better when range_var is constant
    range_var = loop.target[1].value[0].value.value
    loop.target[1].value[0].value.value = range_var + " // " + str(n)

    # Hack needed because redbaron does not indent the first line correctly if it contains code
    loop.insert(0, "\n")

    length = len(loop)
    for i in range(n - 1):
        loop.extend(loop[0:length])

    # Remove the line that was added for the hack
    loop.remove(loop[0])


# TODO: While loop unroll
def unroll_while(loop: WhileNode):
    pass
