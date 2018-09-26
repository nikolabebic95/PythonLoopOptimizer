from redbaron import Node, NameNode, WhileNode, CallNode, DefNode, AtomtrailersNode
from typing import List, Set, Dict

from src.utils import rename_variables, is_in_global_scope, remove_node, is_single_line_function, \
    get_single_line_from_function, get_scope_level_ancestor, insert, is_recursive, is_generator


# RedBaron does not support type annotations, but this code should work
# even when RedBaron supports them
# https://github.com/PyCQA/baron/issues/127#issue-270939120
def get_all_parameters_as_list(func: DefNode) -> List[str]:
    return [name.value for name in func.arguments.find_all('name')]


def get_all_parameters(func: DefNode) -> Set[str]:
    return set(get_all_parameters_as_list(func))


def get_all_local_variables(func: DefNode) -> Set[str]:
    ret = set()
    parameters = get_all_parameters(func)

    assignments = func.value.find_all('assign')
    for assignment in assignments:
        if not isinstance(assignment.target, NameNode) or assignment.target.value in parameters:
            continue
        ret.add(assignment.target.value)

    global_names = func.value.find_all('global')
    for global_name_list in global_names:
        for global_name in global_name_list.value:
            if global_name.value in ret:
                ret.remove(global_name.value)

    # Not sure this is needed, for loop is a different scope
    # for_nodes = func.value.find_all('for')
    # for for_node in for_nodes:
        # ret.add(for_node.iterator.value)

    return ret


def get_all_names_in_scope(loop: Node) -> Set[str]:
    ret = set([name.value for name in loop.value.find_all('name')])
    if isinstance(loop, WhileNode):
        ret.update(set([name.value for name in loop.test.find_all('name')]))
    return ret


def get_all_actual_parameters(function_call: CallNode) -> List[str]:
    return ['(' + argument.dumps() + ')' for argument in function_call.value]


def create_parameters_mapping(formal_parameters: List[str], actual_parameters: List[str]):
    ret = {}
    for i in range(len(formal_parameters)):
        ret[formal_parameters[i]] = actual_parameters[i]
    return ret


def clone_function_with_variables(func: DefNode, mapping: Dict[str, str]) -> DefNode:
    ret = func.copy()
    rename_variables(ret, mapping)
    return ret


def create_name_clashes_mapping(func_local_vars: Set[str], loop_scope_names: Set[str]) -> Dict[str, str]:
    ret = {}
    for name in func_local_vars:
        if name in loop_scope_names:
            # TODO: Smarter rename
            ret[name] = name + '_'
    return ret


def fix_global_keyword_in_global_scope(loop: Node, cloned_function: DefNode):
    if is_in_global_scope(loop):
        global_keywords = cloned_function.find_all('global')
        for g in global_keywords:
            remove_node(g)


def inline_lines(scope_level_node: Node, cloned_function: DefNode) -> None:
    parent = scope_level_node.parent
    index_on_parent = scope_level_node.index_on_parent
    remove_node(scope_level_node)

    for index, item in enumerate(cloned_function.value):
        insert(parent, item, index_on_parent + index)


def inline_multiline_function(atomtrailer: AtomtrailersNode, cloned_function: DefNode) -> None:
    return_nodes = cloned_function.find_all('return')
    scope_level_node = get_scope_level_ancestor(atomtrailer)

    if scope_level_node.on_attribute != 'value':
        return

    for return_node in return_nodes:
        atomtrailer.replace(return_node.value)
        copy_of_scope_level_node = scope_level_node.copy()
        return_node.replace(copy_of_scope_level_node)

    inline_lines(scope_level_node, cloned_function)


def inline_loop(loop: Node, root: Node) -> None:
    # TODO: Solve problem when there is too much endlines and redbaron puts wrong indentation
    atomtrailers = loop.value.find_all('atomtrailers')
    for atomtrailer in atomtrailers:
        if len(atomtrailer.value) != 2:
            # If the function is not defined in the same file, it cannot be inlined
            continue

        name = atomtrailer.value[0].value

        definition = root.find('def', name=name)

        if definition is None:
            continue

        if is_recursive(definition):
            continue

        if is_generator(definition):
            continue

        actual_parameters = get_all_actual_parameters(atomtrailer.value[1])
        formal_parameters = get_all_parameters_as_list(definition)
        mapping = create_parameters_mapping(formal_parameters, actual_parameters)
        cloned_function = clone_function_with_variables(definition, mapping)

        func_local_vars = get_all_local_variables(definition)
        names_in_loop_scope = get_all_names_in_scope(loop)
        mapping = create_name_clashes_mapping(func_local_vars, names_in_loop_scope)
        rename_variables(cloned_function, mapping)

        if is_single_line_function(cloned_function):
            atomtrailer.replace(get_single_line_from_function(cloned_function))
        else:
            fix_global_keyword_in_global_scope(loop, cloned_function)
            inline_multiline_function(atomtrailer, cloned_function)
