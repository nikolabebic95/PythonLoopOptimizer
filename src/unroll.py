from redbaron import ForNode, Node
from typing import List, Dict

from src.utils import is_range_for, has_continue, rename_variables, is_constant, get_constant, is_var_or_num, \
    get_var_or_num


def get_range_params(range_node: Node) -> (str, str, str):
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

    if is_var_or_num(start):
        start = get_var_or_num(start)

    if is_var_or_num(end):
        end = get_var_or_num(end)

    if is_var_or_num(step):
        step = get_var_or_num(step)

    return start, end, step


def is_constant_loop(start: str, end: str, step: str) -> bool:
    return is_constant(start) and is_constant(end) and is_constant(step)


def get_constant_params(start: str, end: str, step: str) -> (int, int, int):
    return get_constant(start), get_constant(end), get_constant(step)


def get_num_of_iterations(start: int, end: int, step: int) -> int:
    return (end - start) // step


def get_real_end(start: int, end: int, step: int) -> int:
    return start + step * get_num_of_iterations(start, end, step)


def get_num_of_prologue_iterations(n: int, start: int, end: int, step: int) -> int:
    return get_num_of_iterations(start, end, step) % n


def get_prologue_iterators(n: int, start: int, end: int, step: int) -> List[int]:
    num_epilog_iterations = get_num_of_prologue_iterations(n, start, end, step)
    return [start + i * step for i in range(num_epilog_iterations)]


def unroll_for_prologue_constant(loop: ForNode, iterator_name: str, iterators: List[int]) -> None:
    for iterator in iterators:
        cloned = loop.copy()
        mapping = {iterator_name: str(iterator)}
        rename_variables(cloned, mapping)
        # TODO: Rename variables that might clash with the scope outside the loop
        for i in range(len(loop.value)):
            loop.parent.insert(loop.index_on_parent + i, cloned.value[i])


def build_prologue_end(n: int, start: str, end: str, step: str) -> str:
    if is_constant(start) and is_constant(end):
        start_int = get_constant(start)
        end_int = get_constant(end)
        second_part = '((' + str(end_int - start_int) + ') // ' + step + ') % ' + str(n)
        if start_int == 0:
            return second_part
        else:
            return start + ' + ' + second_part
    elif is_constant(start) and is_constant(step):
        start_int = get_constant(start)
        step_int = get_constant(step)
        if start_int == 0 and step_int == 1:
            return end + ' % ' + str(n)
        elif start_int == 0:
            return '(' + end + ' // ' + step + ') % ' + str(n)
        elif step_int == 1:
            return start + '(' + end + ' - ' + start + ') % ' + str(n)
        else:
            return start + ' + ((' + end + ' - ' + start + ') // ' + step + ') % ' + str(n)
    elif is_constant(start) and get_constant(start) == 0:
        return '(' + end + ' // ' + step + ') % ' + str(n)
    elif is_constant(step) and get_constant(step) == 1:
        return start + '(' + end + ' - ' + start + ') % ' + str(n)
    return start + ' + ((' + end + ' - ' + start + ') // ' + step + ') % ' + str(n)


def build_range_expression(n: int, start: str, end: str, step: str):
    step_string = step
    if is_constant(step):
        step_string = str(get_constant(step) * n)

    if is_constant(start) and get_constant(start) == 0 and is_constant(step_string) and get_constant(step_string) == 1:
        return 'range(' + end + ')'
    elif is_constant(step_string) and get_constant(step_string) == 1:
        return 'range(' + start + ', ' + end + ')'
    return 'range(' + start + ', ' + end + ', ' + step_string + ')'


def unroll_for_prologue_expression(loop: ForNode, n: int, start: str, end: str, step: str) -> None:
    cloned = loop.copy()
    prologue_end = build_prologue_end(n, start, end, step)
    cloned.target = build_range_expression(1, start, prologue_end, step)
    loop.parent.insert(loop.index_on_parent, cloned)


def unroll_for_prologue(loop: ForNode, n: int, start: str, end: str, step: str) -> None:
    if is_constant_loop(start, end, step):
        start_int, end_int, step_int = get_constant_params(start, end, step)
        end_int = get_real_end(start_int, end_int, step_int)
        iterators = get_prologue_iterators(n, start_int, end_int, step_int)
        unroll_for_prologue_constant(loop, loop.iterator.value, iterators)
    else:
        unroll_for_prologue_expression(loop, n, start, end, step)


def get_actual_loop_start(n: int, start: int, end: int, step: int) -> int:
    return start + get_num_of_prologue_iterations(n, start, end, step) * step


def build_range_constant(start: int, end: int, step: int) -> str:
    if start == 0 and step == 1:
        return 'range(' + str(end) + ')'
    elif step == 1:
        return 'range(' + str(start) + ', ' + str(end) + ')'
    return 'range(' + str(start) + ', ' + str(end) + ', ' + str(step) + ')'


def create_mapping(iterator: str, step: str, index: int) -> Dict[str, str]:
    rhs = step + ' * ' + str(index)

    if is_constant(step):
        rhs = str(get_constant(step) * index)

    return {iterator: '(' + iterator + ' + ' + rhs + ')'}


def unroll_for_actual_loop_content(loop: ForNode, n: int, step: str) -> None:
    cloned = loop.copy()

    for i in range(n - 1):
        to_extend = cloned.copy()
        mapping = create_mapping(loop.iterator.value, step, i + 1)
        rename_variables(to_extend, mapping)
        loop.extend(to_extend.value)


def unroll_for_actual_loop_constant(loop: ForNode, n: int, start: int, end: int, step: int) -> None:
    actual_start = get_actual_loop_start(n, start, end, step)
    loop.target = build_range_constant(actual_start, end, step * n)
    unroll_for_actual_loop_content(loop, n, str(step))


def unroll_for_actual_loop_expression(loop: ForNode, n: int, start: str, end: str, step: str) -> None:
    actual_start = build_prologue_end(n, start, end, step)
    loop.target = build_range_expression(n, actual_start, end, step)
    unroll_for_actual_loop_content(loop, n, step)


def unroll_for_actual_loop(loop: ForNode, n: int, start: str, end: str, step: str) -> None:
    if is_constant_loop(start, end, step):
        start_int, end_int, step_int = get_constant_params(start, end, step)
        end_int = get_real_end(start_int, end_int, step_int)
        unroll_for_actual_loop_constant(loop, n, start_int, end_int, step_int)
    else:
        unroll_for_actual_loop_expression(loop, n, start, end, step)


def unroll_for(loop: ForNode, n: int) -> None:
    if not is_range_for(loop):
        return

    if has_continue(loop):
        return

    start, end, step = get_range_params(loop.target[1])

    unroll_for_prologue(loop, n, start, end, step)
    unroll_for_actual_loop(loop, n, start, end, step)
