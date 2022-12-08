import sys
from typing import List
from dataclasses import dataclass
from pprint import pprint

@dataclass
class Tree:
    height: int
    visibility: str # 'LRUD' | 'E'

def parseInput():
    forest_map: List[List[Tree]] = []
    init_map: List[List[str]] = []
    for line in sys.stdin:
        init_map.append(list(line.strip()))
    for row in init_map:
        new_row: List[int] = []
        for element in row:
            new_row.append(Tree(element, ''))
        forest_map.append(new_row)
    return forest_map

def create_deep_copy(forest_map: List[List[Tree]]):
    new_forest_map: List[List[Tree]]= []
    for row in forest_map:
        new_row: List[Tree] = []
        for tree in row:
            new_row.append(Tree(tree.height, tree.visibility))
        new_forest_map.append(new_row)
    return new_forest_map

def convert_to_tree(forest_map: List[List[Tree]]):
    max_height_column: List[int] = []
    max_height_row: List[int] = []
    for idx, row in enumerate(forest_map):
        for col, tree in enumerate(row):
            if col == 0 or col == (len(row) - 1) or idx == 0 or idx == (len(forest_map) - 1):
                tree.visibility = 'E'
                if len(max_height_row) <= idx:
                    max_height_row.append(tree.height)
                else: 
                    if tree.height > max_height_row[idx]:
                        max_height_row[idx] = tree.height
                if len(max_height_column) <= col:
                    max_height_column.append(tree.height)
                else:
                    if tree.height > max_height_column[col]:
                        max_height_column[col] = tree.height
            else:
                if len(max_height_row) <= idx:
                    max_height_row.append(tree.height)
                else:
                    if tree.height > max_height_row[idx]:
                        max_height_row[idx] = tree.height
                        tree.visibility += 'L'
                if len(max_height_column) <= col:
                    max_height_column.append(tree.height)
                else: 
                    if tree.height > max_height_column[col]:
                        max_height_column[col] = tree.height
                        tree.visibility += 'U'
    new_forest_map = create_deep_copy(forest_map=forest_map)
    for _, row in enumerate(new_forest_map):
        row.reverse()
    new_forest_map.reverse()
    max_height_column = []
    max_height_row = []
    for idx, row in enumerate(new_forest_map):
        for col, tree in enumerate(row):
            if col == 0 or col == (len(row) - 1) or idx == 0 or idx == (len(forest_map) - 1):
                tree.visibility = 'E'
                if len(max_height_row) <= idx:
                    max_height_row.append(tree.height)
                else: 
                    if tree.height > max_height_row[idx]:
                        max_height_row[idx] = tree.height
                if len(max_height_column) <= col:
                    max_height_column.append(tree.height)
                else:
                    if tree.height > max_height_column[col]:
                        max_height_column[col] = tree.height
            else:
                if len(max_height_row) <= idx:
                    max_height_row.append(tree.height)
                else:
                    if tree.height > max_height_row[idx]:
                        max_height_row[idx] = tree.height
                        tree.visibility += 'R'
                if len(max_height_column) <= col:
                    max_height_column.append(tree.height)
                else: 
                    if tree.height > max_height_column[col]:
                        max_height_column[col] = tree.height
                        tree.visibility += 'D'
    return new_forest_map

def count_trees_visible(forest_map: List[List[Tree]]):
    visible_trees = 0
    for row in forest_map:
        for tree in row:
            if tree.visibility != '':
                visible_trees += 1
    return visible_trees

if __name__ == '__main__':
    forest_map = parseInput()
    new_forest_map = convert_to_tree(forest_map)
    pprint(new_forest_map)
    print(count_trees_visible(new_forest_map))
