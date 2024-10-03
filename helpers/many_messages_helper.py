import re


def compile_pair(list1: list, list2: list) -> list:
    result = []
    for elem1 in list1:
        for elem2 in list2:
            if isinstance(elem2, tuple):
                result.append((elem1, *elem2))
            else:
                result.append((elem1, elem2))
    return result


def compile_lists(lists: list[list]) -> list[list]:
    if len(lists) == 1:
        return lists
    while True:
        if len(lists) == 1:
            return lists[0]
        the_last = lists.pop()
        the_previous = lists.pop()
        lists.append(compile_pair(the_previous, the_last))


def check_replays(input_str: str) -> list:
    pattern = re.compile("(&&.*?&&)")
    matches = re.findall(pattern, input_str)
    if not matches:
        return []
    all_lists = []
    for match in matches:
        match_list = match.replace("&&", "").split(", ")
        all_lists.append(match_list)
    changes = compile_lists(all_lists)
    result_strs = []
    for change in changes:
        result_str = input_str
        for index, match in enumerate(matches):
            result_str = result_str.replace(match, change[index])
        result_strs.append(result_str)
    return result_strs
