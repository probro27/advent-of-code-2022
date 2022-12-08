import sys
from typing import List
from dataclasses import dataclass
from pprint import pprint

@dataclass
class Tree:
    height: int
    visibility: str # 'LRUD' | 'E'
    
@dataclass
class NewTree:
    height: int
    visibility: List[int] # [L, R, U, D] | [0, 0, 0, 0] (for edges)
    scenic_score: int
    
    
def parseInputRound2():
    forest_map: List[List[NewTree]] = []
    init_map: List[List[str]] = []
    for line in sys.stdin:
        init_map.append(list(line.strip()))
    for row in init_map:
        new_row: List[int] = []
        for element in row:
            new_row.append(NewTree(element, [0, 0, 0, 0], 0))
        forest_map.append(new_row)
    return forest_map

def create_deep_copy(forest_map: List[List[NewTree]]):
    new_forest_map: List[List[NewTree]]= []
    for row in forest_map:
        new_row: List[NewTree] = []
        for tree in row:
            new_row.append(NewTree(tree.height, tree.visibility, tree.scenic_score))
        new_forest_map.append(new_row)
    return new_forest_map

def count_trees_visible(lst_before: List[int], height: int):
    reverse_lst_before = lst_before[::-1]
    trees_visible = 1
    stopping_index = -1
    for idx, element in enumerate(reverse_lst_before):
        if element < height:
            trees_visible += 1
        else:
            stopping_index = idx
            break
    if stopping_index == -1:
        trees_visible -= 1
    return trees_visible

# row_tree = [0: [3, 0, 3, 7, 3], 1: [2, 5]] Reach: 5
# Take row_tree[idx] => calculate from end how many trees less than 5 Start at 1
# Return 1 -> L: 1

def check_scenary(forest_map: List[List[NewTree]]):
    max_height_column: List[List[int]] = []
    max_height_row: List[List[int]] = []
    for idx, row in enumerate(forest_map):
        for col, tree in enumerate(row):
            if col == 0 or col == (len(row) - 1) or idx == 0 or idx == (len(forest_map) - 1):
                tree.visibility = [0, 0, 0, 0]
                if len(max_height_row) <= idx:
                    max_height_row.append([tree.height])
                else:
                    max_height_row[idx].append(tree.height)
                if len(max_height_column) <= col:
                    max_height_column.append([tree.height])
                else:
                    max_height_column[col].append(tree.height)
            else:
                if len(max_height_row) <= idx:
                    max_height_row.append([tree.height]) # should never occur
                else:
                    lst_before = max_height_row[idx]
                    tree.visibility[0] = count_trees_visible(lst_before=lst_before, height=tree.height)
                    max_height_row[idx].append(tree.height)
                if len(max_height_column) <= col:
                    max_height_column.append([tree.height]) # should never occur
                else: 
                    lst_before = max_height_column[col]
                    tree.visibility[2] = count_trees_visible(lst_before=lst_before, height=tree.height)
                    max_height_column[col].append(tree.height)
    new_forest_map = create_deep_copy(forest_map=forest_map)
    for _, row in enumerate(new_forest_map):
        row.reverse()
    new_forest_map.reverse()
    max_height_column = []
    max_height_row = []
    for idx, row in enumerate(new_forest_map):
        for col, tree in enumerate(row):
            if col == 0 or col == (len(row) - 1) or idx == 0 or idx == (len(forest_map) - 1):
                tree.visibility = [0, 0, 0, 0]
                if len(max_height_row) <= idx:
                    max_height_row.append([tree.height])
                else:
                    max_height_row[idx].append(tree.height)
                if len(max_height_column) <= col:
                    max_height_column.append([tree.height])
                else:
                    max_height_column[col].append(tree.height)
            else:
                if len(max_height_row) <= idx:
                    max_height_row.append([tree.height]) # should never occur
                else:
                    lst_before = max_height_row[idx]
                    tree.visibility[1] = count_trees_visible(lst_before=lst_before, height=tree.height)
                    max_height_row[idx].append(tree.height)
                if len(max_height_column) <= col:
                    max_height_column.append([tree.height]) # should never occur
                else: 
                    lst_before = max_height_column[col]
                    tree.visibility[3] = count_trees_visible(lst_before=lst_before, height=tree.height)
                    max_height_column[col].append(tree.height)
    return new_forest_map

def find_max_scenary(forest_map: List[List[NewTree]]):
    max_scenary: int = 1
    for row in forest_map:
        for tree in row:
            tree.scenic_score = tree.visibility[0] * tree.visibility[1] * tree.visibility[2] * tree.visibility[3]
            if tree.scenic_score > max_scenary:
                max_scenary = tree.scenic_score
    return max_scenary

if __name__ == '__main__':
    forest_map = parseInputRound2()
    new_forest_map = check_scenary(forest_map)
    pprint(new_forest_map)
    print(find_max_scenary(new_forest_map))
