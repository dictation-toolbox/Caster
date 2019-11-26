def list_update_unique(a_list, new_item, should_include):
    """
    Modifies a list, safely and quickly, such that the new item:
    1. won't be inserted in the list if it is already in the list
    2. won't throw an error if it is supposed to be removed and isn't in the list

    :param a_list: list to be altered
    :param new_item: new item to be added/removed
    :param should_include: whether the new item should be in the list after this function call
    """
    a_set = frozenset(a_list)
    if should_include and new_item not in a_set:
        a_list.append(new_item)
    elif new_item in a_set and not should_include:
        a_list.remove(new_item)
    return list(a_list)
