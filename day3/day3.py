import sys
from typing import List

def split_list(alist: List[str], wanted_parts=2) -> List[List[str]]:
    length = len(alist)
    return [ alist[i * length // wanted_parts: (i + 1) * length // wanted_parts] 
            for i in range(wanted_parts) ]
    
def find_common_element(list1: List[str], list2: List[str]) -> str:
    common_element = ''
    hashMap = {}
    for element in list1:
        hashMap[element] = 1
    for element in list2:
        if element in hashMap.keys():
            common_element = element
            break
    return common_element

def find_common_element_general(general_list: List[List[str]]) -> str:
    common_element = ''
    hash_map = {}
    for lst in general_list:
        list_hash_set = set()
        for element in lst:
            list_hash_set.add(element)
        for element in list_hash_set:
            if element in hash_map.keys():
                hash_map[element] += 1
            else:
                hash_map[element] = 1
        # print(f"Set: {list_hash_set}, Map: {hash_map}")
    for element in hash_map.keys():
        if hash_map[element] == 3:
            common_element = element
    return common_element

def find_priority(element: str) -> int:
    if element.isupper():
        return (ord(element[0]) - 64) + 26
    else:
        return (ord(element[0]) - 96)

def parseInputRound2():
    sum_of_priorities = 0
    line_count = 0
    per_group_list = []
    for line in sys.stdin:
        line_count += 1
        if line_count % 3 == 0:
            per_group_list.append(list(line.strip()))
            line_count = 0
            per_group_game_element = find_common_element_general(per_group_list)
            # print(f"Priority element: {per_group_game_element}, List: {per_group_list}")
            priority = find_priority(per_group_game_element)
            # print(f"Priority element: {per_group_game_element}, Priority: {priority}")
            sum_of_priorities += priority
            per_group_list = []
            per_group_game_element = ''
        else:
            per_group_list.append(list(line.strip()))
    return sum_of_priorities

def parseInputRound1():
    sum_of_priorities = 0
    for line in sys.stdin:
        (list1, list2) = split_list(list(line))
        common_element = find_common_element(list1, list2)
        priority = find_priority(common_element)
        sum_of_priorities += priority
        print(f"Priority element: {common_element}, Priority: {priority}")
    return sum_of_priorities

if __name__ == '__main__':
    # print(f"Part 1: {parseInputRound1()}")
    print(f'Part 2: {parseInputRound2()}')
    # lst = [['v', 'J', 'r', 'w', 'p', 'W', 't', 'w', 'J', 'g', 'W', 'r', 'h', 'c', 's', 'F', 'M', 'M', 'f', 'F', 'F', 'h', 'F', 'p'], ['j', 'q', 'H', 'R', 'N', 'q', 'R', 'j', 'q', 'z', 'j', 'G', 'D', 'L', 'G', 'L', 'r', 's', 'F', 'M', 'f', 'F', 'Z', 'S', 'r', 'L', 'r', 'F', 'Z', 's', 'S', 'L']]
    # print(find_common_element_general(lst))
    
